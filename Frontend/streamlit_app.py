# -*- coding: utf-8 -*-


import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import plotly.express as px
import datetime


st.set_page_config(layout="wide")
#Navigation menu
selected = option_menu(
        menu_title = None,
        options= ["Prediction of demand", "Dashboard"],
        icons = ["bar-chart-line", "bicycle"],
        orientation = "horizontal"
        
    )




df_stations = pd.read_csv("Frontend/stations_final.csv")
predictions_total = pd.read_csv("Frontend/predictions_all_stations.csv")
rides_per_day = pd.read_csv("Frontend/movements_grouped.csv")

if selected == "Prediction of demand":
    visualization = st.sidebar.selectbox("Select the type of visualization: ", ["All stations", "Demand per zones"])
    if visualization == "Demand per zones":
        postal_code = st.sidebar.selectbox('Postal code', list(df_stations['postal_code'].unique()))
    
    with st.container():
        st.write("---")
        line_chart_data = predictions_total.copy()
        fig = px.line(line_chart_data)
        
        fig.update_layout(
                showlegend = False,
                width = 1000,
                height = 400,
                margin = dict(l=1, r=1, b=1, t=1),
                font = dict(color = "#383635", size = 15)
        )
        st.write(fig)
        #fig.update_xaxes(type='category')
                
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Demand prediction BICIMAD")
            
     
            
        with right_column:    
            df_stations['lat']= df_stations['latitude']
            df_stations['lon']=df_stations['longitude']
            df_stations = df_stations[['lat', 'lon', 'postal_code']]
            
            if visualization == "Demand per zones":
                st.map(df_stations[df_stations['postal_code']==postal_code])
                
            if visualization == "All stations":
                
                st.map(df_stations)
                
if selected == "Dashboard":
   month_options = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
  

    year = st.sidebar.selectbox("Select the year: ", [2021,2020,2019])
    month = st.sidebar.multiselect("Select the month: ", [1,2,3,4,5,6,7,8,9,10,11,12], default=[1,2,3,4,5,6,7,8,9,10,11,12], format_func=lambda x: month_options.get(x))
    average_demand_per_day = int(rides_per_day[(rides_per_day['year']==year)]['rides'].mean())
    average_demand_per_day_year_before = int(rides_per_day[(rides_per_day['year']==year-1)]['rides'].mean())
    percentual_variation_demand_year = round(((average_demand_per_day - average_demand_per_day_year_before) / average_demand_per_day_year_before)*100,2)
    avg_rides_per_hour = rides_per_day[rides_per_day['year']==year].groupby(['hour']).mean().reset_index()
    max_rides = avg_rides_per_hour['rides'].max()
    peak_hour = avg_rides_per_hour[avg_rides_per_hour['rides'] == max_rides]['hour']
    avg_rides_day = rides_per_day[rides_per_day['year'] == year].groupby(['weekday']).mean().reset_index()
    max_demand = avg_rides_day['rides'].max()
    peak_day = avg_rides_day[avg_rides_day['rides']==max_demand]['weekday']
    peak_day = str(peak_day)[5:-29]
    available_docks = df_stations['total_bases'].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Avg. demand per hour", value = average_demand_per_day, delta = percentual_variation_demand_year)
    col2.metric(label="Peak hour demand", value = peak_hour)
    col3.metric(label = "Peak day demand", value = peak_day)
    col4.metric(label = "Nº of available docks", value = available_docks)

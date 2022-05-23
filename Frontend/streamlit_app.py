# -*- coding: utf-8 -*-


import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import plotly.express as px


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
    year = st.sidebar.selectbox("Select the year: ", [2021,2020,2019])
    average_demand_per_day = int(rides_per_day[rides_per_day['year']==year]['rides'].mean())
    average_demand_per_day_year_before = int(rides_per_day[rides_per_day['year']==year-1]['rides'].mean())
    percentual_variation_demand_year = ((average_demand_per_day - average_demand_per_day_year_before) / average_demand_per_day_year_before)*100
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Avg. demand per day", value = average_demand_per_day, delta = percentual_variation_demand_year) 

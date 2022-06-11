# -*- coding: utf-8 -*-


import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import plotly.express as px
import datetime
import seaborn as sns
import plotly.graph_objects as go


st.set_page_config(layout="wide")
#Navigation menu
selected = option_menu(
        menu_title = None,
        options= ["Prediction of demand", "Dashboard"],
        icons = ["bar-chart-line", "bicycle"],
        orientation = "horizontal"
        
    )




df_stations = pd.read_csv("Frontend/stations_postal_code.csv")
predictions_total = pd.read_csv("Frontend/predictions_all_stations.csv")
predictions_per_zone = pd.read_csv("Frontend/predictions_per_zone.csv")
rides_per_hour = pd.read_csv("Frontend/movements_grouped.csv")
evaluation_models = pd.read_csv("Frontend/evaluation_models_global_demand.csv")

if selected == "Prediction of demand":
    visualization = st.sidebar.selectbox("Select the type of visualization: ", ["All stations", "Demand per zones"])
    if visualization == "Demand per zones":
        postal_code = st.sidebar.selectbox('Postal code', list(df_stations['postal_code'].unique()))
        model = "default"
    scope = st.sidebar.radio('Period: ', ['next 24 hours', 'next 14 days'])
    if visualization == "All stations":
        model = st.sidebar.radio('Model:', ['Random Forest', 'Light GBM', 'Catboost', 'Compare models'])
    with st.container():
        if scope == 'next 14 days':
                st.header("Predictions for the next 14 days")
        if scope == 'next 24 hours':
                st.header("Predictions for the next 24 hours")
        
        if visualization == "All stations":
                if scope == "next 24 hours":
                        predictions_global_show = predictions_total[predictions_total['day']=='2021-07-01']
                if scope == "next 14 days":
                        predictions_global_show = predictions_total
                if model == 'Compare models':
                        fig = px.line(predictions_global_show, x = 'datetime', y = 'pred', color = 'model')
 
                        fig.update_layout(
                                showlegend = True,
                                width = 1400,
                                height = 400,
                                margin = dict(l=1, r=1, b=1, t=1),
                                font = dict(color = "#383635", size = 15)
                        )
                        fig.update_xaxes(
                                rangeslider_visible = True,
                                rangeselector=dict(
                                        buttons = list([
                                        dict(count=1, label = "1d", step = "day", stepmode="todate"),
                                        dict(step="all")])
                                ))
                        st.write(fig)
                        
                if model != 'Compare models':
                        predictions_global_final = predictions_global_show[predictions_global_show['model']==model]
                        max_demand = predictions_global_final['pred'].max()
                        predictions_global_max = predictions_global_final[predictions_global_final['pred']==max_demand]
                        fig = px.line(predictions_global_final, x = 'datetime', y = 'pred')
        
                        fig.update_layout(
                                showlegend = False,
                                width = 1400,
                                height = 400,
                                margin = dict(l=1, r=1, b=1, t=1),
                                font = dict(color = "#383635", size = 15)
                        )
                        fig.update_xaxes(
                                rangeslider_visible = True,
                                rangeselector=dict(
                                        buttons = list([
                                        dict(count=1, label = "1d", step = "day", stepmode="todate"),
                                        dict(step="all")])
                                ))
                        
                     
              
                
                        st.write(fig)
        if visualization == "Demand per zones":
                     if scope == 'next 24 hours':
                        predictions_per_zone_show = predictions_per_zone[predictions_per_zone['day']=='2021-07-01']
                     if scope == 'next 14 days':
                        predictions_per_zone_show = predictions_per_zone
                     predictions_zone = predictions_per_zone_show[predictions_per_zone_show['postal_code'] == postal_code]
                     max_demand = predictions_zone['pred'].max()
                     predictions_zone_max = predictions_zone[predictions_zone['pred']==max_demand]
                        
                     fig = px.line(predictions_zone, x= 'datetime', y='pred')
                     fig.update_layout(
                        showlegend = True,
                        width = 1400,
                        height = 400,
                        margin = dict(l=1, r=1, b=1, t=1),
                        font = dict(color = "#383635", size = 15)
                        )
                     fig.update_xaxes(
                        rangeslider_visible = True,
                        rangeselector=dict(
                                buttons = list([
                                        dict(count=1, label = "1d", step = "day", stepmode="todate"),
                                        dict(step="all")])
                             ))
                        
                     st.write(fig)
                
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Some useful data")
            if visualization == "Demand per zones":
                peak_hour_max_demand = predictions_zone[predictions_zone['pred']==max_demand]['hour']
                peak_day_max_demand = predictions_zone[predictions_zone['pred']==max_demand]['datetime']
                stations_postal_code = df_stations[df_stations['postal_code'] == postal_code]
            if visualization == "All stations" and model != "Compare models":
                peak_hour_demand = predictions_global_show[predictions_global_show['pred']==max_demand]['hour']
                peak_day_max_demand = predictions_global_show[predictions_global_show['pred']==max_demand]['datetime']
                stations_postal_code = df_stations    
            
            if model == "Compare models" and visualization == "All stations":
                st.dataframe(evaluation_models[['model', 'MSE', 'MAE', 'RMSE','R2']])                                                                       
            if model != "Compare models" :
                st.metric(label="Maximum demand", value = int(max_demand))
                st.metric(label="Total stations", value = stations_postal_code['id'].count())
                #col1, col2 =  st.columns(2)  
                #st.metric(label="Maximum demand hour", value = peak_hour_max_demand)
                st.metric(label="Day of maximum demand", value = str(peak_day_max_demand)[7:27])
            
                st.metric(label = "Total docks", value = stations_postal_code['total_bases'].sum())
                      
            
     
            
        with right_column:    
            st.subheader("Map with stations")
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
  
  average_demand_month = rides_per_hour[rides_per_hour['month'].isin(month)].groupby(['year']).mean().reset_index()
  average_demand_year = int(average_demand_month[average_demand_month['year'] == year]['rides'])
  
  average_demand_year_before = int(average_demand_month[average_demand_month['year'] == year - 1]['rides'])
  percentual_variation_demand_year = round(((average_demand_year - average_demand_year_before) / average_demand_year_before)*100,2)
  
  avg_rides_months = rides_per_hour[rides_per_hour['month'].isin(month)].groupby(['year', 'hour']).mean().reset_index()
  avg_rides_per_hour = avg_rides_months[avg_rides_months['year']==year]
  max_rides_id = avg_rides_per_hour['rides'].idxmax()
  max_rides = avg_rides_per_hour.loc[max_rides_id,'rides']
  peak_hour = avg_rides_per_hour.loc[max_rides_id,'hour']
  
  avg_rides_month_weekday = rides_per_hour[rides_per_hour['month'].isin(month)].groupby(['year','weekday']).mean().reset_index()
  avg_rides_day = avg_rides_month_weekday[avg_rides_month_weekday['year'] == year]
  max_demand = avg_rides_day['rides'].max()
  peak_day = avg_rides_day[avg_rides_day['rides']==max_demand]['weekday']
  peak_day = str(peak_day)[5:-29]
  available_docks = df_stations['total_bases'].sum()

  col1, col2, col3, col4 = st.columns(4)
  col1.metric(label="Avg. demand per hour", value = average_demand_year, delta = percentual_variation_demand_year)
  col2.metric(label="Peak hour demand", value = str(peak_hour) + " h")
  col3.metric(label = "Peak day demand", value = peak_day)
  col4.metric(label = "Nº of available docks", value = available_docks)
   
  with st.container():
     rides_per_hour_months=rides_per_hour[rides_per_hour['month'].isin(month)]
     st.subheader('Distribution of demand ')
     order = {"Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday": 6, "Sunday":7}
     col1, col2, col3, col4 = st.columns(4)
     with col1:
        x=st.radio('Period: ', ['per hour', 'per weekday'])
     with col2:
        y=st.radio('Plot: ', ['boxplot','lineplot'])
     if x == "per hour":
       
        if y == "boxplot":
                fig = px.box(rides_per_hour_months[rides_per_hour_months['year']==year], x= 'hour', y='rides', color='is_weekend')
        if y == "lineplot":
                rides_per_hour_lineplot = rides_per_hour_months.groupby(['is_weekend','hour','year'])['rides'].mean().reset_index()
                fig = px.line(rides_per_hour_lineplot[rides_per_hour_lineplot['year']==year], x='hour', y='rides', color='is_weekend', markers=True)
        fig.update_layout(
                showlegend = True,
                width = 1400,
                height = 400,
                margin = dict(l=1, r=1, b=1, t=1),
                font = dict(color = "#383635", size = 15)
                )
        st.write(fig)
     if x == "per weekday":
        if y == "boxplot":
                rides_per_hour_months['order'] = rides_per_hour_months['weekday'].map(order)
                rides_per_hour_months.sort_values(by='order', inplace=True)
                fig = px.box(rides_per_hour_months[rides_per_hour_months['year']==year], x= 'weekday', y='rides', color='is_weekend')
                
        if y == "lineplot":
                
                rides_per_weekday_lineplot = rides_per_hour_months.groupby(['weekday','year'])['rides'].mean().reset_index()
                rides_per_weekday_lineplot['order'] = rides_per_weekday_lineplot['weekday'].map(order)
                rides_per_weekday_lineplot.sort_values(by='order', inplace=True)
                fig = px.line(rides_per_weekday_lineplot[rides_per_weekday_lineplot['year']==year], x='weekday', y ='rides', markers = True)
        fig.update_layout(
                showlegend = True,
                width = 1400,
                height = 400,
                margin = dict(l=1, r=1, b=1, t=1),
                font = dict(color = "#383635", size = 15)
                )
        st.write(fig)

  with st.container():
     st.subheader('Evolution of demand in the selected year')
     rides_per_hour['datetime'] = pd.to_datetime(rides_per_hour['datetime'])
     rides_per_hour.sort_values(by='datetime', inplace=True)
     fig = px.line(rides_per_hour_months[rides_per_hour_months['year']==year], x = 'datetime', y ='rides')
     fig.update_layout(
                showlegend = True,
                width = 1400,
                height = 400,
                margin = dict(l=1, r=1, b=1, t=1),
                font = dict(color = "#383635", size = 15)
                )
     fig.update_xaxes(
             rangeslider_visible = True,
             rangeselector=dict(
                     buttons = list([
                             dict(count=1, label = "1d", step = "day", stepmode="backward"),
                             dict(count=1, label = "1m", step="month", stepmode="backward"),
                             dict(count=6, label = "6m", step = "month", stepmode = "backward"),
                             dict(step="all")])
                             ))
     st.write(fig)

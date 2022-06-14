# -*- coding: utf-8 -*-


import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
# import numpy as np
# import datetime
# import seaborn as sns
import plotly.graph_objects as go


st.set_page_config(layout="wide")
# Navigation menu
selected = option_menu(
        menu_title=None,
        options=["Prediction of demand", "Dashboard demand"],
        icons=["bar-chart-line", "bicycle"],
        orientation="horizontal")
#Creating the dataframes needed
df_stations = pd.read_csv("Frontend/stations_postal_code.csv")
predictions_total = pd.read_csv("Frontend/predictions_all_stations.csv")
predictions_per_zone = pd.read_csv("Frontend/predictions_per_zone.csv")
rides_per_hour = pd.read_csv("Frontend/movements_grouped.csv")
#Preparing the dataset rides_per_station_2021
rides_per_station_2021 = pd.read_csv("Frontend/rides_per_station_2021.zip")
rides_per_station_2021 = rides_per_station_2021.merge(df_stations, how='inner', left_on = 'id', right_on = 'id')
rides_per_station_2021['postal_code'] = rides_per_station_2021['postal_code_y']
rides_per_station_2021 = rides_per_station_2021[['postal_code', 'rides', 'weekday', 'month', 'year', 'day', 'hour','time', 'datetime']]
rides_per_station_2021 = rides_per_station_2021.groupby(['postal_code', 'weekday','month', 'year', 'day','hour', 'datetime', 'time'])['rides'].sum().reset_index()
#Preparing the dataset with models used
evaluation_models = pd.read_csv("Frontend/evaluation_models_global_demand.csv")
models_used = predictions_per_zone.groupby('postal_code').max().reset_index()
models_used = models_used[['postal_code', 'model']]
#Possible options for models
dict_models = {'RandomForest': 'Random Forest', 'Random Forest': 'Random Forest', 'Catboost': 'CatBoost', 'CatBoost': 'CatBoost', 
               'XGBoost': 'XGBoost', 'XGboost': 'XGBoost', 'Light GBM': 'Light GBM'
              }
#Apply dictionary to column models
models_used['model'].replace(dict_models, inplace=True)
#Dictionary to convert 1 and 0 in weekend and weekdays
is_weekend = {
        1: "Weekend",
        0: "Weekdays"}

is_weekend_2 = {
        "Monday": "Weekdays",
        "Tuesday": "Weekdays",
        "Wednesday": "Weekdays",
        "Thursday": "Weekdays",
        "Friday": "Weekdays",
        "Saturday": "Weekend",
        "Sunday": "Weekend"}
rides_per_hour['day_week'] = rides_per_hour['is_weekend'].map(is_weekend)
rides_per_station_2021['day_week'] = rides_per_station_2021['weekday'].map(is_weekend_2)
#######################################
# PREDICTIONS OF DEMAND VISUALIZATION #
#######################################

if selected == "Prediction of demand":

    scope = st.sidebar.radio('Period: ', ['next 24 hours', 'next 14 days'])

    visualization = st.sidebar.selectbox(
        "Select the type of visualization: ",
        ["All stations", "Demand per zones"])

    if visualization == "Demand per zones":
        postal_code = st.sidebar.selectbox(
            'Postal code',
            list(df_stations['postal_code'].unique()))
        model = "default"
        stations = st.sidebar.radio(
            'Comparison of all zones or individual zones: ',
            ['Individual zone', 'Comparison all zones'])
    elif visualization == "All stations":
        model = st.sidebar.radio(
            'Model:',
            ['Random Forest', 'XGBoost','Light GBM', 'Catboost', 'Compare models'])


    # Container 1 PREDICTIONS
    with st.container():

        if scope == 'next 14 days':
            st.header("Predictions for the next 14 days")

        elif scope == 'next 24 hours':
            st.header("Predictions for the next 24 hours")

        # ALL STATIONS VISUALIZATION
        if visualization == "All stations":

            if scope == "next 24 hours":
                predictions_global_show = predictions_total[
                    predictions_total['day'] == '2021-07-01']
            elif scope == "next 14 days":
                predictions_global_show = predictions_total

            if model == 'Compare models':

                fig = px.line(
                    predictions_global_show,
                    x='datetime',
                    y='pred', color='model')

                fig.update_layout(
                    showlegend=True,
                    width=1400,
                    height=400,
                    margin=dict(l=1, r=1, b=1, t=1),
                    font=dict(color="#383635", size=15)
                    )

                fig.update_xaxes(
                    rangeslider_visible=True,
                    rangeselector=dict(
                        buttons=list([dict(
                            count=1,
                            label="1d",
                            step="day",
                            stepmode="todate"),
                            dict(step="all")])))
                st.write(fig)

            else:

                predictions_global_final = predictions_global_show[
                    predictions_global_show['model'] == model]
                max_demand = predictions_global_final['pred'].max()
                predictions_global_max = predictions_global_final[
                    predictions_global_final['pred'] == max_demand]

                fig = px.line(
                    predictions_global_final,
                    x='datetime',
                    y='pred')

                fig.update_layout(
                    showlegend=False,
                    width=1400,
                    height=400,
                    margin=dict(l=1, r=1, b=1, t=1),
                    font=dict(color="#383635", size=15))

                fig.update_xaxes(
                    rangeslider_visible=True,
                    rangeselector=dict(
                        buttons=list([dict(
                            count=1,
                            label="1d",
                            step="day",
                            stepmode="todate"),
                            dict(step="all")])))

                st.write(fig)

        # DEMAND PER ZONE VISUALIZATION
        if visualization == "Demand per zones":

            if scope == 'next 24 hours':

                predictions_per_zone_show = predictions_per_zone[
                    predictions_per_zone['day'] == '2021-07-01']
         

            elif scope == 'next 14 days':

                predictions_per_zone_show = predictions_per_zone
            
            if stations == 'Comparison all zones':
                predictions_zone = predictions_per_zone_show
                max_demand = predictions_zone['pred'].max()
                predictions_zone_max = predictions_zone[predictions_zone['pred'] == max_demand]
            elif stations == 'Individual zone':
                predictions_zone = predictions_per_zone_show[
                predictions_per_zone_show['postal_code'] == postal_code]
                max_demand = predictions_zone['pred'].max()
                predictions_zone_max = predictions_zone[
                        predictions_zone['pred'] == max_demand]

            fig = px.line(predictions_zone, x='datetime', y='pred', color = 'postal_code')

            fig.update_layout(
                        showlegend=True,
                        width=1400,
                        height=400,
                        margin=dict(l=1, r=1, b=1, t=1),
                        font=dict(color="#383635", size=15)
                        )
            fig.update_xaxes(
                        rangeslider_visible=True,
                        rangeselector=dict(
                                buttons=list([dict(
                                    count=1,
                                    label="1d",
                                    step="day",
                                    stepmode="todate"),
                                    dict(step="all")])))

            st.write(fig)

        left_column, middle_column,right_column = st.columns(3)
        
        #MIDDLE SIDE VISUALIZATION
        with middle_column:
                st.subheader("Stations list")
                if visualization == "Demand per zones":
                     st.dataframe(data = df_stations[df_stations['postal_code] == postal_code]  ) 

        # LEFT SIDE VISUALIZATION
        with left_column:

            st.subheader("Some useful data")

            if visualization == "Demand per zones":

                peak_hour_max_demand = predictions_zone[
                    predictions_zone['pred'] == max_demand]['hour']

                peak_day_max_demand = predictions_zone[
                    predictions_zone['pred'] == max_demand]['datetime']

                stations_postal_code = df_stations[
                    df_stations['postal_code'] == postal_code]

            if visualization == "All stations" and model != "Compare models":

                peak_hour_demand = predictions_global_show[
                    predictions_global_show['pred'] == max_demand]['hour']

                peak_day_max_demand = predictions_global_show[
                    predictions_global_show['pred'] == max_demand]['datetime']

                stations_postal_code = df_stations

            if model == "Compare models" and visualization == "All stations":

                st.dataframe(
                    evaluation_models[['model', 'MSE', 'MAE', 'RMSE', 'R2']])

            if model != "Compare models":

                st.metric(label="Maximum demand", value=int(max_demand))
                st.metric(label="Total stations",
                          value=stations_postal_code['id'].count())
                # col1, col2 =  st.columns(2)
                # st.metric(label="Maximum demand hour", value = peak_hour_max_demand)
                st.metric(label="Day of maximum demand",
                          value=str(peak_day_max_demand)[7:27])

                st.metric(label="Total docks",
                          value=stations_postal_code['total_bases'].sum())

        # RIGHT SIDE VISUALIZATION
        with right_column:
            if visualization == "All stations" or stations == "Individual zone":

                st.subheader(" Map with stations")
                df_stations['lat'] = df_stations['latitude']
                df_stations['lon'] = df_stations['longitude']
                df_stations = df_stations[['lat', 'lon', 'postal_code']]

                if visualization == "Demand per zones":
                        st.map(df_stations[df_stations['postal_code'] == postal_code])

                if visualization == "All stations":

                        st.map(df_stations)
            else:
                st.subheader("Models used for predictions")
                labels = ["Random Forest", "XGBoost", "Catboost", "Light GBM", "XGboost", "Randomforest"]
                pie_chart = models_used.groupby('model').count().reset_index()
                fig = px.pie(pie_chart, values = 'postal_code', names = 'model', hover_name='model')
                fig.update_layout(
                        showlegend=True,
                        width=600,
                        height=400,
                        margin=dict(l=1, r=1, b=1, t=1),
                        font=dict(color="#383635", size=15)
                        )

                st.write(fig)
                

###########################
# DASHBOARD VISUALIZATION DEMAND #
###########################

if selected == "Dashboard demand":

    month_options = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"}

    year = st.sidebar.selectbox(
        "Select the year: ",
        [2021, 2020, 2019])

    month = st.sidebar.multiselect(
        "Select the month: ",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        format_func=lambda x: month_options.get(x))

    visualization = st.sidebar.selectbox(
        "Select the type of visualization: ",
        ["All stations", "Demand per zones"])
        
    if visualization == "Demand per zones":
        postal_code = st.sidebar.selectbox(
            'Postal code',
            list(df_stations['postal_code'].unique()))
        model = "default"


    # Average demand calculations
    if visualization == "All stations":    
        average_demand_month = rides_per_hour[
                rides_per_hour['month'].isin(month)].groupby(['year']).mean().reset_index()

        average_demand_year = int(
                average_demand_month[average_demand_month['year'] == year]['rides'])

        average_demand_year_before = int(
                average_demand_month[average_demand_month['year'] == year - 1]['rides'])
        percentual_variation_demand_year = round(
                ((average_demand_year - average_demand_year_before) / average_demand_year_before) * 100, 2)

        avg_rides_months = rides_per_hour[rides_per_hour['month'].isin(
                month)].groupby(['year', 'hour']).mean().reset_index()
        avg_rides_per_hour = avg_rides_months[avg_rides_months['year'] == year]
        max_rides_id = avg_rides_per_hour['rides'].idxmax()
        max_rides = avg_rides_per_hour.loc[max_rides_id, 'rides']
        peak_hour = avg_rides_per_hour.loc[max_rides_id, 'hour']

        avg_rides_month_weekday = rides_per_hour[rides_per_hour['month'].isin(
                month)].groupby(['year', 'weekday']).mean().reset_index()
        avg_rides_day = avg_rides_month_weekday[avg_rides_month_weekday['year'] == year]
        max_demand = avg_rides_day['rides'].max()
        peak_day = avg_rides_day[avg_rides_day['rides'] == max_demand]['weekday']
        peak_day = str(peak_day)[5:-29]
        available_docks = df_stations['total_bases'].sum()
      
    if visualization == "Demand per zones":
         rides_per_hour_station = rides_per_station_2021[rides_per_station_2021['postal_code'] == postal_code]
         average_demand_month = rides_per_hour_station[
                rides_per_hour_station['month'].isin(month)].groupby(['year']).mean().reset_index()

         average_demand_year = int(average_demand_month['rides'])
         #average_demand_year_before = int(average_demand_month[average_demand_month['year'] == year]['rides'])
         percentual_variation_demand_year = 0

         avg_rides_months = rides_per_hour_station[rides_per_hour_station['month'].isin(month)].groupby(['year', 'hour']).mean().reset_index()
         avg_rides_per_hour = avg_rides_months
         max_rides_id = avg_rides_per_hour['rides'].idxmax()
         max_rides = avg_rides_per_hour.loc[max_rides_id, 'rides']
         peak_hour = avg_rides_per_hour.loc[max_rides_id, 'hour']

         avg_rides_month_weekday = rides_per_hour_station[rides_per_hour_station['month'].isin(month)].groupby(['year', 'weekday']).mean().reset_index()
         avg_rides_day = avg_rides_month_weekday
         max_demand = avg_rides_day['rides'].max()
         peak_day = avg_rides_day[avg_rides_day['rides'] == max_demand]['weekday']
         peak_day = str(peak_day)[5:-29]
         df_docks = df_stations[df_stations['postal_code'] == postal_code]
         available_docks = df_docks['total_bases'].sum()       
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Avg. demand per hour",
        value=average_demand_year,
        delta=percentual_variation_demand_year)

    col2.metric(
        label="Peak hour demand",
        value=str(peak_hour) + " h")

    col3.metric(
        label="Peak day demand",
        value=peak_day)

    col4.metric(
        label="Nº of available docks",
        value=available_docks)

    # Container 2 PLOTS OF EVOLUTION OF DEMAND
    with st.container():
        if visualization == 'All stations':
                rides_per_hour_months = rides_per_hour[rides_per_hour['month'].isin(
                        month)]
        elif visualization == 'Demand per zones':
                rides_per_hour_months = rides_per_station_2021[rides_per_station_2021['postal_code'] == postal_code]
                rides_per_hour_months = rides_per_hour_months[rides_per_hour_months['month'].isin(month)]
        st.subheader('Distribution of demand ')

        order = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7}

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            x = st.radio('Period: ', ['per hour', 'per weekday'])

        with col2:
            y = st.radio('Plot: ', ['boxplot', 'lineplot'])

        if x == "per hour":
            if y == "boxplot":
                fig = px.box(
                    rides_per_hour_months[rides_per_hour_months['year'] == year],
                    x='hour',
                    y='rides',
                    color='day_week')

            elif y == "lineplot":
                rides_per_hour_lineplot = rides_per_hour_months.groupby(
                    ['day_week', 'hour', 'year'])['rides'].mean().reset_index()

                fig = px.line(
                    rides_per_hour_lineplot[rides_per_hour_lineplot['year'] == year],
                    x='hour',
                    y='rides',
                    color='day_week',
                    markers=True)

            fig.update_layout(
                    showlegend=True,
                    width=1400,
                    height=400,
                    margin=dict(l=1, r=1, b=1, t=1),
                    font=dict(color="#383635", size=15))

            st.write(fig)

        if x == "per weekday":
            if y == "boxplot":
                rides_per_hour_months['order'] = rides_per_hour_months['weekday'].map(
                    order)
                rides_per_hour_months.sort_values(by='order', inplace=True)

                fig = px.box(
                    rides_per_hour_months[
                        rides_per_hour_months['year'] == year],
                    x='weekday',
                    y='rides',
                    color='day_week')

            elif y == "lineplot":

                rides_per_weekday_lineplot = rides_per_hour_months.groupby(
                    ['weekday', 'year'])['rides'].mean().reset_index()
                rides_per_weekday_lineplot['order'] = rides_per_weekday_lineplot['weekday'].map(
                        order)
                rides_per_weekday_lineplot.sort_values(
                        by='order', inplace=True)

                fig = px.line(
                    rides_per_weekday_lineplot[
                        rides_per_weekday_lineplot['year'] == year],
                    x='weekday',
                    y='rides',
                    markers=True)

                fig.update_layout(
                    showlegend=True,
                    width=1400,
                    height=400,
                    margin=dict(l=1, r=1, b=1, t=1),
                    font=dict(color="#383635", size=15))

            st.write(fig)

    # Container 3 REPRESENTATION OF THE TIME SERIES
    with st.container():

        st.subheader('Evolution of demand in the selected year')
        rides_per_hour['datetime'] = pd.to_datetime(rides_per_hour['datetime'])
        rides_per_hour.sort_values(by='datetime', inplace=True)
        rides_per_hour_months['datetime'] = pd.to_datetime(rides_per_hour_months['datetime'])
        rides_per_hour_months.sort_values(by='datetime', inplace = True)

        fig = px.line(
            rides_per_hour_months[
                rides_per_hour_months['year'] == year],
            x='datetime',
            y='rides')

        fig.update_layout(
            showlegend=True,
            width=1400,
            height=400,
            margin=dict(l=1, r=1, b=1, t=1),
            font=dict(color="#383635", size=15))

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(
                        count=1,
                        label="1d",
                        step="day",
                        stepmode="backward"),
                    dict(
                        count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(
                        count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(
                        step="all")])))

        st.write(fig)

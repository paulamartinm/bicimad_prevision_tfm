# -*- coding: utf-8 -*-


import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
#Navigation menu
selected = option_menu(
        menu_title = None,
        options= ["Prediction of demand", "Dashboard"],
        icons = ["bar-chart-line", "bicycle"],
        orientation = "horizontal"
        
    )




df_stations = pd.read_csv("stations_final.csv")

if selected == "Prediction of demand":
    visualization = st.sidebar.selectbox("Select the type of visualization: ", ["All stations", "Demand per station"])
    if visualization == "Demand per station":
        postal_code = st.sidebar.selectbox('Postal code', list(df_stations['postal_code'].unique()))
    
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Demand prediction BICIMAD")
            
     
            
        with right_column:    
            df_stations['lat']= df_stations['latitude']
            df_stations['lon']=df_stations['longitude']
            df_stations = df_stations[['lat', 'lon', 'postal_code']]
            
            if visualization == "Demand per station":
                st.map(df_stations[df_stations['postal_code']==postal_code])
                
            if visualization == "All stations":
                
                st.map(df_stations)
                
          
        


    
     



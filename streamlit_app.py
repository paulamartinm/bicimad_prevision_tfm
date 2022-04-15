# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np

header = st.container()
part1 = st.container()
with header:
   st.set_page_config(page_title="Bicimad demand prediction", layout="wide")
   st.header("Demand prediction BICIMAD")

with part1:
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Evolution of the demand")
        
        #stations = st.selectbox('Select the zone: ', options = ['100','200'])
       
        
    with right_column:
        df = pd.read_csv("stations_final.csv")
        df['lat']= df['latitude']
        df['lon']=df['longitude']
        df = df[['lat', 'lon']]
        st.map(df)
     


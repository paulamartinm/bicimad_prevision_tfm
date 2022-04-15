# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Bicimad demand prediction", layout="wide")
st.header("Demand prediction BICIMAD")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Evolution of the demand 1")
        df = pd.read_csv("stations_final.csv")
        df['lat']= df['latitude']
        df['lon']=df['longitude']
        df = df[['lat', 'lon']]
        st.map(df)


# -*- coding: utf-8 -*-

import streamlit as st

st.set_page_config(page_title="Bicimad demand prediction", layout="wide")
st.header("Demand prediction BICIMAD")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Evolution of the demand")

                   

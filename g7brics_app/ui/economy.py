#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

import g7brics_config as config
import data_viz as viz 
 

def size(df, df_group, year, gdp_measure):
    if gdp_measure == config.GDP_MEASURE[0]:
        column = config.COLUMNS[7]
    else: 
        column = config.COLUMNS[1]

    with st.expander(f"🔢 GDP {gdp_measure}", expanded=True):
        
        tabs = st.tabs(config.TAB_OPTIONS + config.TAB_OPT_EXTRA)
    
        with tabs[0]:

            viz.stacked_bar(
                df_group, 
                column + " (%)", 
                "Percentage Share", 
                "%"
            )  

            viz.stacked_bar(
                df_group, 
                column, 
                "Total GDP", 
                "$"
            )  


        with tabs[1]:
            viz.group_pie(df_group, column, year) 

        with tabs[2]:
            viz.country_pie(df, year, column, dollar_sign=True)

        with tabs[3]:
            viz.sunburst(df, column, year, dollar_sign=True) 
            
        with tabs[4]:
            viz.treemap(df, column, year, dollar_sign=True)
             



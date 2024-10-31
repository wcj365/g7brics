#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

import g7brics_config as config
import data_viz as viz 
    

def population(df, df_group, year):   
    with st.container(border=True):
        tabs = st.tabs(config.TAB_OPTIONS + config.TAB_OPT_EXTRA)
        with tabs[0]:

            viz.stacked_bar(
                df_group, 
                config.COLUMNS[0] + " (%)", 
                "Percentage Share", 
                "%"
            )

            viz.stacked_bar(
                df_group, 
                config.COLUMNS[0], 
                "Total Population"
            )
           
        with tabs[1]:
            viz.group_pie(df_group, config.COLUMNS[0], year)

        with tabs[2]:
            viz.country_pie(df, year, config.COLUMNS[0])

        with tabs[3]:
            viz.sunburst(df, config.COLUMNS[0], year)
            
        with tabs[4]:
            viz.treemap(df, config.COLUMNS[0], year)

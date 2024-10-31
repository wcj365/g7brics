#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st


import g7brics_config as config
import data_viz as viz 
    

def health(df, df_group, year):
    with st.expander("🔢 Life Expentancy", expanded=True):

        tabs = st.tabs(config.TAB_OPTIONS)
        with tabs[0]:
            viz.stacked_bar(
                df_group, 
                config.COLUMNS[3], 
                "Life Expectancy",
            )  

        with tabs[1]:
            viz.group_bar(df_group, config.COLUMNS[3], year)

        with tabs[2]:
            df[config.COLUMNS[3]] = df[config.COLUMNS[3]].round(1) 
            viz.country_bar(df, config.COLUMNS[3], year)   

    with st.expander("🔢 Suicide Mortality", expanded=True):

        tabs = st.tabs(config.TAB_OPTIONS)
        with tabs[0]:
            viz.stacked_bar(
                df_group, 
                config.COLUMNS[4], 
                "Suicide Mortality"
            )  

        with tabs[1]:
            viz.group_bar(df_group, config.COLUMNS[4], year)
        with tabs[2]:
            df[config.COLUMNS[4]] = df[config.COLUMNS[4]].round(1) 
            viz.country_bar(df, config.COLUMNS[4], year)
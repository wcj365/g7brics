#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

import g7brics_config as config
import data_viz as viz 
 

def size(df, df_group, year):
    with st.expander(f"🔢 Millitary Expenditure", expanded=True):
        
        tabs = st.tabs(config.TAB_OPTIONS + [":sunny: Sun Burst", ":sunny: Tree Map"])

        with tabs[0]:
            viz.stacked_bar(
                df_group, 
                config.COLUMNS[5] + " (%)", 
                "Percentage Share", 
                "%"
            )          

            viz.stacked_bar(
                df_group, 
                config.COLUMNS[5], 
                "Total", 
                "$"
            )  

        with tabs[1]:
            viz.group_pie(df_group, config.COLUMNS[5], year)
            
        with tabs[2]:
            viz.country_pie(df, year, config.COLUMNS[5], dollar_sign=True)

        with tabs[3]:
            viz.sunburst(df, config.COLUMNS[5], year, dollar_sign=True)
            
        with tabs[4]:
            viz.treemap(df, config.COLUMNS[5], year, dollar_sign=True)           


def percent(df, df_group, year):

    with st.expander(f"🔢 Millitary Expenditure (% of GDP)", expanded=True):
        
        tabs = st.tabs(config.TAB_OPTIONS)

        with tabs[0]:

            viz.stacked_bar(
                df_group, 
                config.COLUMNS[6], 
                "", 
                "%"
            )  

        with tabs[1]:
            viz.group_bar(
                df_group, 
                config.COLUMNS[6], 
                year, 
                "%"
            )

        with tabs[2]:
            df[config.COLUMNS[6]] = df[config.COLUMNS[6]].round(1)
            viz.country_bar(
                df, 
                config.COLUMNS[6], 
                year, 
                "%"
            )
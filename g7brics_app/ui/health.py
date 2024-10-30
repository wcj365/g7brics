#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st


import g7brics_config as config
import data_viz as viz 
    

def health(df, df_group, year):
    with st.expander("🔢 Life Expentancy", expanded=True):
        title="Time Trend of Life Expentancy by G7 and BRICS"
        fig = viz.stacked_bar(df_group, config.COLUMNS[3], title)
        tabs = st.tabs(config.TAB_OPTIONS)
        with tabs[0]:
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")

        with tabs[1]:
            fig_bar = viz.group_bar(df_group, config.COLUMNS[3], year)
            st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit") 

        with tabs[2]:
            df[config.COLUMNS[3]] = df[config.COLUMNS[3]].round(1) 
            bar = viz.country_bar(df, config.COLUMNS[3], year)
            st.plotly_chart(bar, use_container_width=True, theme="streamlit")    

    with st.expander("🔢 Suicide Mortality", expanded=True):
        title="Time Trend of Suicide Mortality Rate by G7 and BRICS"
        fig = viz.stacked_bar(df_group, config.COLUMNS[4], title)
        tabs = st.tabs(config.TAB_OPTIONS)
        with tabs[0]:
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")

        with tabs[1]:
            fig_bar = viz.group_bar(df_group, config.COLUMNS[4], year)
            st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit") 

        df[config.COLUMNS[4]] = df[config.COLUMNS[4]].round(1) 
        bar = viz.country_bar(df, config.COLUMNS[4], year)
        st.plotly_chart(bar, use_container_width=True, theme="streamlit")    
 


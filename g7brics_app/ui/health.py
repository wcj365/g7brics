#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st


import g7brics_config as config
import dataviz_utils as viz 
    

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
            bars = viz.get_bar_charts(df, year, config.COLUMNS[3])
            columns = st.columns(2)
            with columns[0]:
                st.plotly_chart(bars[0], use_container_width=True, theme="streamlit")    
            with columns[1]:
                st.plotly_chart(bars[1], use_container_width=True, theme="streamlit") 
    with st.expander("🔢 Suicide Mortality", expanded=True):
        title="Time Trend of Suicide Mortality Rate by G7 and BRICS"
        fig = viz.stacked_bar(df_group, config.COLUMNS[4], title)
        tabs = st.tabs(config.TAB_OPTIONS)
        with tabs[0]:
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")

        with tabs[1]:
            fig_bar = viz.group_bar(df_group, config.COLUMNS[4], year)
            st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit") 

        bars = viz.get_bar_charts(df, year, config.COLUMNS[4])
        with tabs[2]:
            columns = st.columns(2)
            with columns[0]:
                st.plotly_chart(bars[0], use_container_width=True, theme="streamlit")    
            with columns[1]:
                st.plotly_chart(bars[1], use_container_width=True, theme="streamlit") 


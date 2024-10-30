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
        
        title = "Time Trend and Percentage Share of Global GDP by G7 and BRICS"
        fig_bar = viz.stacked_bar(df_group, column + " (%)", title)  
        fig_bar.update_traces(
            texttemplate='%{text}%', 
            textposition='inside'  
        )   

        tabs = st.tabs(config.TAB_OPTIONS + [":sunny: Sun Burst", ":sunny: Tree Map"])
        with tabs[0]:
            st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit") 

        fig_pie = viz.group_pie(df_group, column, year)
        with tabs[1]:
            st.plotly_chart(fig_pie, use_container_width=True, theme="streamlit") 

        pies = viz.country_pie(df, year, column, dollar_sign=True)
        with tabs[2]:
            columns = st.columns(2)      
            with columns[0]:
                st.plotly_chart(pies[0], use_container_width=True, theme="streamlit")    
            with columns[1]:
                st.plotly_chart(pies[1], use_container_width=True, theme="streamlit")   

        with tabs[3]:
            fig = viz.sunburst(df, column, year, dollar_sign=True)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit") 
            
        with tabs[4]:
            fig = viz.treemap(df, column, year, dollar_sign=True)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")             



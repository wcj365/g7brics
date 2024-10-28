#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

import g7brics_config as config
import dataviz_utils as viz 
    

def population(df, df_group, year):   
    with st.container(border=True):
        tabs = st.tabs(config.TAB_OPTIONS + [":sunny: Sun Burst", ":sunny: Tree Map"])
        with tabs[0]:
            title = "Time Trend and Percentage Share of World Population by G7 and BRICS"
            fig = viz.stacked_bar(df_group, config.COLUMNS[0] + " (%)", title)
            fig.update_traces(
                texttemplate='%{text}%',  
            )
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")  
           
        with tabs[1]:
            fig_pie = viz.group_pie(df_group, config.COLUMNS[0], year)
            st.plotly_chart(fig_pie, use_container_width=True, theme="streamlit") 

        with tabs[2]:
            pies = viz.get_pie_charts(df, year, config.COLUMNS[0])
            columns = st.columns(2)
            with columns[0]:
                st.plotly_chart(pies[0], use_container_width=True, theme="streamlit")    
            with columns[1]:
                st.plotly_chart(pies[1], use_container_width=True, theme="streamlit")   

        with tabs[3]:
            fig = viz.sunburst(df, config.COLUMNS[0], year)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit") 
            
        with tabs[4]:
            fig = viz.treemap(df, config.COLUMNS[0], year)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit") 
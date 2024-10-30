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
            title = "Time Trend and Percentage Share of Global Millitary Expenditure by G7 and BRICS"
            fig_bar = viz.stacked_bar(df_group, config.COLUMNS[5] + " (%)", title)  
            fig_bar.update_traces(
                texttemplate='%{text}%', 
                textposition='inside'  
            )   
            st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit") 

        with tabs[1]:
            fig_pie = viz.group_pie(df_group, config.COLUMNS[5], year)
            st.plotly_chart(fig_pie, use_container_width=True, theme="streamlit") 

        with tabs[2]:
            pies = viz.country_pie(df, year, config.COLUMNS[5], dollar_sign=True)
            columns = st.columns(2)      
            with columns[0]:
                st.plotly_chart(pies[0], use_container_width=True, theme="streamlit")    
            with columns[1]:
                st.plotly_chart(pies[1], use_container_width=True, theme="streamlit")   

        with tabs[3]:
            fig = viz.sunburst(df, config.COLUMNS[5], year, dollar_sign=True)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit") 
            
        with tabs[4]:
            fig = viz.treemap(df, config.COLUMNS[5], year, dollar_sign=True)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")             


def percent(df, df_group, year):

    with st.expander(f"🔢 Millitary Expenditure (% of GDP)", expanded=True):
        
        tabs = st.tabs(config.TAB_OPTIONS)

        with tabs[0]:
            title = "Time Trend and Percentage Share of Global Millitary Expenditure (% of GDP)"
            fig_bar = viz.stacked_bar(df_group, config.COLUMNS[6], title)  
            fig_bar.update_traces(
                texttemplate='%{text}%', 
                textposition='inside'  
            )   
            st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit") 

        with tabs[1]:
            fig_bar = viz.group_bar(df_group, config.COLUMNS[6], year, "%")
            st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit") 

        with tabs[2]:
            df[config.COLUMNS[6]] = df[config.COLUMNS[6]].round(1)
            bar = viz.country_bar(df, config.COLUMNS[6], year, "%")
            st.plotly_chart(bar, use_container_width=True, theme="streamlit")    
 

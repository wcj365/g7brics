#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

import g7brics_config as config
import dataviz_utils as viz 
 

def size(df, df_group, year):
    with st.expander(f"🔢 GDP", expanded=True):
        
        title = "Time Trend and Percentage Share of Global GDP by G7 and BRICS"
        fig_bar = viz.stacked_bar(df_group, config.COLUMNS[1] + " (%)", title)  
        fig_bar.update_traces(
            texttemplate='%{text}%', 
            textposition='inside'  
        )   

        tabs = st.tabs(config.TAB_OPTIONS + [":sunny: Sun Burst", ":sunny: Tree Map"])
        with tabs[0]:
            st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit") 

        fig_pie = viz.group_pie(df_group, config.COLUMNS[1], year)
        with tabs[1]:
            st.plotly_chart(fig_pie, use_container_width=True, theme="streamlit") 

        pies = viz.get_pie_charts(df, year, config.COLUMNS[1])
        with tabs[2]:
            columns = st.columns(2)      
            with columns[0]:
                st.plotly_chart(pies[0], use_container_width=True, theme="streamlit")    
            with columns[1]:
                st.plotly_chart(pies[1], use_container_width=True, theme="streamlit")   

        with tabs[3]:
            fig = viz.sunburst(df, config.COLUMNS[1], year, dollar_sign=True)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit") 
            
        with tabs[4]:
            fig = viz.treemap(df, config.COLUMNS[1], year, dollar_sign=True)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")             


def wealth(df, df_group, year):
    with st.expander(f"🔢 GDP Per Capita", expanded=True):
        tabs = st.tabs(config.TAB_OPTIONS)
        with tabs[0]:
            title="Time Trend GDP per Capita by G7 and BRICS"
            fig = viz.stacked_bar(df_group, config.COLUMNS[2], title)
            fig.update_traces(
                texttemplate='$%{text:,.0f}', 
                textposition='inside' 
            )

            st.plotly_chart(fig, use_container_width=True, theme="streamlit")


        with tabs[1]:
            fig_bar = viz.group_bar(df_group, config.COLUMNS[2], year, dollar_sign=True)
            st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit") 

        with tabs[2]:
            bars = viz.get_bar_charts(df, year, config.COLUMNS[2])
            columns = st.columns(2)
            with columns[0]:
                st.plotly_chart(bars[0], use_container_width=True, theme="streamlit")    
            with columns[1]:
                st.plotly_chart(bars[1], use_container_width=True, theme="streamlit") 

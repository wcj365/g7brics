#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

import g7brics_config as config
import data_viz as viz


def wealth(df, df_group, year, gdp_measure):
    if gdp_measure == config.GDP_MEASURE[0]:
        column = config.COLUMNS[8]
    else: 
        column = config.COLUMNS[2]

    with st.expander(f"🔢 GDP Per Capita {gdp_measure}", expanded=True):
        tabs = st.tabs(config.TAB_OPTIONS)
        with tabs[0]:
            title="Time Trend GDP per Capita by G7 and BRICS"
            fig = viz.stacked_bar(df_group, column, title)
            fig.update_traces(
                texttemplate='$%{text:,.0f}', 
                textposition='inside' 
            )

            st.plotly_chart(fig, use_container_width=True, theme="streamlit")


        with tabs[1]:
            fig_bar = viz.group_bar(df_group, column, year, "$")
            st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit") 

        with tabs[2]:
            bar = viz.country_bar(df, column, year, "$")
            st.plotly_chart(bar, use_container_width=True, theme="streamlit") 
       

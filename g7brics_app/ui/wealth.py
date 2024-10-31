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

            viz.stacked_bar(
                df_group, 
                column, 
                f"GDP Per Capita {gdp_measure}",
                "$"
            )  

        with tabs[1]:
            viz.group_bar(df_group, column, year, "$")

        with tabs[2]:
            viz.country_bar(df, column, year, "$")   
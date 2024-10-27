#/usr/local/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

import config




@st.cache_data
def get_pie_charts(df, year, column):
    figs = []
    for group in ["G7", "BRICS"]:
        fig = px.pie(     
            df[(df["Group"] == group) & (df["Year"] == year)],
            values=column,
            color="Country Code",
            hole=0.3,
            names="Country Name",
            title=f"{year} {group} {column}"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label+value')
        fig.update_layout(showlegend=False)
        figs.append(fig)
    return figs


@st.cache_data
def get_bar_charts(df, year, column):
    figs = []
    for group in ["G7", "BRICS"]:
        fig = px.bar(     
            df[(df["Group"] == group) & (df["Year"] == year)],
            x=column,
            color="Country Code",
            y="Country Name",
            title=f"{year} {group}"
        )
#        fig.update_traces(textposition='inside', textinfo='percent+label+value')
        fig.update_layout(
            showlegend=False,
            yaxis={'categoryorder':'total descending', "title":""}
        )
        figs.append(fig)
    return figs

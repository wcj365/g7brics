#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

import g7brics_config as config


def geography(df):
    df_2020 = df[(df["Group"].isin(["G7", "BRICS"])) & (df["Year"] == 2020)]
    fig = px.choropleth(  
        df_2020,
        locations='Country Code', 
        color='Group',
        scope="world",
        labels="Country Name",
        color_discrete_map=config.COLOR_MAP,
        featureidkey='properties.name',
    )
    ## Add labels on countries
    fig.add_scattergeo(
        locations=df_2020["Country Code"],
        text=df_2020['Country Name'],
        mode='text',
        textfont_color="black",
    #     textfont_style="bold",
        featureidkey='properties.name',
        showlegend=False
    )
    fig.update_geos(
        fitbounds='locations',
        oceancolor='blue'
    )
    fig.update_layout(legend=dict(
        yanchor="bottom",
        y=0.05,
        xanchor="center",
        x=0.5,
        orientation="h",
        title=None
    ))
    fig.update_layout(margin=dict(l=1, r=1, t=1, b=1))

    st.plotly_chart(fig, use_container_width=True, theme="streamlit") 
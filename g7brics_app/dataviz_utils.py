#/usr/local/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

import g7brics_config as config


def stacked_bar(df, column, title):
    fig = px.bar(
        df,
        x="Year",     
        y=column,      
        color="Group",
        text=column,
        color_discrete_map=config.COLOR_MAP,
        barmode="stack"
    )

    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            x=1,              # at the end of x
            xanchor="right",  # Anchor the legend's right
            yanchor="bottom", # Anchor the legend's bottom
            y=1.02,           # Slightly above the plot
            title_text=None
        )
    )

    return fig


def group_pie(df, column, year, dollar_sign=False):
    fig = px.pie(     
        df[df["Year"] == year],
        values=column,
        color="Group",
        hole=0.3,
        names="Group",
        color_discrete_map=config.COLOR_MAP,
        title=f"{year} {column}"
    )


    if dollar_sign:
        temp = '<b>%{label}</b><br>%{percent:.0%}<br>$%{value:,.0f}'
    else:
        temp = '<b>%{label}</b><br>%{percent:.0%}<br>%{value:,.0f}'

    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label+value',
        texttemplate='<b>%{label}</b><br>%{percent:.0%}<br>$%{value:,.0f}',   
        insidetextorientation='horizontal'  
    )
    fig.update_layout(showlegend=False)

    return fig


def group_bar(df, column, year, dollar_sign=False):
    fig = px.bar(     
        df[df["Year"] == year],
        x="Group",
        y=column,
        color="Group",
        text=column,
        color_discrete_map=config.COLOR_MAP,
        title=f"{year} {column}"
    )     
    fig.update_layout(
        showlegend=False,
        xaxis={'categoryorder': 'total descending'}
    )

    if dollar_sign:
        temp ='$%{text:,.0f}'
    else:
        temp = '%{text}'

    fig.update_traces(
        texttemplate=temp, 
        textposition='inside'  
    )

    return fig


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


def sunburst(df, column, year, dollar_sign=False):
    fig = px.sunburst(
        df[df["Year"] == year],      
        path=["Group", "Country Name"], 
        values=column,
        title=f"{year} {column}",
        color_discrete_map=config.COLOR_MAP
    )

    if dollar_sign:
        temp = '<b>%{label}</b><br>$%{value:,.0f}'
    else:
        temp = '<b>%{label}</b><br>%{value:,.0f}'

    fig.update_traces(
        textinfo="label+value",
        texttemplate=temp,  
    )

    return fig


def treemap(df, column, year, dollar_sign=False):

    fig = px.treemap(
        df[df["Year"] == year], 
        path=["Group", "Country Name"], 
        values=column
    )


    if dollar_sign:
        temp = '<b>%{label}</b><br>$%{value:,.0f}'
    else:
        temp = '<b>%{label}</b><br>%{value:,.0f}'

    fig.update_traces(
        textinfo="label+value",
        texttemplate=temp,  
    )

    return fig


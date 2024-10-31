#/usr/local/env python3

import uuid
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

import g7brics_config as config


PLOTLY_CONFIG = {'editable': True, 
                'edits' : {'titleText': True, 
                           "axisTitleText": True,
                           'annotationText' : True, 
                           'annotationPosition' : True,
                           "shapePosition": True,
                           'legendPosition' : True,
                           'legendText' : False},
            #    'modeBarButtonsToAdd':['drawline',
            #                           'drawopenpath',
            #                           'drawclosedpath',
            #                           'drawcircle',
            #                           'drawrect',
            #                           'eraseshape'],
               'toImageButtonOptions' : {'scale' : 2},
               'displaylogo': False,
               'modeBarButtonsToRemove': ['sendDataToCloud']
}   


def show(fig):
    st.plotly_chart(
        fig, 
        key=uuid.uuid4(),
        use_container_width=True, 
        theme="streamlit", 
        config=PLOTLY_CONFIG
)  


def stacked_bar(df, column, title, sign=None, barmode="stack", show_fig=True):
    fig = px.bar(
        df,
        title=title,
        x="Year",     
        y=column,      
        color="Group",
        text=column,
        color_discrete_map=config.COLOR_MAP,
        barmode=barmode
    )

    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            x=0.5,            # in the middle of x
            xanchor="center",  # Anchor the legend's center
            yanchor="bottom", # Anchor the legend's bottom
            y=1.05,           # Slightly above the plot
            title=None        
        )
    )

    if sign == "$":
        temp ='$%{text:,.0f}'
    elif sign == "%":
        temp ='%{text}%'
    else:
        temp = '%{text}'

    fig.update_traces(
        texttemplate=temp,  
    )

    if show_fig:
        show(fig)

    return fig


def group_pie(df, column, year, dollar_sign=False, show_fig=True):
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
        textposition='auto', 
        textinfo='percent+label+value',
        texttemplate=temp,   
        insidetextorientation='horizontal'  
    )

    fig.update_layout(showlegend=False)
   
    if show_fig:
        show(fig)

    return fig


def group_bar(df, column, year, sign=None, show_fig=True):
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

    if sign == "$":
        temp ='$%{text:,.0f}'
    elif sign == "%":
        temp ='%{text}%'
    else:
        temp = '%{text}'

    fig.update_traces(
        texttemplate=temp, 
        textposition='inside'  
    )
     
    if show_fig:
        show(fig)

    return fig


def country_bar(df, column, year, sign=None, show_fig=True):
    fig = px.bar(     
        df[df["Group"].isin(["G7", "BRICS"]) & (df["Year"] == year)],
        x="Country Name",
        y=column,
        color="Group",
        text=column,
        color_discrete_map=config.COLOR_MAP,
        title=f"{year} {column}"
    )     

    fig.update_layout(
        showlegend=True,
        xaxis={'categoryorder': 'total descending'}
    )

    if sign == "$":
        temp ='$%{text:,.0f}'
    elif sign == "%":
        temp ='%{text}%'
    else:
        temp = '%{text}'

    fig.update_traces(
        texttemplate=temp, 
        textposition='outside'  
    )

    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            x=1,              # at the end of x
            xanchor="right",  # Anchor the legend's right
            yanchor="bottom", # Anchor the legend's bottom
            y=1.05,           # Slightly above the plot
            title_text=None
        )
    )
  
    if show_fig:
        show(fig)

    return fig


@st.cache_data
def country_pie(df, year, column, dollar_sign=False, show_fig=True):
    figs = []
    for group in ["G7", "BRICS"]:
        fig = px.pie(     
            df[(df["Group"] == group) & (df["Year"] == year)],
            values=column,
            color="Country Code",
            hole=0.3,
            names="Country Name",
            title=f"{year} {group} {column}",
        )

        if dollar_sign:
            temp = '<b>%{label}</b><br>%{percent:.0%}<br>$%{value:,.0f}'
        else:
            temp = '<b>%{label}</b><br>%{percent:.0%}<br>%{value:,.0f}'

        fig.update_traces(
            textposition='auto', 
            textinfo='percent+label+value',
            texttemplate=temp,   
            insidetextorientation='horizontal'  
        )
        fig.update_layout(
            showlegend=False,
            yaxis=dict(
                automargin=True
            ),
            xaxis=dict(
                automargin=True
            ),
        )

        figs.append(fig)

    if show_fig:
        columns = st.columns(2)
        with columns[0]:
            show(figs[0])   
        with columns[1]:
            show(figs[1]) 

    return figs


def sunburst(df, column, year, dollar_sign=False, show_fig=True):
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
   
    if show_fig:
        show(fig)

    return fig


def treemap(df, column, year, dollar_sign=False, show_fig=True):

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
   
    if show_fig:
        show(fig)

    return fig
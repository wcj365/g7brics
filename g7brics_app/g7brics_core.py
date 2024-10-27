#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import streamlit as st

import config
import wdi_data
import viz_utils as viz 
    
    
@st.cache_data    
def prepare_data(lang):
    df = wdi_data.get_data(lang, config.INDICATORS, [], 2010, 2024)
    df = df.pivot(
        index=['Year', 'Country Code', 'Country Name', 'Region', 'Income Group', 'Lending Type'], 
        columns=["indicator"], 
        values="value"
    ).reset_index()

    df = df[df["Country Code"].isin(config.G7 + config.BRICS)]
    df = df.rename(columns=dict(zip(config.INDICATORS, config.COLUMNS)))
    df[config.COLUMNS[0]] = round(df[config.COLUMNS[0]] / 1000000, 2)
    df[config.COLUMNS[1]] = round(df[config.COLUMNS[1]] / 1000000000000, 2)
    df[config.COLUMNS[2]] = round(df[config.COLUMNS[2]], 2)
    df[config.COLUMNS[3]] = round(df[config.COLUMNS[3]], 2)
    df[config.COLUMNS[4]] = round(df[config.COLUMNS[4]], 2)

    def assign_group(row):
        if row["Country Code"] in config.G7:
            row["Group"] = "G7"
        elif row["Country Code"] in config.BRICS:
            row["Group"] = "BRICS"
        else:
            row["Group"] = "The Rest"
        return row

    df = df.apply(assign_group, axis=1)
    df_group = df.groupby(["Year", "Group"]).agg({
        config.COLUMNS[0] : "sum",
        config.COLUMNS[1] : "sum",
        config.COLUMNS[2] : "mean",
        config.COLUMNS[3] : "mean",
        config.COLUMNS[4] : "mean"
    }).reset_index()

    return df, df_group


def geography(df):
    df_2000 = df[df["Year"] == 2020]
    fig = px.choropleth(
        df_2000,
        locations='Country Code', 
        color='Group',
        scope="world",
        labels="Country Name",
        color_discrete_map=config.COLOR_MAP,
        featureidkey='properties.name',
    )
    ## Add labels on countries
    fig.add_scattergeo(
        locations=df_2000["Country Code"],
        text=df_2000['Country Name'],
        mode='text',
        textfont_color="black",
    #     textfont_style="bold",
        featureidkey='properties.name',
        showlegend=False
    )
    fig.update_geos(fitbounds='locations')
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


def population(df, df_group, year):
    with st.container(border=True):
        fig = px.bar(
            df_group,
            x="Year",     
            y=config.COLUMNS[0],       # population
            color="Group",
            color_discrete_map=config.COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")  

        pies = viz.get_pie_charts(df, year, config.COLUMNS[0])
        columns = st.columns(2)
        with columns[0]:
            st.plotly_chart(pies[0], use_container_width=True, theme="streamlit")    
        with columns[1]:
            st.plotly_chart(pies[1], use_container_width=True, theme="streamlit")   
            
        fig = px.sunburst(
            df[df["Year"] == year],      
            path=["Group", "Country Name"], 
            values=config.COLUMNS[0],
            title=f"{year} {config.COLUMNS[0]}",
            color_discrete_map=config.COLOR_MAP
        )
        fig.update_traces(textinfo="label+value")
        st.plotly_chart(fig, use_container_width=True, theme="streamlit") 
        
        fig = px.treemap(
            df[df["Year"] == year], 
            path=["Group", "Country Name"], 
            values=config.COLUMNS[0],
        )
        fig.update_traces(textinfo="label+value")

        st.plotly_chart(fig, use_container_width=True, theme="streamlit") 


def economy(df, df_group, year):
    with st.expander(f"🔢 GDP", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y=config.COLUMNS[1],      # GDP
            color="Group",
            color_discrete_map=config.COLOR_MAP,
            barmode="group"
        )   
        st.plotly_chart(fig, use_container_width=True, theme="streamlit") 

        pies = viz.get_pie_charts(df, year, config.COLUMNS[1])
        columns = st.columns(2)      
        with columns[0]:
            st.plotly_chart(pies[0], use_container_width=True, theme="streamlit")    
        with columns[1]:
            st.plotly_chart(pies[1], use_container_width=True, theme="streamlit")               
        
    with st.expander(f"🔢 GDP Per Capita", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y=config.COLUMNS[2],    # GDP per capita
            color="Group",
            color_discrete_map=config.COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        
        bars = viz.get_bar_charts(df, year, config.COLUMNS[2])
        columns = st.columns(2)
        with columns[0]:
            st.plotly_chart(bars[0], use_container_width=True, theme="streamlit")    
        with columns[1]:
            st.plotly_chart(bars[1], use_container_width=True, theme="streamlit") 


def health(df, df_group, year):
    with st.expander("🔢 Life Expentancy", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y=config.COLUMNS[3],
            color="Group",
            color_discrete_map=config.COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        
        bars = viz.get_bar_charts(df, year, config.COLUMNS[3])
        columns = st.columns(2)
        with columns[0]:
            st.plotly_chart(bars[0], use_container_width=True, theme="streamlit")    
        with columns[1]:
            st.plotly_chart(bars[1], use_container_width=True, theme="streamlit") 
    with st.expander("🔢 Suicidal Mortality", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y=config.COLUMNS[4],
            color="Group",
            color_discrete_map=config.COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        
        bars = viz.get_bar_charts(df, year, config.COLUMNS[4])
        columns = st.columns(2)
        with columns[0]:
            st.plotly_chart(bars[0], use_container_width=True, theme="streamlit")    
        with columns[1]:
            st.plotly_chart(bars[1], use_container_width=True, theme="streamlit") 


def data(df, df_group):
    with st.expander("🔢 Data", expanded=True):
        tabs = st.tabs([":sunny: Individual Countries", ":sunny: G7 vs BRICS"])
        with tabs[0]:
            st.dataframe(df, use_container_width=True)
        with tabs[1]:
            st.dataframe(df_group, use_container_width=True)

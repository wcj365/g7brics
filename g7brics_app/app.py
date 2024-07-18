#!/usr/bin/env python3

import pandas as pd

# This is a workaround to eliminate the error: 
# AttributeError: ‘DataFrame’ object has no attribute ‘iterItems’
# The strange thing is this error only occurs when dlpoying the app in Domin. 
# It does not appear when running the app in a workspace using the same environment:
# 5.7 Domino Standard Environment Py3.9 R4.3.1
pd.DataFrame.iteritems = pd.DataFrame.items

import plotly.express as px
import streamlit as st
  
G7 = [
    "USA",
    "CAN",
    "GBR",
    "DEU",
    "FRA",
    "ITA",
    "JPN"
]

BRICS = [
    "BRA",
    "RUS",
    "IND",
    "CHN",
    "ZAF"
]

COLOR_MAP = {
    "G7" : "#19D3F3",
    "BRICS" : "gold"   #"gold"
}


INDICATORS = [
    "SP.POP.TOTL",
    "NY.GDP.MKTP.PP.CD",
    "NY.GDP.PCAP.PP.CD",
    "SP.DYN.LE00.IN",
    "SH.STA.SUIC.P5"
]

COLUMNS = [
    "Population (Millions)",
    "GDP PPP ($Trillions)",
    "GDP Per Capita PPP ($)",
    "Life Expectancy at Birth (Years)",
    "Suicide Mortality Rate (Per 100K People)"
]
    
    
@st.cache_data    
def prepare_data():
    df = pd.read_csv("wdx_wide.csv")
    df = df[df["Country Code"].isin(G7 + BRICS)]
    df = df.rename(columns=dict(zip(INDICATORS, COLUMNS)))
    df[COLUMNS[0]] = round(df[COLUMNS[0]] / 1000000, 2)
    df[COLUMNS[1]] = round(df[COLUMNS[1]] / 1000000000000, 2)
    df[COLUMNS[2]] = round(df[COLUMNS[2]], 2)
    df[COLUMNS[3]] = round(df[COLUMNS[3]], 2)
    df[COLUMNS[4]] = round(df[COLUMNS[4]], 2)

    def assign_group(row):
        if row["Country Code"] in G7:
            row["Group"] = "G7"
        elif row["Country Code"] in BRICS:
            row["Group"] = "BRICS"
        else:
            row["Group"] = "The Rest"
        return row

    df = df.apply(assign_group, axis=1)
    df_group = df.groupby(["Year", "Group"]).agg({
        COLUMNS[0] : "sum",
        COLUMNS[1] : "sum",
        COLUMNS[2] : "mean",
        COLUMNS[3] : "mean",
        COLUMNS[4] : "mean"
    }).reset_index()

    
    return df, df_group


@st.cache_data
def geography(df):
    df_2000 = df[df["Year"] == 2000]
    fig = px.choropleth(
        df_2000,
        locations='Country Code', 
        color='Group',
        scope="world",
        labels="Country Name",
        color_discrete_map=COLOR_MAP,
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
        y=0.01,
        xanchor="center",
        x=0.5,
        orientation="h",
        title=None
    ))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    
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



st.sidebar.title('G7 vs BRICS')

df, df_group = prepare_data()

options = ["Geography", "Population", "Economy", "Health", "Data"]
option = st.sidebar.radio("", options, index=0, label_visibility="collapsed")
years = df["Year"].unique()
years.sort()
year = st.sidebar.slider("Year", years[0], years[-1])
st.subheader(option)

if option == options[0]:
    with st.container(border=True):
        fig = geography(df)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit") 
elif option == options[1]:  
    with st.container(border=True):
        fig = px.bar(
            df_group,
            x="Year",     
            y=COLUMNS[0],       # population
            color="Group",
            color_discrete_map=COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")  

        pies = get_pie_charts(df, year, COLUMNS[0])
        columns = st.columns(2)
        with columns[0]:
            st.plotly_chart(pies[0], use_container_width=True, theme="streamlit")    
        with columns[1]:
            st.plotly_chart(pies[1], use_container_width=True, theme="streamlit")   
            
        fig = px.sunburst(
            df[df["Year"] == year],      
            path=["Group", "Country Name"], 
            values=COLUMNS[0],
            title=f"{year} {COLUMNS[0]}",
            color_discrete_map=COLOR_MAP
        )
        fig.update_traces(textinfo="label+value")
        st.plotly_chart(fig, use_container_width=True, theme="streamlit") 
        
        fig = px.treemap(
            df[df["Year"] == year], 
            path=["Group", "Country Name"], 
            values=COLUMNS[0],
        )
        fig.update_traces(textinfo="label+value")

        st.plotly_chart(fig, use_container_width=True, theme="streamlit") 

elif option == options[2]:
    with st.expander(f"🔢 GDP", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y=COLUMNS[1],      # GDP
            color="Group",
            color_discrete_map=COLOR_MAP,
            barmode="group"
        )   
        st.plotly_chart(fig, use_container_width=True, theme="streamlit") 

        pies = get_pie_charts(df, year, COLUMNS[1])
        columns = st.columns(2)      
        with columns[0]:
            st.plotly_chart(pies[0], use_container_width=True, theme="streamlit")    
        with columns[1]:
            st.plotly_chart(pies[1], use_container_width=True, theme="streamlit")               
        
    with st.expander(f"🔢 GDP Per Capita", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y=COLUMNS[2],    # GDP per capita
            color="Group",
            color_discrete_map=COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        
        bars = get_bar_charts(df, year, COLUMNS[2])
        columns = st.columns(2)
        with columns[0]:
            st.plotly_chart(bars[0], use_container_width=True, theme="streamlit")    
        with columns[1]:
            st.plotly_chart(bars[1], use_container_width=True, theme="streamlit") 
        
elif option == options[3]:
    with st.expander("🔢 Life Expentancy", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y=COLUMNS[3],
            color="Group",
            color_discrete_map=COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        
        bars = get_bar_charts(df, year, COLUMNS[3])
        columns = st.columns(2)
        with columns[0]:
            st.plotly_chart(bars[0], use_container_width=True, theme="streamlit")    
        with columns[1]:
            st.plotly_chart(bars[1], use_container_width=True, theme="streamlit") 
    with st.expander("🔢 Suicidal Mortality", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y=COLUMNS[4],
            color="Group",
            color_discrete_map=COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        
        bars = get_bar_charts(df, year, COLUMNS[4])
        columns = st.columns(2)
        with columns[0]:
            st.plotly_chart(bars[0], use_container_width=True, theme="streamlit")    
        with columns[1]:
            st.plotly_chart(bars[1], use_container_width=True, theme="streamlit") 
            
else:
    with st.expander("🔢 Data", expanded=True):
        st.dataframe(df)
        st.dataframe(df_group)




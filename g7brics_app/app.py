#!/usr/bin/env python3

import pandas as pd
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
    "BRICS" : "gold" 
}

@st.cache_data    
def prepare_data():
    df = pd.read_csv("wdx_wide.csv")
    df = df[df["Country Code"].isin(G7 + BRICS)]

    def assign_group(row):
        if row["Country Code"] in G7:
            row["Group"] = "G7"
        elif row["Country Code"] in BRICS:
            row["Group"] = "BRICS"
        else:
            row["Group"] = "The Rest"
        return row

    df = df.apply(assign_group, axis=1)
    df_group = df.groupby(["Year", "Group"]).agg(
        GDP=("NY.GDP.MKTP.PP.CD", "sum"),
        GDP_PCAP=("NY.GDP.PCAP.PP.CD", "mean"),
        POP=("SP.POP.TOTL", "sum"),
        LIFE=("SP.DYN.LE00.IN", "mean"),
        SUICIDE=("SH.STA.SUIC.P5", "mean")
    ).reset_index()

    df_group["GDP PPP (Trillions $)"] = round(df_group["GDP"] / 1000000000000, 2)
    df_group["GDP Per Capita PPP ($)"] = round(df_group["GDP_PCAP"], 2)
    df_group["Population (Billions)"] = round(df_group["POP"] / 1000000000, 2)
    df_group["Life Expectancy (Years)"] = round(df_group["LIFE"], 2)
    df_group["Suicide Mortality Rate (Per 100k People)"] = round(df_group["SUICIDE"], 2)

    df_2000 = df[df["Year"] == 2000]
    
    return df_group, df_2000


@st.cache_data
def geography(df_2000):
    
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


st.set_page_config(
    page_title='_Streamlit_ is :blue[cool] :sunglasses:',
#    page_icon=page_icon,
    layout="wide",
    menu_items={
        "About": "G7 vs BRICS",
        "Get Help": "mailto:wangc1@gao.gov",
    },
)

st.sidebar.title('G7 vs BRICS')
#st.title('_Streamlit_ is :blue[cool] :sunglasses:')

df_group, df_2000 = prepare_data()

options = ["Geography", "Population", "Economy", "Health"]
option = st.sidebar.radio("", options, index=0, label_visibility="collapsed")
st.subheader(option)

if option == options[0]:
    fig = geography(df_2000)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit") 
elif option == options[1]:  
    with st.container(border=True):
        fig = px.bar(
            df_group,
            x="Year",
            y="Population (Billions)",
            color="Group",
            color_discrete_map=COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")    
elif option == options[2]:
    with st.expander(f"🔢 GDP", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y="GDP PPP (Trillions $)",
            color="Group",
            color_discrete_map=COLOR_MAP,
            barmode="group"
        )   
        st.plotly_chart(fig, use_container_width=True, theme="streamlit") 

    with st.expander(f"🔢 GDP Per Capita", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y="GDP Per Capita PPP ($)",
            color="Group",
            color_discrete_map=COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
else:
    with st.expander("🔢 Life Expentancy", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y="Life Expectancy (Years)",
            color="Group",
            color_discrete_map=COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    with st.expander("🔢 Suicidal Mortality", expanded=True):
        fig = px.bar(
            df_group,
            x="Year",
            y="Suicide Mortality Rate (Per 100k People)",
            color="Group",
            color_discrete_map=COLOR_MAP,
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

        

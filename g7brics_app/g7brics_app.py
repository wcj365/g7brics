#!/usr/bin/env python3

import streamlit as st

import config
import g7brics_core as core
    

st.set_page_config(
    page_title='G7 vs BRICS',
 #   page_icon=page_icon,
    layout="wide",
    menu_items={
        "About": "G7 vs BRICS 1.0",
        "Get Help": "mailto:wcj365@gmail.com",
    },
)

st.sidebar.title('G7 vs BRICS')
lang = st.sidebar.selectbox("Language", config.LANGUAGES.keys())
df, df_group = core.prepare_data(config.LANGUAGES[lang])
TOPICS = ["Geography", "Population", "Economy", "Health", "Data"]
topic = st.sidebar.selectbox("Topic", TOPICS, index=0)
years = list(df["Year"].unique())
years.sort(reverse=True)
year = st.sidebar.selectbox("Year", years)
st.subheader(topic)

if topic == TOPICS[0]:
    core.geography(df)
elif topic == TOPICS[1]:  
    core.population(df, df_group, year)
elif topic == TOPICS[2]:
    core.economy(df, df_group, year)           
elif topic == TOPICS[3]:
    core.health(df, df_group, year)           
else:
    core.data(df, df_group)



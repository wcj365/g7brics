#!/usr/bin/env python3

import streamlit as st


import g7brics_config as config
import data_prep as prep
from ui import geography as geo
from ui import population as pop
from ui import economy as econ
from ui import defense
from ui import wealth
from ui import health
from ui import data
    

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
#lang = st.sidebar.selectbox("Language", config.LANGUAGES.keys())
lang="English"
BRICS_OPTIONS = [
    "Original Members (5)",
    "All Members (5 + 4)",
#    "Members (9) & Partners (13)"
]
brics_option = st.sidebar.selectbox("BRICS Countries", BRICS_OPTIONS, index=0)
if brics_option == BRICS_OPTIONS[0]:
    brics = config.FOUNDERS
elif brics_option == BRICS_OPTIONS[1]:
    brics = config.FOUNDERS + config.ADDITIONS
else:
    brics = config.FOUNDERS + config.ADDITIONS + config.PARTNERS

df, df_group = prep.prepare_data(config.LANGUAGES[lang], brics)
topic = st.sidebar.selectbox("Topic", config.TOPICS, index=0)
if topic in [config.TOPICS[2], config.TOPICS[4]]:
    gdp = st.sidebar.selectbox("GDP Measure", config.GDP_MEASURE)
years = list(df["Year"].unique())
years.sort(reverse=True)
year = st.sidebar.selectbox("Year", years)
st.subheader(topic)
    
if topic == config.TOPICS[0]:
    geo.geography(df)
elif topic == config.TOPICS[1]:  
    pop.population(df, df_group, year)
elif topic == config.TOPICS[2]:
    econ.size(df, df_group, year, gdp)  
elif topic == config.TOPICS[3]:
    defense.size(df, df_group, year)  
    defense.percent(df, df_group, year) 
elif topic == config.TOPICS[4]:
    wealth.wealth(df, df_group, year, gdp)          
elif topic == config.TOPICS[5]:
    health.health(df, df_group, year)           
else:
    data.display(df, df_group)



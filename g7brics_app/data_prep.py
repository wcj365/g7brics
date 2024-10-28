#!/usr/bin/env python3

import pandas as pd
import streamlit as st

import g7brics_config as config
import wdi_data
  
    
@st.cache_data    
def prepare_data(lang):
    df = wdi_data.get_data(lang, config.INDICATORS, [],2000, 2024)
    df = df.pivot(
        index=['Year', 'Country Code', 'Country Name', 'Region', 'Income Group', 'Lending Type'], 
        columns=["indicator"], 
        values="value"
    ).reset_index()

    #df = df[df["Country Code"].isin(config.G7 + config.BRICS)]
    df = df.rename(columns=dict(zip(config.INDICATORS, config.COLUMNS)))
    df[config.COLUMNS[0]] = df[config.COLUMNS[0]] / 1000000       # Population in millions
    df[config.COLUMNS[1]] = df[config.COLUMNS[1]] / 1000000000 # GDP in billions


    def assign_group(row):
        if row["Country Code"] in config.G7:
            row["Group"] = "G7"
        elif row["Country Code"] in config.BRICS:
            row["Group"] = "BRICS"
        else:
            row["Group"] = "REST OF WORLD"
        return row

    df = df.apply(assign_group, axis=1)

    df_group = df.groupby(["Year", "Group"]).agg({
        config.COLUMNS[0] : "sum",
        config.COLUMNS[1] : "sum",
        config.COLUMNS[2] : "mean",
        config.COLUMNS[3] : "mean",
        config.COLUMNS[4] : "mean"
    }).reset_index()

    def pop_pctg(row):
        pop_total = df_group[df_group["Year"] == row["Year"]][config.COLUMNS[0]].sum()
        gdp_total = df_group[df_group["Year"] == row["Year"]][config.COLUMNS[1]].sum()
        row[config.COLUMNS[0] + " (%)"] = round(100 * row[config.COLUMNS[0]] / pop_total, 1)
        row[config.COLUMNS[1] + " (%)"] = round(100 * row[config.COLUMNS[1]] / gdp_total, 1)
        return row

    df_group = df_group.apply(pop_pctg, axis=1)

    df_group[config.COLUMNS[0]] = round(df_group[config.COLUMNS[0]], 0)
    df_group[config.COLUMNS[1]] = round(df_group[config.COLUMNS[1]], 0)
    df_group[config.COLUMNS[2]] = round(df_group[config.COLUMNS[2]], 0)    # GDP per Capita
    df_group[config.COLUMNS[3]] = round(df_group[config.COLUMNS[3]], 1)    # Life expectancy
    df_group[config.COLUMNS[4]] = round(df_group[config.COLUMNS[4]], 0)

    return df, df_group

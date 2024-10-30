#!/usr/bin/env python3

import pandas as pd
import streamlit as st

import g7brics_config as config
import wdi_data
  
    
@st.cache_data    
def prepare_data(lang, brics):
    df = wdi_data.get_data(lang, config.INDICATORS, [],2000, 2024)
    df = df.pivot(
        index=['Year', 'Country Code', 'Country Name', 'Region', 'Income Group', 'Lending Type'], 
        columns=["indicator"], 
        values="value"
    ).reset_index()

    df = df.rename(columns=dict(zip(config.INDICATORS, config.COLUMNS)))
    df[config.COLUMNS[0]] = df[config.COLUMNS[0]] / 1000000       # Population in millions
    df[config.COLUMNS[1]] = df[config.COLUMNS[1]] / 1000000000 # GDP in billions
    df[config.COLUMNS[5]] = df[config.COLUMNS[5]] / 1000000       # Millitary expenditure in 
    df[config.COLUMNS[7]] = df[config.COLUMNS[7]] / 1000000000 # GDP in billions



    def assign_group(row):
        if row["Country Code"] in config.G7:
            row["Group"] = "G7"
        elif row["Country Code"] in brics:
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
        config.COLUMNS[4] : "mean",
        config.COLUMNS[5] : "sum",
        config.COLUMNS[7] : "sum",
        config.COLUMNS[8] : "mean"
    }).reset_index()

    def percent(row):
        pop_total = df_group[df_group["Year"] == row["Year"]][config.COLUMNS[0]].sum()
        gdp_ppp_total = df_group[df_group["Year"] == row["Year"]][config.COLUMNS[1]].sum()
        gdp_usd_total = df_group[df_group["Year"] == row["Year"]][config.COLUMNS[7]].sum()
        mil_total = df_group[df_group["Year"] == row["Year"]][config.COLUMNS[5]].sum()
        row[config.COLUMNS[0] + " (%)"] = round(100 * row[config.COLUMNS[0]] / pop_total, 1)
        row[config.COLUMNS[1] + " (%)"] = round(100 * row[config.COLUMNS[1]] / gdp_ppp_total, 1)
        row[config.COLUMNS[5] + " (%)"] = round(100 * row[config.COLUMNS[5]] / mil_total, 1)
        row[config.COLUMNS[6]] = round(100 * row[config.COLUMNS[5]] / row[config.COLUMNS[7]] / 1000, 1)
        row[config.COLUMNS[7] + " (%)"] = round(100 * row[config.COLUMNS[7]] / gdp_usd_total, 1)
        return row

    df_group = df_group.apply(percent, axis=1)

    df_group[config.COLUMNS[0]] = round(df_group[config.COLUMNS[0]], 0)
    df_group[config.COLUMNS[1]] = round(df_group[config.COLUMNS[1]], 0)
    df_group[config.COLUMNS[2]] = round(df_group[config.COLUMNS[2]], 0)    # GDP per Capita
    df_group[config.COLUMNS[3]] = round(df_group[config.COLUMNS[3]], 1)    # Life expectancy
    df_group[config.COLUMNS[4]] = round(df_group[config.COLUMNS[4]], 0)
    df_group[config.COLUMNS[5]] = round(df_group[config.COLUMNS[5]], 0)
    df_group[config.COLUMNS[6]] = round(df_group[config.COLUMNS[6]], 1)
    df_group[config.COLUMNS[7]] = round(df_group[config.COLUMNS[7]], 0)
    df_group[config.COLUMNS[8]] = round(df_group[config.COLUMNS[8]], 0)    # GDP per Capita

    return df, df_group

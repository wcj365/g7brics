#!/usr/bin/env python3

import streamlit as st


def display(df, df_group):
    with st.expander("🔢 Data", expanded=True):
        tabs = st.tabs([":sunny: Individual Countries", ":sunny: Aggregated"])
        with tabs[0]:
            st.dataframe(df, use_container_width=True)
        with tabs[1]:
            st.dataframe(df_group, use_container_width=True)

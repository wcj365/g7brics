#!/usr/bin/env bash

rsconnect deploy streamlit \
  --server https://posit-connect.gaoinnovations.gov/ \
  --api-key $POSIT_CONNECT_API_KEY   \
  --entrypoint app.py    \
  /home/wangc1/g7brics/g7brics_app

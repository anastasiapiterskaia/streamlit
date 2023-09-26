#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

st.write("""
### Reading info on our dataset
""")
st.write("""
#### head of data
""")
df=pd.read_csv('/Users/anastasiapiterskaa/Downloads/rest_data_us.csv')
st.table(df.head())


#Investigate the proportions of the various types of establishments. Plot a graph.
st.write("""
### Proportions of the various types of establishments
""")
grouped_est=df.groupby(['object_type'])['id'].nunique().reset_index()
st.table(grouped_est)


## showing how plotly works


import plotly.express as px

pie=px.pie(grouped_est, values=grouped_est.id, names=grouped_est.object_type)
st.plotly_chart(pie)



## filtering the data
st.write("""## 
         Block with Filtered Data
""")
st.text('You can filter the data however you want')


#creating options to choose from
rest_type=df['object_type'].unique() 
# create a parameter that is a final choice
make_choice = st.sidebar.selectbox('Select your establishment:', rest_type)



filtered_type=df[df.object_type==make_choice]
st.table(filtered_type)
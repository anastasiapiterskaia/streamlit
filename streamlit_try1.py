
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


import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px




fig3 = px.pie(grouped_est, values=grouped_est.id, names=grouped_est.object_type,
              color=grouped_est.object_type,
color_discrete_map={'Sendo':'cyan', 'Tiki':'royalblue','Shopee':'darkblue'})
fig3.update_layout(
title="<b> Split by establishment</b>")
st.plotly_chart(fig3)



#Investigate the proportions of chain and nonchain establishments. Plot a graph.
st.write("""
### Proportions of chain vs non_chain
""")
import matplotlib.pyplot as plt
chart_data = df.groupby(['chain'])['id'].nunique().reset_index()
chart_data['chain']=chart_data['chain'].apply(lambda x: 'Yes' if x==True else 'No')
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(chart_data['chain'], chart_data['id'], color ='maroon',
        width = 0.4)
 
st.pyplot(fig)

#Which type of establishment is typically a chain?
st.write("""
### Establishment split by chain/not chain
""")
import altair as alt
grouped_chain_type=df.groupby(['chain','object_type'])['id'].nunique().reset_index()

c=alt.Chart(grouped_chain_type).mark_bar().encode(
    x=alt.X('sum(id)', stack="normalize"),
    y='object_type',
    color='chain'
)

st.altair_chart(c, use_container_width=True)



#What characterizes chains: many establishments with a small number of seats 
#or a few establishments with a lot of seats?

st.write("""
### Scatter plot of number of restaurants vs seating for chain
""")

rest_grouped=df[df.chain==True].groupby(['object_name'])['number'].agg(['count','median']).reset_index()
rest_grouped.columns=['name','number','average_seating']



c = alt.Chart(rest_grouped).mark_circle(size=60).encode(
    x='average_seating',
    y='number',
    tooltip=['name', 'average_seating', 'number']
).interactive()

st.altair_chart(c, use_container_width=True)




#Determine the average number of seats for each type of restaurant. 
#On average, which type of restaurant has the greatest number of seats? 
#Plot graphs.
st.write("""
### Average seating per type
""")

seating_grouped=df.groupby(['object_type'])['number'].median().reset_index()



diction={'Bakery':'🎂','Fast Food':'🍔',
                           'Bar':'🍷','Cafe':'🍲','Pizza':'🍕',
                           'Restaurant':'🍽️'}
seating_grouped['emoji1'] =seating_grouped['object_type'].apply(lambda x: diction.get(x))


bar = alt.Chart(seating_grouped).mark_bar().encode(
    x='object_type',
    y='number',
    color='object_type',
    text='object_type'
).properties(
    width=alt.Step(40)  # controls width of bar.
)
text=alt.Chart(seating_grouped).mark_text(align='center',size=30).encode(
    x='object_type',
    y='number',
    text='emoji1',
    
).properties(width=1000, height=300)

c=bar+text
st.altair_chart(c)


## filtering the data

st.write("""## 
         Block with Filtered Data
""")

rest_type=df['object_type'].unique() 
make_choice = st.sidebar.selectbox('Select your establishment:', rest_type)

seating_range = st.slider(
     "Choose the seating",
     value=(10, 300))

actual_range=list(range(seating_range[0],seating_range[1]+1))




filtered_type=df[df.object_type==make_choice]
filtered_type=filtered_type[filtered_type.number.isin(list(actual_range))]

st.table(filtered_type)



@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

csv = convert_df(filtered_type)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='filtered_data.csv',
     mime='text/csv',)

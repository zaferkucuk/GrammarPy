import csv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

## add text
st.title('Penguins explorer')
## s.write()
##st.write('Demo app to try out 'code', _graphs_ and **more**!')

##st.header('The Data')
##df=pd.read_csv('../data/penguins_pimped.csv')
##dfimport streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

## add Text
st.title('Penguins explorer')
## s.write() army knife of streamlit, you can pass text, mark up, fstrings, etc
st.write('Demo app to try out `code`, _graphs_ and **more**!')

st.header('The Data')
df = pd.read_csv('../../data/penguins_pimped.csv')
# render data frames as tables by passing the whole df or with st.write
st.subheader('Complete data frame')
df

## Add iterative elements
st.sidebar.write('Iterative Elements')
species = st.sidebar.selectbox(
    'Filter by species',
    df['species'].unique()
)

df_species = df.loc[df['species'] == species, :]


if st.checkbox(f'Show small sample of selected species {species}'):
    st.subheader('Sample of the data')
    st.write(df_species.sample(15))

## Plots
st.header('Some plots')
st.subheader('Standard `matplotlib`/`seaborn`')
st.write('`seaborn` figure')
fig, ax = plt.subplots()
ax = sns.scatterplot(data = df_species, x = 'body_mass_g', y = 'flipper_length_mm', hue = 'sex')
sns.despine()
# works for pandas plots, plt., seaborn
st.pyplot(fig)
st.write('`pandas` figure')
fig, ax = plt.subplots()
ax = df.groupby('species')['island'].count().plot.bar()
sns.despine()
st.pyplot(fig)

st.subheader('Streamlit figure') #check the documentation for more
st.write('Pass fitting data to have the figure displayed')
st.write(df.groupby('species')['island'].count())
st.bar_chart(data = df.groupby('species')['island'].count())

st.subheader('Interactive plots with `plotly`')
fig = px.scatter(df,
                  x = 'bill_length_mm',
                  y = 'bill_depth_mm',
                  color = 'sex', 
                  hover_name = 'name', 
                  animation_frame= 'species', 
                  range_x = [30,65],
                  range_y = [10,25]
)

st.plotly_chart(fig)

## Maps
st.header('Maps')
st.write('Super easy maps with native `st.map`, works with a `lat` and `lon` column in your data frame')
st.map(df)
st.write('Plotly is also great for maps')
st.write('There\'s also the possibility to make more sophisticated ones with [`pydeck`](https://deckgl.readthedocs.io/en/latest/)')

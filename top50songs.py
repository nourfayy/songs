import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.title('Top 50 Songs of 2020 on Spotify')
st.image('https://storage.googleapis.com/pr-newsroom-wp/1/2020/03/Header.png')

st.markdown("""---""")

#Importing the Songs dataset
songs = pd.read_csv('Top2020.csv')

#Renaming columns and capitalizing first letter of each word in titles of columns
songs.columns = songs.columns.str.title()
songs2 = songs.rename(columns={'Bpm': 'Beats_Per_Minute', 'Nrgy': 'Energy', 'Dnce': 'Danceability', 'Db': 'Loudness', 'Live': 'Liveness', 'Val': 'Valence', 'Dur':'Duration', 'Acous': 'Acousticness', 'Spch':'Speechiness', 'Pop': 'Popularity'})
songs2.info()

#Identifying empty/null cells
songs2.isnull().sum()

#Checking if there are any duplicates
songs2.duplicated()

if st.checkbox('The Top 50 Songs of 2020 Dataset'):
    chart_data = songs2
    chart_data

st.header('2020s Favorite Song 🎶')
st.video('https://www.youtube.com/watch?v=4NRXx6U8ABQ')

st.markdown("""---""")

#Bar Plot – Danceability per Song
st.subheader('★ Bar Plot – Danceability per Song')
barplotdance = go.Figure(data=[go.Bar(x=songs2.Title, y=songs2.Danceability,)])
barplotdance.update_traces(marker_color='rgb(255,127,80)', marker_line_color='rgb(255,99,71)', marker_line_width=1.5, opacity=0.6)
barplotdance.update_layout(title_text='Danceability/Song')
st.plotly_chart(barplotdance)

#Bar Plot – Popularity vs. Danceability per Song
st.subheader('★ Bar Plot – Popularity vs. Danceability per Song')
barplotpop = px.bar(songs2, x='Popularity', y='Title', color='Danceability', title ='Popularity vs. Danceability')
st.plotly_chart(barplotpop)

#Histogram of # of Songs/Artist
st.subheader('★ Histogram of # of Songs/Artist') 
hist=px.histogram(data_frame=songs2, x='Artist', color_discrete_sequence=px.colors.colorbrewer.Set1, title = 'Number of Songs per Artist')
st.plotly_chart(hist)

#3D plot showing the position of each track according to Energy, Liveness and Acousticness
st.subheader('★ 3D plot showing the position of each track according to Energy, Liveness and Acousticness') 
threed = go.Figure(data = [go.Scatter3d(
    x = songs2['Energy'],
    y = songs2['Loudness'],
    z = songs2['Liveness'],
    text = songs2['Title'], 
    mode = 'markers',
    marker = dict(
    color = songs2['Popularity'],
    colorbar_title = 'Popularity',
    colorscale = 'sunset'
    )
)])

# Set variables and size
threed.update_layout(width=800, height=800, title = 'Energy, Liveness, Acousticness plot of Songs',
                  scene = dict(xaxis=dict(title='Energy'),
                               yaxis=dict(title='Liveness'),
                               zaxis=dict(title='Acousticness')
                               )
                 )

st.plotly_chart(threed)

#Features Correlation Matrix
st.subheader('★ Features Correlation Matrix') 
cr=songs2.corr(method='pearson')
cor= go.Figure(go.Heatmap(x=cr.columns, y=cr.columns, z=cr.values.tolist(), colorscale='sunset', zmin=-1, zmax=1))
st.plotly_chart(cor)

st.markdown("""---""")

st.title('Top 15 Songs of 2020')
#Top 15 songs
top_songs = songs2.head(15)

#Selectbox
option = st.selectbox(
    'Which song do you like best?',
     top_songs['Title'])

'You selected: ', option

#Bar Chart of Songs and Popularity: Bears Per Minute, Energy and Danceability
st.subheader('★ Bar Chart of Songs and Popularity: Bears Per Minute, Energy and Danceability') 
song_bpm = go.Bar(x=top_songs.Title,
                  y=top_songs.Beats_Per_Minute,
                  name='Beats Per Minute',
                  marker=dict(color='coral'))

song_energy = go.Bar(x=top_songs.Title,
                y=top_songs.Energy,
                name='Energy Per Song',
                marker=dict(color='lightsalmon'))

song_danceability = go.Bar(x=top_songs.Title,
                y=top_songs.Danceability,
                name='Danceability Per Song',
                marker=dict(color='MediumBlue'))

data = [song_bpm, song_energy, song_danceability]

layout = go.Layout(title="Top Songs 2020",
                xaxis=dict(title='Song'),
                yaxis=dict(title='scale'))

fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig)

#Scatter Plot – Popularity vs. Genre vs. Energy
st.subheader('★ Scatter Plot – Popularity vs. Genre vs. Energy')
scatter = px.scatter(top_songs, x='Title', y='Popularity', color='Top Genre', size='Energy', size_max=14, hover_name='Title', color_discrete_sequence=px.colors.sequential.Sunset)
st.plotly_chart(scatter)

#Pie Chart of Top Genres
st.subheader('★ Pie Chart of Top Genres')
fig = px.pie(top_songs, values = 'Popularity', names='Top Genre', hole = 0.3, color_discrete_sequence=px.colors.sequential.Sunset, title='Pie Chart of Top Genres')
fig.update_layout(annotations=[dict(text='Top Genre',font_size=20, showarrow=False)])
st.plotly_chart(fig)

#Histogram of Top Genres vs. Beats Per Minute and Popularity
st.subheader('★ Histogram of Top Genres vs. Beats Per Minute and Popularity')
fig = px.histogram(top_songs,
                   x="Popularity", y='Beats_Per_Minute',
                  opacity = 0.8,
                  title = 'Top Genres vs. Beats Per Minute and Popularity',
                  color = 'Top Genre', color_discrete_sequence=px.colors.sequential.Sunset)
st.plotly_chart(fig)

#Download dataset
@st.cache
def convert_df(songs):
     return songs.to_csv().encode('utf-8')

csv = convert_df(songs)

st.download_button(
     label="Download Songs data as CSV",
     data=csv,
     file_name='songs.csv',
     mime='text/csv',
 )

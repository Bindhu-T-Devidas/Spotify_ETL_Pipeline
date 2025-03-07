import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import streamlit as st
from PIL import Image

# Customizing the Streamlit theme
st.set_page_config(page_title="🎶 Music Data Dashboard 🎀", layout="wide")
#st.markdown("<style>div.stButton > button {background-color: pink;}</style>", unsafe_allow_html=True)



# Load data
album_df = pd.read_csv('/Users/bindudevidas/Spotify_DE/album_transformed_2024-11-04_04-21-16.csv')
artist_df = pd.read_csv('/Users/bindudevidas/Spotify_DE/artist_transformed_2024-11-04_04-21-16.csv')
songs_df = pd.read_csv('/Users/bindudevidas/Spotify_DE/songs_transformed_2024-11-04_04-21-16.csv')
image = Image.open('/Users/bindudevidas/Spotify_DE/image.png') 


# Convert date columns to datetime
album_df['album_release_date'] = pd.to_datetime(album_df['album_release_date'], errors='coerce')
songs_df['song_added'] = pd.to_datetime(songs_df['song_added'], errors='coerce')



# Title
st.title("🎶 Spotify Music Data Dashboard  ")
st.image(image, caption="Spotify Data ETL Pipeline on AWS", use_column_width=True)

st.markdown("""
## Welcome to our Dashboard! 🎶🌸

We collected data from the Spotify API and processed it using AWS services in an ETL (Extract, Transform, Load) workflow:

- **Extract**: We used AWS Lambda, triggered by Amazon CloudWatch, to extract data from Spotify and save it in Amazon S3 as raw data.
- **Transform**: Another AWS Lambda function transformed the raw data, which was then saved in Amazon S3 as structured data.
- **Load**: AWS Glue Crawlers and Data Catalog inferred the schema and made the data accessible for analysis. Finally, we used Amazon Athena to run SQL queries and perform data analytics.

""" )

# Key Insights with emojis
st.header("Key Insights 💖")
st.markdown("""
- **Total Albums**: 39 📀  
- **Average Tracks per Album**: ~9.2 🎶  
- **Total Unique Artists**: 51 🎤  
- **Total Songs**: 50 🎵  
- **Average Song Duration**: ~3.3 minutes ⏳  
- **Average Popularity Score**: 88.4 🌟  
""")

# Visualizations and Explanations

# Album Release Trend
st.markdown("#### Album Release Trend Over Time 📅")
album_df['release_year'] = album_df['album_release_date'].dt.year
album_release_trend = album_df['release_year'].value_counts().sort_index()
fig1 = px.line(x=album_release_trend.index, y=album_release_trend.values, labels={'x': 'Year', 'y': 'Albums Released'}, title="Album Releases Over Time 💽", line_shape="spline")
fig1.update_traces(line=dict(color="pink"))
st.plotly_chart(fig1)
st.markdown("""
**Explanation**: This line chart shows the number of albums released over time. Peaks in certain years may indicate increased artist activity or trends that prompted more album releases.
""")

# Song Popularity Distribution
st.markdown("#### Distribution of Song Popularity 🌟")
fig2 = px.histogram(songs_df, x='popularity', nbins=20, title="Distribution of Song Popularity 💫")
fig2.update_traces(marker_color="#ebdef0")
st.plotly_chart(fig2)
st.markdown("""
**Explanation**: This histogram displays the distribution of song popularity scores. Most songs have high popularity, clustering around 80-100, indicating a dataset of well-liked or popular songs.
""")

# Song Duration vs. Popularity
st.markdown("#### Song Duration vs. Popularity 🎼")
fig3 = px.scatter(songs_df, x='duration_ms', y='popularity', hover_data=['song_name'], labels={'duration_ms': 'Duration (ms)', 'popularity': 'Popularity'}, title='Song Duration vs Popularity 🕰️')
fig3.update_traces(marker=dict(color="mediumvioletred", size=10))
st.plotly_chart(fig3)
st.markdown("""
**Explanation**: This scatter plot shows the relationship between song duration and popularity. The near-zero correlation suggests that song length does not significantly impact popularity in this dataset.
""")

# Top 10 Prolific Artists by Song Count
st.markdown("#### Top 10 Prolific Artists by Song Count 👩‍🎤👨‍🎤")
prolific_artists = songs_df['artist_id'].value_counts().head(10).reset_index()
prolific_artists.columns = ['artist_id', 'song_count']
prolific_artists = prolific_artists.merge(artist_df[['artist_id', 'artist_name']], on='artist_id')
fig4 = px.bar(prolific_artists, x='artist_name', y='song_count', title='Top 10 Prolific Artists by Song Count 🎸', color_discrete_sequence=["#aed6f1"])
st.plotly_chart(fig4)
st.markdown("""
**Explanation**: This bar chart highlights the top 10 artists by song count. It shows which artists are the most productive in terms of song output within this dataset.
""")

# Average Popularity by Album
st.markdown("#### Top 10 Albums by Average Popularity 🎼")
avg_popularity_per_album = songs_df.groupby('album_id')['popularity'].mean().reset_index()
avg_popularity_per_album = avg_popularity_per_album.merge(album_df[['album_id', 'album_name']], on='album_id')
top_albums_popularity = avg_popularity_per_album.sort_values(by='popularity', ascending=False).head(10)
fig5 = px.bar(top_albums_popularity, x='album_name', y='popularity', title='Top 10 Albums by Average Popularity 🎵', color_discrete_sequence=["#DB7093"])
st.plotly_chart(fig5)
st.markdown("""
**Explanation**: This bar chart shows the top 10 albums with the highest average popularity scores, reflecting albums that consistently contain well-liked songs.
""")

# Song Duration Distribution
st.markdown("#### Song Duration Distribution ⏱️")
fig6 = px.histogram(songs_df, x='duration_ms', nbins=20, labels={'duration_ms': 'Duration (ms)'}, title="Song Duration Distribution ⏳")
fig6.update_traces(marker_color="#a2d9ce ")
st.plotly_chart(fig6)
st.markdown("""
**Explanation**: This histogram shows the distribution of song durations in milliseconds. Most songs range between 2 to 4 minutes, aligning with typical commercial music lengths.
""")

# Monthly Song Addition Trend - Bar Chart
st.markdown("#### Monthly Trend of Songs Added 📅")
songs_df['song_added_month'] = songs_df['song_added'].dt.to_period('M').dt.to_timestamp()
monthly_song_addition = songs_df['song_added_month'].value_counts().sort_index()
fig7 = px.bar(x=monthly_song_addition.index, y=monthly_song_addition.values, labels={'x': 'Month', 'y': 'Songs Added'}, title="Monthly Trend of Songs Added 🌷")
fig7.update_traces(marker_color="#DB7093")
st.plotly_chart(fig7)
st.markdown("""
**Explanation**: This bar chart shows the number of songs added each month, highlighting potential seasonal patterns in song releases.
""")

# Distribution of Average Artist Popularity
st.markdown("#### Distribution of Average Artist Popularity 🌸")
artist_popularity = songs_df.groupby('artist_id')['popularity'].mean().reset_index()
artist_popularity = artist_popularity.merge(artist_df[['artist_id', 'artist_name']], on='artist_id')
fig8 = px.histogram(artist_popularity, x='popularity', nbins=15, title="Distribution of Average Artist Popularity 🎤", color_discrete_sequence=["#FFB6C1"])
st.plotly_chart(fig8)
st.markdown("""
**Explanation**: This histogram displays the distribution of average popularity per artist. A high concentration of artists with high popularity suggests a dataset focused on well-received music.
""")

# Average Popularity by Release Year
st.markdown("#### Average Popularity by Release Year 🎼")
album_popularity = songs_df.merge(album_df[['album_id', 'album_release_date']], on='album_id')
album_popularity['release_year'] = album_popularity['album_release_date'].dt.year
average_popularity_by_year = album_popularity.groupby('release_year')['popularity'].mean()
fig10 = px.bar(x=average_popularity_by_year.index, y=average_popularity_by_year.values, labels={'x': 'Release Year', 'y': 'Average Popularity'}, title="Average Popularity by Release Year 🎀", color_discrete_sequence=["#e91e63"])
st.plotly_chart(fig10)
st.markdown("""
**Explanation**: This bar chart illustrates the average popularity of songs by release year, indicating stable reception of music over the years with slight variations.
""")

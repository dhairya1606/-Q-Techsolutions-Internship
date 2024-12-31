import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
data_path = 'C:\\Users\\dhairya\\OneDrive\\Documents\\8th Sem Internships\\QTechSolutions\\Task 3\\imdb_top_1000.csv'  # Replace with your CSV file path
data = pd.read_csv(data_path)

# Data Cleaning
data['Released_Year'] = pd.to_numeric(data['Released_Year'], errors='coerce')
data['Gross'] = data['Gross'].str.replace(',', '').str.extract('(\d+)').astype(float)
data['Runtime'] = data['Runtime'].str.replace(' min', '').astype(float)

# Streamlit Dashboard
st.title("IMDb Top Movies Dashboard")
st.image("https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg", width=200)

# Sidebar Filters
st.sidebar.markdown("""
## Welcome!
#### I welcome you all to the dashboard where the movies rated from IMDB are displayed according to thier Statistics.
###### - Dhairya Kalathia""")
st.sidebar.header("Filters")
year_filter = st.sidebar.slider(
    "Released Year", 
    int(data['Released_Year'].min()), 
    int(data['Released_Year'].max()),
    (1990, 2020)
)

genre_filter = st.sidebar.selectbox(
    "Genre", 
    options=["All"] + list(data['Genre'].unique()), 
    index=0
)

rating_filter = st.sidebar.slider(
    "IMDb Rating", 
    float(data['IMDB_Rating'].min()), 
    float(data['IMDB_Rating'].max()),
    (7.0, 9.5)
)

votes_filter = st.sidebar.slider(
    "Number of Votes", 
    int(data['No_of_Votes'].min()), 
    int(data['No_of_Votes'].max()),
    (50000, 2000000)
)

# Apply filters
filtered_data = data[
    (data['Released_Year'] >= year_filter[0]) & (data['Released_Year'] <= year_filter[1]) &
    ((data['Genre'] == genre_filter) | (genre_filter == "All")) &
    (data['IMDB_Rating'] >= rating_filter[0]) & (data['IMDB_Rating'] <= rating_filter[1]) &
    (data['No_of_Votes'] >= votes_filter[0]) & (data['No_of_Votes'] <= votes_filter[1])
]

# Top Movies Table
st.subheader("Top Movies")
st.dataframe(filtered_data[['Series_Title', 'Released_Year', 'IMDB_Rating', 'Gross', 'Director', 'Genre']]
             .sort_values(by='IMDB_Rating', ascending=False).head(10))

# Genre Popularity by Decade
st.subheader("Genre Popularity by Decade")
data['Decade'] = (data['Released_Year'] // 10) * 10
genre_decade = data.groupby(['Decade', 'Genre']).size().reset_index(name='Count')
fig_genre_decade = px.bar(genre_decade, x='Decade', y='Count', color='Genre', title="Genre Popularity by Decade")
st.plotly_chart(fig_genre_decade)

# Top Rated Movies by Genre
st.subheader("Top Rated Movies by Genre")
top_movies_by_genre = filtered_data.groupby('Genre').apply(lambda x: x.nlargest(1, 'IMDB_Rating')).reset_index(drop=True)
st.dataframe(top_movies_by_genre[['Series_Title', 'Genre', 'IMDB_Rating']])

# Line Chart: Trend of Movies Released Over the Years
st.subheader("Trend of Movies Released Over the Years")
movies_per_year = filtered_data['Released_Year'].value_counts().sort_index().reset_index()
movies_per_year.columns = ['Year', 'Count']
fig_line = px.line(movies_per_year, x='Year', y='Count', title="Movies Released Over the Years")
st.plotly_chart(fig_line)

# Movies with the Highest Votes
st.subheader("Movies with the Highest Votes")
highest_votes = filtered_data.nlargest(10, 'No_of_Votes')[['Series_Title', 'No_of_Votes', 'IMDB_Rating']]
st.dataframe(highest_votes)

# Genre Distribution
st.subheader("Movies by Genre")
genre_counts = filtered_data['Genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
fig_genre = px.bar(genre_counts, x='Genre', y='Count', title="Number of Movies by Genre")
st.plotly_chart(fig_genre)

# Scatter Plot: IMDb Rating vs Gross
st.subheader("IMDb Rating vs Gross Earnings")
fig_scatter = px.scatter(filtered_data, x='Gross', y='IMDB_Rating', size='No_of_Votes', color='Genre', 
                         title="IMDb Rating vs Gross Earnings", hover_data=['Series_Title'])
st.plotly_chart(fig_scatter)

# Runtime Distribution
st.subheader("Runtime Distribution (Pie Chart)")
runtime_bins = [0, 60, 90, 120, 150, 180, 240]
runtime_labels = ['< 1 hour', '1-1.5 hours', '1.5-2 hours', '2-2.5 hours', '2.5-3 hours', '> 3 hours']
filtered_data['Runtime_Category'] = pd.cut(filtered_data['Runtime'], bins=runtime_bins, labels=runtime_labels, right=False)
runtime_counts = filtered_data['Runtime_Category'].value_counts().reset_index()
runtime_counts.columns = ['Runtime Category', 'Count']
fig_runtime_pie = px.pie(runtime_counts, names='Runtime Category', values='Count', title="Runtime Distribution")
st.plotly_chart(fig_runtime_pie)

# Top Directors with Most Movies
st.subheader("Top Directors with Most Movies")
top_directors = filtered_data['Director'].value_counts().head(10).reset_index()
top_directors.columns = ['Director', 'Movie Count']
fig_directors = px.bar(top_directors, x='Director', y='Movie Count', title="Top Directors with Most Movies")
st.plotly_chart(fig_directors)

# Correlation Analysis
st.subheader("Correlation Analysis")
correlation = filtered_data[['IMDB_Rating', 'Gross', 'Runtime', 'No_of_Votes']].corr()
st.write("### Correlation Heatmap")
fig_corr, ax = plt.subplots()
sns.heatmap(correlation, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig_corr)

# Gross Earnings by Year
st.subheader("Gross Earnings by Year")
gross_by_year = filtered_data.groupby('Released_Year')['Gross'].sum().reset_index()
fig_gross = px.line(gross_by_year, x='Released_Year', y='Gross', title="Gross Earnings Over the Years")
st.plotly_chart(fig_gross)

# Save file as Python script
st.sidebar.info("Save this script as 'app.py' and run `streamlit run app.py` in your terminal.")

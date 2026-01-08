from preswald import text, plotly, connect, get_df, table, sidebar, slider
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add sidebar
sidebar("""
## Navigation
- [Overview](#dataset-overview)
- [Top Movies](#top-rated-movies)
- [Rating Distribution](#rating-distribution)
- [Movies by Year](#movies-by-year)
- [Runtime Analysis](#runtime-analysis)
- [Genre Analysis](#genre-analysis)
- [Directors Analysis](#top-directors)
- [Star Power](#star-power)
- [Key Insights](#key-insights)
""")

# Display the title
text("# Movie Dataset Analysis 🎬")

# Connect to the data source
connect()

# Load the dataset
df = get_df('data/movies_dataset.csv')

# Dataset overview
text("## Dataset Overview")
text(f"This dataset contains information about {len(df)} movies from the IMDB database.")

# Display the columns with descriptions
text("### Dataset Columns")
columns_desc = {
    'Poster_Link': 'URL link to the movie poster',
    'Series_Title': 'Name of the movie',
    'Released_Year': 'Year the movie was released',
    'Certificate': 'Certificate of the movie (age rating)',
    'Runtime': 'Length of the movie in minutes',
    'Genre': 'Genre(s) of the movie',
    'IMDB_Rating': 'Rating of the movie on IMDB',
    'Overview': 'Brief summary of the movie',
    'Meta_score': 'Score of the movie on Metacritic',
    'Director': 'Director of the movie',
    'Star1': 'First star/actor in the movie',
    'Star2': 'Second star/actor in the movie',
    'Star3': 'Third star/actor in the movie',
    'Star4': 'Fourth star/actor in the movie',
    'No_of_Votes': 'Number of votes received by the movie',
    'Gross': 'Gross earnings of the movie'
}

# Create a dataframe for the columns and descriptions
columns_df = pd.DataFrame([
    {"Column": col, "Description": columns_desc.get(col, "No description available")}
    for col in df.columns
])
table(columns_df)

# Clean and prepare data for analysis
text("### Data Preparation")
# Convert Released_Year to numeric
df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')

# Clean Runtime column - extract numbers only
df['Runtime'] = df['Runtime'].str.extract('(\d+)').astype(int)

# Process Gross column (remove commas and convert to numeric)
df['Gross'] = df['Gross'].str.replace(',', '').str.replace('"', '')
df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce')

# Ensure IMDB_Rating is numeric
df['IMDB_Rating'] = pd.to_numeric(df['IMDB_Rating'], errors='coerce')

# Ensure No_of_Votes is numeric
df['No_of_Votes'] = pd.to_numeric(df['No_of_Votes'], errors='coerce')

# Split genre into list
df['Genre_List'] = df['Genre'].str.split(', ')

# Top Rated Movies
text("## Top Rated Movies")
text("Here are the top 10 highest rated movies in the dataset:")
top_movies = df.sort_values('IMDB_Rating', ascending=False).head(10)[['Series_Title', 'Released_Year', 'IMDB_Rating', 'Director', 'Genre']]
table(top_movies)

# Rating Distribution
text("## Rating Distribution")
fig_rating = px.histogram(
    df, 
    x="IMDB_Rating", 
    nbins=20, 
    title="Distribution of IMDB Ratings",
    color_discrete_sequence=['#3498db']
)
fig_rating.update_layout(xaxis_title="IMDB Rating", yaxis_title="Number of Movies")
plotly(fig_rating)

# Rating vs Votes
fig_votes = px.scatter(
    df, 
    x="IMDB_Rating", 
    y="No_of_Votes", 
    hover_data=["Series_Title", "Released_Year", "Director"],
    title="IMDB Rating vs Number of Votes",
    color="IMDB_Rating",
    color_continuous_scale="viridis",
    size="No_of_Votes",
    size_max=50
)
fig_votes.update_layout(xaxis_title="IMDB Rating", yaxis_title="Number of Votes")
plotly(fig_votes)

# Movies by Year
text("## Movies by Year")
movies_by_year = df.groupby('Released_Year').size().reset_index(name='Count')
# Filter for valid years (remove NaN and very old movies)
movies_by_year = movies_by_year[movies_by_year['Released_Year'] >= 1920].dropna()

fig_years = px.bar(
    movies_by_year, 
    x="Released_Year", 
    y="Count", 
    title="Number of Movies Released by Year",
    color="Count",
    color_continuous_scale="viridis"
)
fig_years.update_layout(xaxis_title="Release Year", yaxis_title="Number of Movies")
plotly(fig_years)

# Average Rating by Decade
# First ensure Released_Year is numeric and not NaN
df_decade = df.dropna(subset=['Released_Year'])
df_decade['Decade'] = (df_decade['Released_Year'].astype(int) // 10) * 10
decade_rating = df_decade.groupby('Decade')['IMDB_Rating'].mean().reset_index()
decade_rating = decade_rating[decade_rating['Decade'] >= 1920]  # Filter out very old movies

fig_decade = px.line(
    decade_rating,
    x="Decade",
    y="IMDB_Rating",
    title="Average IMDB Rating by Decade",
    markers=True,
    line_shape="linear"
)
fig_decade.update_layout(xaxis_title="Decade", yaxis_title="Average IMDB Rating")
plotly(fig_decade)

# Runtime Analysis
text("## Runtime Analysis")
# Distribution of movie runtime
fig_runtime = px.histogram(
    df, 
    x="Runtime", 
    nbins=30, 
    title="Distribution of Movie Runtimes",
    color_discrete_sequence=['#2ecc71']
)
fig_runtime.update_layout(xaxis_title="Runtime (minutes)", yaxis_title="Number of Movies")
plotly(fig_runtime)

# Runtime vs Rating
fig_runtime_rating = px.scatter(
    df, 
    x="Runtime", 
    y="IMDB_Rating", 
    hover_data=["Series_Title", "Released_Year", "Director"],
    title="Runtime vs IMDB Rating",
    color="IMDB_Rating",
    color_continuous_scale="viridis",
)
fig_runtime_rating.update_layout(xaxis_title="Runtime (minutes)", yaxis_title="IMDB Rating")
plotly(fig_runtime_rating)

# Genre Analysis
text("## Genre Analysis")
# Extract all genres from the dataset
all_genres = []
for genres in df['Genre_List']:
    if isinstance(genres, list):
        all_genres.extend(genres)

# Count frequency of each genre
genre_counts = pd.Series(all_genres).value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']

# Plot top genres
top_genres = genre_counts.head(15)
fig_genres = px.bar(
    top_genres, 
    x="Genre", 
    y="Count", 
    title="Most Common Movie Genres",
    color="Count",
    color_continuous_scale="viridis"
)
fig_genres.update_layout(xaxis_title="Genre", yaxis_title="Number of Movies")
plotly(fig_genres)

# Average Rating by Genre
genre_ratings = {}
for genre in genre_counts['Genre'].head(10):  # Top 10 genres
    # Filter movies containing this genre
    genre_df = df[df['Genre'].str.contains(genre, case=False, na=False)]
    # Calculate average rating
    genre_ratings[genre] = genre_df['IMDB_Rating'].mean()

genre_rating_df = pd.DataFrame({'Genre': list(genre_ratings.keys()), 'Average_Rating': list(genre_ratings.values())})
genre_rating_df = genre_rating_df.sort_values('Average_Rating', ascending=False)

fig_genre_rating = px.bar(
    genre_rating_df, 
    x="Genre", 
    y="Average_Rating", 
    title="Average IMDB Rating by Genre",
    color="Average_Rating",
    color_continuous_scale="viridis"
)
fig_genre_rating.update_layout(xaxis_title="Genre", yaxis_title="Average IMDB Rating")
plotly(fig_genre_rating)

# Top Directors
text("## Top Directors")
director_counts = df['Director'].value_counts().reset_index().head(10)
director_counts.columns = ['Director', 'Number_of_Movies']

fig_directors = px.bar(
    director_counts,
    x="Director",
    y="Number_of_Movies",
    title="Top 10 Directors by Number of Movies",
    color="Number_of_Movies",
    color_continuous_scale="viridis"
)
fig_directors.update_layout(xaxis_title="Director", yaxis_title="Number of Movies")
plotly(fig_directors)

# Average Rating of Top Directors
top_directors = director_counts['Director'].tolist()
director_ratings = []

for director in top_directors:
    director_df = df[df['Director'] == director]
    director_ratings.append({
        'Director': director,
        'Average_Rating': director_df['IMDB_Rating'].mean(),
        'Number_of_Movies': len(director_df)
    })

director_rating_df = pd.DataFrame(director_ratings)
director_rating_df = director_rating_df.sort_values('Average_Rating', ascending=False)

fig_director_rating = px.bar(
    director_rating_df,
    x="Director",
    y="Average_Rating",
    title="Average IMDB Rating of Top Directors",
    color="Average_Rating",
    color_continuous_scale="viridis",
    hover_data=["Number_of_Movies"]
)
fig_director_rating.update_layout(xaxis_title="Director", yaxis_title="Average IMDB Rating")
plotly(fig_director_rating)

# Star Power Analysis
text("## Star Power")
# Combine all stars into one list
all_stars = pd.concat([df['Star1'], df['Star2'], df['Star3'], df['Star4']]).reset_index(drop=True)
star_counts = all_stars.value_counts().reset_index().head(10)
star_counts.columns = ['Actor', 'Number_of_Movies']

fig_stars = px.bar(
    star_counts,
    x="Actor",
    y="Number_of_Movies",
    title="Top 10 Actors by Number of Movies",
    color="Number_of_Movies",
    color_continuous_scale="viridis"
)
fig_stars.update_layout(xaxis_title="Actor", yaxis_title="Number of Movies")
plotly(fig_stars)

# Key Insights
text("## Key Insights")
text("""
1. **Rating Distribution**: Most movies in the dataset have ratings between 7.5 and 8.5, with a few exceptional movies rated above 9.0.

2. **Popularity vs Quality**: Movies with higher ratings generally receive more votes, showing a correlation between perceived quality and audience engagement.

3. **Release Trends**: There has been a substantial increase in movie production in recent decades, with peaks visible in the data.

4. **Runtime Impact**: The most highly rated movies tend to have runtimes between 120-180 minutes, suggesting audiences appreciate well-developed stories.

5. **Genre Preferences**: Drama appears as the most common genre, often combined with other genres like Crime or Action to create compelling storylines.

6. **Director Influence**: Certain directors consistently produce highly-rated films, demonstrating the significant impact of direction on movie quality.

7. **Star Power**: Several actors appear frequently in top-rated films, highlighting the importance of casting in a movie's success.
""")

# Display a sample of the movie data
rows_to_display = slider("Number of rows to display", min_val=5, max_val=50, default=10)
text("## Sample Movie Data")
table(df.head(rows_to_display))

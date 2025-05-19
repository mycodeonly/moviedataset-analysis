# Movie Dataset Analysis Dashboard

A Preswald app that provides comprehensive analysis and visualizations of the IMDB movies dataset.

## Overview

This interactive dashboard analyzes a dataset of 1000+ top-rated movies from IMDB, offering insights into ratings, genres, directors, actors, and more. The application is built using Preswald, a Python-based framework for creating interactive data dashboards.

## Features

- **Dataset Overview**: Displays basic information about the dataset including column descriptions
- **Top Rated Movies**: Lists the highest-rated movies in the dataset
- **Rating Distribution**: Visualizes the distribution of IMDB ratings
- **Movies by Year**: Shows trends in movie releases over time and average ratings by decade
- **Runtime Analysis**: Analyzes movie lengths and their relationship with ratings
- **Genre Analysis**: Identifies the most common genres and their average ratings
- **Directors Analysis**: Highlights the most prolific directors and their average ratings
- **Star Power**: Analyzes the most frequently appearing actors

## Data Source

The application uses the "movies_dataset.csv" file which contains information about movies including:

- Movie titles and release years
- IMDB ratings and number of votes
- Runtime information
- Genre classifications
- Director and actor information
- Box office earnings

## Usage

1. Ensure Preswald is installed in your environment
2. Run the application using the command: `python run.py`
3. Navigate through different analyses using the sidebar
4. Interact with visualizations for deeper insights

## Key Insights

The dashboard reveals several interesting patterns in the data:

1. Rating distribution across popular movies
2. Correlation between audience engagement and movie ratings
3. Trends in movie production over recent decades
4. Relationship between movie length and audience reception
5. Most successful genres, directors, and actors based on ratings

## Requirements

- Python
- Preswald
- pandas
- plotly
- numpy

## Future Improvements

Potential enhancements for future versions:

- Add predictive modeling for box office performance
- Include sentiment analysis of movie overviews
- Create network visualizations of director-actor collaborations
- Add filtering options for more interactive exploration

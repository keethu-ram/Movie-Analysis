import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import csv
import sys

df = pd.read_csv('movie_metadata.csv')

df_edited = df.drop(["color", "num_critic_for_reviews", "actor_3_facebook_likes", "actor_1_facebook_likes",\
            "num_voted_users", "facenumber_in_poster", "num_user_for_reviews",\
            "actor_2_facebook_likes", "aspect_ratio", "director_facebook_likes",\
            "movie_imdb_link", "cast_total_facebook_likes", "movie_facebook_likes",\
            "content_rating"], axis=1)

df_edited.rename(
    columns={
        "director_name":"Director",
        "duration":"Duration",
        "actor_2_name":"Supporting_Actor_1",
        "genres":"Genres",
        "actor_1_name":"Lead_Actor",
        "movie_title":"Title",
        "actor_3_name":"Supporting_Actor_2",
        "plot_keywords":"Keywords",
        "language":"Language",
        "country":"Country",
        "title_year":"Year_of_Release",
        "imdb_score":"IMDb_Rating",
        "gross":"Revenue",
        "budget":"Budget",

    },
    inplace=True
)

df_edited['Title'] = df_edited['Title'].astype(str).str[:-1]


df_edited = df_edited[["Title", "Director", "Year_of_Release", "Genres", "Budget", "Revenue", "Duration", "Language", "Country",\
"Lead_Actor", "Supporting_Actor_1", "Supporting_Actor_2", "IMDb_Rating", "Keywords"]]

def stringToList(string):
    li = list(string.split("|"))
    return li

def editColumns(df):
    for index_label, row_series in df.iterrows():
        df.at[index_label, 'Genres'] = stringToList(row_series['Genres'])
    for index_label, row_series in df.iterrows():
        df.at[index_label, 'Keywords'] = stringToList(str(row_series['Keywords']))

editColumns(df_edited)
df_edited.to_csv("edited_movie_database.csv", index=False, encoding='utf8')

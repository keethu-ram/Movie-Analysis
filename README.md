# Movie-Analysis
Analyzing a given Letterboxd list by using both webscraped information, the TMDB API, and an existing dataset, providing a word
cloud of most common keywords, details about most represented actors, directors, genres, etc. (through matlib plots), and
average budget and revenue. This is used to understand the movie habits and preferences of the user.

1) CLEANING THE DATASET:
  The "Movie MetaData" dataset (containing information for 5000 movies) from Kaggle is used in this project. In MovieAnalysis1.py,
this dataset is cleaned by dropping columns with extraneous data such as "No. of Likes on Director's Facebook Page", as such 
information is irrelevant to our analysis. 
  Next, many movies are missing revenue and budget information, and are marked by "0"s in both columns. The number of such entries
is significant enough to affect budget and revenue averages, so these values are replaced with NaN values. 
  Finally, Columns are renamed and reordered and those with multiple values under a single entry, such as "Genres" and "Keywords",
are converted from Panda Seriess to Lists of Lists for easy iteration.
  The resulting DataFrame is saved as a CSV file named "edited_movie_database.csv" when MovieAnalysis.py is run.

2) ACQUIRING THE LIST:
  acquireList.py is run with the URL of the Letterboxd list to be analyzed. A webscraper is used to create a list of all titles of all movies. Then, each movie is searched for in edited_movie_database.csv. If it is not found, the information is found witha webscraper and the TMDB (The Movie Database) API.
  The resulting information for all titles in the list is put into a DataFrame, and then saved as a CSV file named "Search.csv".
  
3) ANALYSIS:
  In analysis.py, the "Search.csv" file is analyzed to provide mean budget, revenue, duration, and rating. Additionally, matlib plots are made for top genres, actors, and directors. A word cloud is made for keywords. 
  


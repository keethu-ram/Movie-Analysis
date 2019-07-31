from lxml import html
import requests
import pandas as pd
from pandas import DataFrame
import csv
import sys
import time
import re
from bs4 import BeautifulSoup
import tmdbsimple as tmdb
import config
tmdb.API_KEY = config.API_KEY

start_time = time.time()
df = pd.read_csv('edited_movie_database.csv')

def getAttributes(url, tag, selector, aClass, attribute):
    """
    Returns a list of required attribute for all liked movies.

    Parameter url: URL of liked list
    Precondition: url is a str
    Example: "https://boxd.it/3FToC"

    Parameter tag: tag that contains necessary class
    Precondition: tag name is a str
    Example: "img"

    Parameter selector: type of selector
    Precondition: selector is a str
    Example: "class" or "ID"

    Parameter aClass: class that contains the attribute
    Precondition: class name is a str
    Example: "image"

    Parameter attribute: attribute required
    Precondition: attribute name is a str
    Example: "alt" or "title"
    """

    soup = BeautifulSoup(requests.get(url).content)
    selects = soup.find_all(tag,{selector: aClass, attribute: True})
    Attributes = []
    for s in selects:
        Attributes.append(s["alt"])
    return Attributes

def getTitles(url):
    """
    Returns a list of titles for all liked movies.

    Parameter url: URL of liked list
    Precondition: url is a str
    Example: "https://boxd.it/3FToC"
    """

    soup = BeautifulSoup(requests.get(url).content)
    selects = soup.find_all("img",{"class": "image", "alt": True})
    Titles = []
    for s in selects:
        Titles.append(s["alt"])
    return Titles

def MovieSearch(title, df):
    """
    Searches for movie in the existing DataFrame.
    If it is found, the DataFrame entry is returned as a dictionary (columns
    are keys).

    Parameter title: title of movie to be searched
    Precondition: title is a string
    Example: "Gone Girl"
    """
    results = df.query("Title=='{0}'".format(title))
    if (results.empty):
        return None
    index = (results.index.values.astype(int)[0])
    myDict = df.iloc[index,:].to_dict()
    return myDict

def ListSearch(titlesList):
    """
    Searches if each movie in the list is in the existing DataFrame.
    If found, the movie is added to dictList.

    If not, a web scraper is used to find movie details, and is then added to
    dictList.

    Finally, the list is converted to a
    DataFrame, and it is saved as a csv file named "Search.csv".

    Parameter titlesList: List of titles of movies
    Precondition: titlesList is a list
    Example: "["Gone Girl, "The Royal Tenenbaums]"
    """
    dictList = []
    newList = []
    for x in titlesList:
        result = MovieSearch(x, df)
        if (result is not None):
            dictList.append(result)
            newList.append(result)
        else:
            webResult = FindMovieDetails(x)
            if webResult is not None:
                (dictList.append(FindMovieDetails(x)))

    addToDf(newList, df)
    searchDf = pd.DataFrame(dictList)
    searchDf.to_csv("Search.csv", index=False, encoding='utf8')
    print(len(dictList))

def addToDf(newList, df):
    newDf = pd.DataFrame(newList)
    df.append(newDf)
    df.to_csv("edited_movie_database.csv", index=False, encoding='utf8')


def Search(url):
    """
    Saves all movie details as a csv file named "Search.csv" for a given
    Letterboxd list's URL

    Parameter url: URL of liked list
    Precondition: url is a str
    Example: "https://boxd.it/3FToC"
    """
    list = getTitles(url)
    ListSearch(list)
    print("--- %s seconds ---" % (time.time() - start_time))


def hyphenate(words):
    """
    Returns words with spaces replaced by hyphens.

    Parameter words: string of words to hyphenate
    Precondition: words is a str
    """
    return '-'.join(words.split())

def strip(string):
    cleanString = re.sub('\W+', ' ', string )
    return cleanString

def getTmdbUrl(title):
    """
    Returns TMDB URL of given movie.

    Parameter title: title of movie
    Precondition: title is a str
    """
    title = strip(title)
    lower = title.lower()
    urlT = hyphenate(lower)
    url =  "https://letterboxd.com/film/"+urlT+"/"
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    selects = soup.find_all("a",{"class": "micro-button track-event", \
    "data-track-action": True})
    counter = 0
    for s in selects:
        counter += 1
        if (counter == 2):
            return s['href']

def getTmdbID(title):
    """
    Returns TMDB ID of given movie.

    Parameter title: title of movie
    Precondition: title is a str
    """
    TmdbUrl = getTmdbUrl(title)
    n = 4 #no. of '/' after which the ID is
    if (TmdbUrl is None):
        print(title)
        return
    index = TmdbUrl.find('/')
    while index >= 0 and n > 1: #finding index of 4th '/'
        index = TmdbUrl.find('/', index+len('/'))
        n -= 1
    return TmdbUrl[index+1:-1]

def FindMovieDetails(title):
    """
    Finds movie details using the tmdbsimple API and returns details as a
    dictionary (columns are keys).

    Parameter title: title of movie
    Precondition: title is a str
    """
    TmdbID = getTmdbID(title)
    if (TmdbID is None):
        return
    movie = tmdb.Movies(TmdbID)
    response = movie.info()
    credits = movie.credits()
    myGenres = []
    counter = 0
    for x in range(len(movie.genres)):
        myGenres.append((movie.genres[counter]['name']))
        counter += 1

    myKey = []
    counter = 0
    for x in range(len(movie.keywords()['keywords'])):
        myKey.append((movie.keywords()['keywords'][counter]['name']))
        counter += 1

    movieObject = {
        "Title": (title.title()),
        "Director": (movie.crew[0]['name']),
        "Year_of_Release": (movie.release_date.split("-")[0]),
        "Genres": (myGenres),
        "Budget": (movie.budget),
        "Revenue": (movie.revenue),
        "Duration": (movie.runtime),
        "Language": (movie.spoken_languages[0]['name']),
        #Country.append(movie.origin_country)
        "Lead_Actor": (movie.cast[0]['name']),
        "Supporting_Actor_1": (movie.cast[1]['name']),
        "Supporting_Actor_2": (movie.cast[2]['name']),
        "IMDb_Rating": (movie.vote_average), ## TODO: fix
        "Keywords": (myKey)
    }
    return movieObject

def ListToDf(MovieList):
    """
    A web scraper is used to find movie details of all movies in the given
    list, and is then added to dictList.

    Finally, the list is converted to a DataFrame, and it is saved as a csv
    file named "my_movies.csv".

    Parameter titlesList: List of titles of movies
    Precondition: titlesList is a list
    Example: "["Gone Girl, "The Royal Tenenbaums]"
    """
    detailsList = []
    for x in MovieList:
        object = FindMovieDetails(x)
        detailsList.append(object)

    moviesDf = pd.DataFrame(detailsList)
    moviesDf.to_csv("my_movies.csv", index=False, encoding='utf8')

Search("https://boxd.it/3FToC")

import pandas as pd
import csv
import ast
import collections
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from collections import Counter


df = pd.read_csv('Search.csv')

def commonWordsList(column):
    """
    Given a column, this method turns it into a list and then flattens the list\
    of lists (since the entries are also lists), and then returns the top 4\
    most common entries (with the number of instances) as a tuple.

    Parameter column: Column of a DataFrame to be analyzed
    Precondition: column of a DataFrame
    Example: "Keywords"
    """
    l = df[column].tolist()
    list = [inner for item in l for inner in ast.literal_eval(item)] #flatten the list
    counter = collections.Counter(list)
    return(counter.most_common()[:4])

def commonWords(column, c2 = [], c3 = []):
    """
    Given a column(s) (that is practically a 1D list without any nested lists),\
    this method turns it into a list, and then returns the top 4 most common \
    entries. If more there is more than 1 column provided, it turns all given \
    columns into lists, joins them to create a single bigger list, and then \
    returns the top 4 most common entries (with the number of instances) as a \
    tuple

    Parameter column: Column of a DataFrame to be analyzed
    Paramater c2: Column of a DataFrame to be analyzed
    Parameter c3: Column of a DataFrame to be analyzed
    Precondition (for all parameters): column of a DataFrame
    Example: "Director, Lead_Actor"
    """
    l1 = df[column].tolist()
    l = l1
    if (c2 != [] and c3 != []):
        l2 = df[c2].tolist()
        l3 = df[c3].tolist()
        l = l1 + l2 + l3
    counter = collections.Counter(l)
    return(counter.most_common()[:4])

def makePlot(column):
    d = df.groupby("Director")
    plt.figure(figsize=(12,8))
    d.size().sort_values(ascending=False).plot.bar()
    plt.xticks(rotation=50)
    plt.xlabel("Name of Director")
    plt.ylabel("Number of Liked Movies")
    plt.savefig("myPlot"+".png", bbox_inches='tight')
    plt.show()
    plt.close()

def makeWordCloud(column):
    list = df[column].tolist()
    my_list = [inner for item in list for inner in ast.literal_eval(item)]
    word_could_dict=Counter(my_list)
    wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies\
    (word_could_dict)

    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("myWorldCloud"+".png", bbox_inches='tight')
    plt.show()
    plt.close()

meanBudget = df["Budget"].mean()
meanDuration = df["Duration"].mean()
meanRating = df["IMDb_Rating"].mean()
meanRevenue = df["Revenue"].mean()
topGenres = commonWordsList("Genres")
topKeywords = commonWordsList("Keywords")
topDirectors = commonWords("Director")
topActors = commonWords("Lead_Actor", "Supporting_Actor_1", "Supporting_Actor_2")
makeWordCloud("Keywords")
makePlot("Genres")

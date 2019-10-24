import sys
import pandas as pd
import numpy as np
import difflib

def getMeanRatingForMatches(movie, ratingDf, n):

    closeMatch = difflib.get_close_matches(movie, ratingDf["title"], n = n, cutoff = 0.6)
    indexForRating = ratingDf['title'].isin(closeMatch)
    location = ratingDf.loc[indexForRating]
    print(location)
    return location['rating'].mean()

def main():
    movie_list = sys.argv[1]
    movie_rating = sys.argv[2]
    outputFilename = sys.argv[3]

    movie_data = open(movie_list).readlines()
    movie_dataFrame = pd.Series(movie_data).replace('\n', '', regex=True)
    rating_data = pd.read_csv(movie_rating)
    rating_array = np.array(rating_data["title"])
    rating_array_length = len(rating_array)
    meanRating = round(movie_dataFrame.apply(getMeanRatingForMatches, args=(rating_data, rating_array_length)), 2)
    output = pd.DataFrame(
    data={'title' : movie_dataFrame,'rating': meanRating}
    ).set_index('title').dropna().sort_values(by=['title']).to_csv(outputFilename)




if __name__ == '__main__':
    main()

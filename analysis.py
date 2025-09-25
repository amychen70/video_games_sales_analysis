from clean import read_file, remove_missing_data, convert_str_to_float, remove_games_before_year
FILENAME = "vgsales.csv"
COLUMN_RANK = 0
COLUMN_NAME = 1
COLUMN_PLATFORM = 2
COLUMN_YEAR = 3
COLUMN_GENRE = 4
COLUMN_PUBLISHER = 5
COLUMN_NA = 6
COLUMN_EU = 7
COLUMN_JP = 8
COLUMN_OTHER = 9
COLUMN_GLOBAL = 10

# reading the CSV file into a 2d list
data = read_file(FILENAME)

# removing any games that have any missing pieces of data associated with them
non_empty_data = remove_missing_data(data)

# converting any numeric values into proper integer format instead of strings
converted_type_data = convert_str_to_float(non_empty_data, COLUMN_RANK, COLUMN_YEAR, COLUMN_NA,
                                           COLUMN_EU, COLUMN_JP, COLUMN_OTHER, COLUMN_GLOBAL)

# removing any games before the year range we are working with
cleaned_data = remove_games_before_year(converted_type_data)


# constant dictionary for correlating the column numbers (in the processed data) with what their values mean
COLS = {"rank" : 0, "name" : 1, "platform" : 2, "year" : 3, "genre" : 4,
        "publisher" : 5, "region_NA" : 6, "region_EU" : 7, "region_JP" : 8,
        "region_other" : 9}


def calc_region_totals(data, regions):
    """
    Does:
        Calculates the total game sales in each region (both as an absolute
        total and for each of the separate genres

    Parameters:
        •data
            •2D list of lists
            •Dataset containing game information
        •regions - list of strings
            •The names of the regions - in order
            •These have to be added (instead of derived like the genres)
             because their info is not included in the data lists; it's only in
             the CSV's headers, which weren't included since we processed each
             row as a list instead of a dictionary

    Returns:
        •A 2D dictionary where
          •The outer dictionary's keys are the names of each region
          •The inner dictionaries breaks it down into sums by genre (alongside
          the total sums at the end)
    """

    # creating an empty dictionary to add stuff into
    regional_totals = {}

    # getting a list of genres
    list_of_genres = find_genres(data)

    # going through the list of regions and adding portions for them to the dict
    # each of which contains a (currently empty) dictionary
    for region in regions:
        regional_totals[region] = {}

        # then each of those inner-dicts is given a spot for each region
        # (set to 0 already so it can be added to later)
        for genre in list_of_genres:
            regional_totals[region][genre] = 0

        # also then adding one last section to the region: its total sales
        regional_totals[region]["total_sales"] = 0

    # thus, this is now the setup: more or less
    '''
    regional totals = {
            "region1" : {"genre1" : 0, "genre2" : 0, ... "total_sales" : 0 },
            "region2" : {"genre1" : 0, "genre2" : 0, ... "total_sales" : 0 },
            ...
        }
    '''
    # which seems ready to collect the sums!

    # finally going through the data itself...
    for game in data:

        # for each game, it gets tested against each of the genres
        for genre in list_of_genres:
            if game[COLS["genre"]] == genre:
                # and gets added only to genre-specific sum it fits
                regional_totals[regions[0]][genre] += game[COLS["region_NA"]]
                regional_totals[regions[1]][genre] += game[COLS["region_EU"]]
                regional_totals[regions[2]][genre] += game[COLS["region_JP"]]
                regional_totals[regions[3]][genre] += game[COLS["region_other"]
                ]

        # also, their sales are generally added to each region's total sales
        regional_totals[regions[0]]["total_sales"] += game[COLS["region_NA"]]
        regional_totals[regions[1]]["total_sales"] += game[COLS["region_EU"]]
        regional_totals[regions[2]]["total_sales"] += game[COLS["region_JP"]]
        regional_totals[regions[3]]["total_sales"] += game[COLS["region_other"]
        ]

    # returning the 2d dict
    return regional_totals


def find_genres(data):
    """
    Does:
        Returns a list of all the genres featured in a dataset

    Parameters:
        •data
            •list of lists: a dataset containing games and their information

    Returns:
        list of genre names (as strings)
    """

    # creating an empty list to append into
    genre_list = []

    # going through all the games in the data set
    for game in data:
        # if the game's genre hasn't been seen yet, it is added to the genre list
        if game[COLS["genre"]] not in genre_list:
            genre_list.append(game[COLS["genre"]])

    # list of genres is returned
    return genre_list

def get_genre_sizes(data, genres):
    """
    Does:
        Finds out how many games are in each genre

    Parameters:
        •data
            •2D list of games and their information
        •genres
            •list of lists holding the different genre names

    Returns:
        dict of genre names correlated with integer values of the number
        of games in that genre
    """

    # creating a dict of the number of games in each genre
    num_of_games = {}

    # going through each genre and setting up their genre with a count of 0
    # so that i can add to it later when counting
    for genre in genres:
        num_of_games[genre] = 0

    # going through all the games
    for game in data:
        # comparing each game to all the genres
        for genre in num_of_games.keys():
            # and increasing the count of whichever genre it fits into by one
            if game[COLS["genre"]] == genre:
                num_of_games[genre] += 1

    return num_of_games

def get_genre_total_sales(data, genres):
  """
    Does:
         Finds out total global sales from each genre

    Parameters:
      •data
          •2D list of games and their information
      •genres
          •list of lists holding the different genre names

    Returns:
        dict of genre names correlated with float values of the number
        of the number of games in that genre in millions
    """

  # creating a dict of the number of games in each genre
  genre_sales = {}

  # going through each genre and setting up their genre with a count of 0
  # so that i can add to it later when counting
  for genre in genres:
      genre_sales[genre] = 0

  # going through all the games
  for game in data:
      # comparing each game to all the genres
      for genre in genre_sales.keys():
          # and adding the game's total sales to that genre's count
          if game[COLUMN_GENRE] == genre:
              genre_sales[genre] += game[COLUMN_GLOBAL]

  return genre_sales




def main():
    # calculating the number of sales of all the games in each genre, for each region
    # and also finds the total sales of all games (regardless of their genre) from each region
    regional_totals = calc_region_totals(cleaned_data, ["NA", "EU", "JP", "Other"])

    # making a list of the genres to input into things later
    genre_list = find_genres(cleaned_data)

    # finding the total number of games in each genre
    # (not their sales, just the number of actual games there are in each)
    game_numbers_in_each_genre = get_genre_sizes(cleaned_data, genre_list)


    # finding the total number of global sales in each genre
    total_sales_by_genre = get_genre_total_sales(cleaned_data, genre_list)



main()
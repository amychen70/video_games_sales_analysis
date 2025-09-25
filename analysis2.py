from clean import read_file, remove_missing_data, convert_str_to_float, remove_games_before_year
from analysis import calc_region_totals, find_genres
FILENAME = "vgsales.csv"
NA = 'NA_Sales'
EU = 'EU_Sales'
JP = 'JP_Sales'
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
'''Are there regional preferences for game genres among consumers since (2006/2013)?  '''


def count_total_games(game_list):
    """
    Does:
        Gets the total number of games in file

    Parameters:
      •game_list: the 2d list of the games and their data

    Returns:
        Total the number of games in the file
    """
    total = 0
    for line in game_list:
        total += 1

    return total


# Top x Ranking
def rank_top_x(data, name_col, how_many=5):
    """
    Does:
        Ranks and returns the top <x> number of games in the dataset

    Parameters:
        •data: 2d list
            •the games in the data file
        •name_col: int
            •the index of the cell the game's name is in
        •how_many: int
            •the number of top picks to choose from - default of 5

    Returns:
        a list containing the top <x> highest selling games in order
    """

    # creating list of games to return
    top_five_list = []

    # making sure it won't try to go over the length of the list
    if how_many >= len(data):
        how_many = len(data)
    # and if the count is invalid, it just returns nothing
    elif how_many <= 0:
        return None

    for i in range(how_many):
        top_five_list.append(data[i][name_col])
        i += 1

    return top_five_list


# Average sales per genre per country
def average_per_genre_in_region(data, genre_string, genre_column, country_column):
    """
    Does:
        Calculates average sales a game from the targeted genre in the targeted countries

    Parameters:
      •data (2d list)
          •list of each of the games and their associated values from the file
      •genre_string (str)
          •String of chosen genre
      •genre_column (int)
          •Column index for the genre (e.g., 4)
      •country_column (int)
          •Column index for the targeted country (e.g., NA: 6, EU: 7,
          JP: 8, Other: 9, Global: 10)
      •country_name (str)
          •String of country targeted: NA, EU, JP, Others, Global

    Returns:
        float, average sales of a single game from the targeted genre in
        the targeted country
    """
    count = 0
    divide = 0

    for game in data:
        if game[genre_column] == genre_string:
            count += game[country_column]
            divide += 1
    average = count / divide

    return average


# calling that previous function repeatedly to get all region+genre combos
def get_all_genre_averages_by_region(data, regions_and_cols, genre_list, genre_column):
  """
  Does:
      •creates a 2d dictionary containing the average sales of a single game
      in each genre for each region

  Parameters:
      •data - 2D list of lists
          •Dataset containing game information
      •regions_and_cols - dict of strings : ints
          •keys are the names of the regions in order
          •their values are the int of their column
      •genre_list - list of strings
          •names of the genres
      •genre_column - int
          •the index of the genres in the 2d data list

    Returns:
        •A 2D dictionary where
          •The outer dictionary's keys are the names of each region
          •The inner dictionaries breaks it down into the average sales of a
          game in each genre
    """

  regional_averages = {}


  # going through the list of regions and adding empty dicts keyed to them
  # in the outer dict
  for region, region_col in regions_and_cols.items():
      regional_averages[region] = {}

      # then each of those inner-dicts is given a genre and the region's average
      # sales in that genre
      # converted to an int since a partial game doesn't really make sense
        # also it gets rounded before the actual int change statement so that
        # it actually *rounds* instead of truncating
      for genre in genre_list:
          regional_averages[region][genre] = int(round(average_per_genre_in_region(data, genre, genre_column, region_col), 0))

  # returning the 2d dict
  return regional_averages



# not an analysis function, but for the purpose of printing the results of them
def print_regional_values(regional_values, list_of_genres):
    """
    does:
        •prints the total sales by genre for each region in a series of
        aligned columns for more easy readability

    parameters:
        •regional_values:
            2d dictionary - the regions and their sales for each genre
        •list_of_genres: list of strings
            the genres in the list

    return:
        •nothing; it just prints
    """
    # creating the start string for the region labels; empty but has width for
    # alignment reasons
    #   •this make use of .format(), because that's the only way i found to
    #    make columns of consisent width regardless of shorter string length
    #       •the string stuff before .format() is what it will insert the new
    #        string bits into
    #       •the thing within the parentheses of .format() is the string to be
    #        inserted at the location indicated by {}
    #       •the :<10 part within the braces sets a width (so that even if the
    #        inserted string is shorter, it will still allocate that much
    #        space) - 12 was chosen sorta arbitrarily as being wide enough
    #           •also, the text within will be left aligned (indicated by <)
    region_label_string = "{:<12}".format("")

    # adding all the region labels into that string to be printed as one line
    for region_name in regional_values.keys():
        region_label_string += "{:>12}".format(region_name)

    # printing that one line
    print(region_label_string)

    # then going through each of the genres to get their scores for each
    # subsequent row
    for genre in genre_list:
        # starting the row with the genre's name
        formatted_row_string = "{:<12}".format(genre)

        # then adding each of the values following that
        for region in regional_values.values():
            formatted_row_string += "{:>12}" .format(str(region[genre]))

            # which means in theory this should lead to each of the values in the
            # row, evenly spaced from each other

        # printing the completed row before the loop moves on to the next one
        print(formatted_row_string)

def main():
    data = read_file(FILENAME)
    non_empty_data = remove_missing_data(data)
    converted_type_data = convert_str_to_float(non_empty_data, COLUMN_RANK, COLUMN_YEAR, COLUMN_NA,
                                               COLUMN_EU, COLUMN_JP, COLUMN_OTHER, COLUMN_GLOBAL)
    cleaned_data = remove_games_before_year(converted_type_data)

    # Generated list of genres in cleaned data
    genre_list = find_genres(cleaned_data)
    # Generated list of genres and their sales in cleaned data
    regional_totals = calc_region_totals(cleaned_data, ["NA", "EU", "JP", "Other"])

    # Comparison of games before and after cleaning
    print('There are', count_total_games(data), 'games in the uncleaned data')
    print('There are', count_total_games(cleaned_data), 'games in the cleaned data')
    print(count_total_games(data) - count_total_games(cleaned_data), 'games were created before 2013 '
                                                                     'and filtered out in the cleaned data. ')

    # creating a space before the next set of numbers
    print()

    # Ranking of top 5 selling games from the cleaned dataset
    print('Top 5 Most Sales Games:')
    print(rank_top_x(cleaned_data, COLUMN_NAME, how_many=5))

    print()

    # outputting the total number of games sold in each region
    for name, numbers in regional_totals.items():
        if name == "NA":
            longer_region_name = "North America"
        elif name == "EU":
            longer_region_name = "Europe"
        elif name == "JP":
            longer_region_name = "Japan"
        else:
            longer_region_name = "other regions"

        print("Total sales in ", longer_region_name, ": ", numbers["total_sales"], sep="")

    print()
    print()

    # Chart of regional sales of each genre
    print("Sales by genre by region")
    print("-" * 60)
    print_regional_values(regional_totals, genre_list)

    print()
    print()

    regions_to_cols = {"NA": COLUMN_NA, "EU": COLUMN_EU, "JP": COLUMN_JP, "Other": COLUMN_OTHER}

    regional_averages = get_all_genre_averages_by_region(cleaned_data, regions_to_cols, genre_list, COLUMN_GENRE)

    print("Average sales of a single game in a genre in each region")
    print("-" * 60)
    print_regional_values(regional_averages, genre_list)
    

main()

import csv


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

def read_file(filename):
    """
    Does:
      Reads every line of the file, except the header,
      and stored in a 2d list which is returned at the end

    Parameters:
      •filename for a CSV file

    Returns:
      2D list of strings
    """

    # sets up an empty list for the lists in the file to be put into
    data = []

    # opens the file
    with open(filename) as csvfile:

        # sets up reader to the list, separating at commas
        reader = csv.reader(csvfile, delimiter=",")

        # skip first line so that the header isn't used in the data set
        next(reader)

        # adds each row in the data set into the new list to create a list of lists
        for row in reader:
            data.append(row)

    # returns the new list of data
    return data

def remove_missing_data(list_of_lists):
    """
    Does:
      Removes rows from the dataset that contain 'N/A'

    Parameters:
      •list_of_lists
            •(list of lists of the dataset)

    Returns:
      List of lists without 'N/A' entries
    """

    # sets up an empty list
    fixed_list_of_lists = []

    # for loop to iterate through the lists in the list of lists
    for each_list in list_of_lists:

        # if n/a is in the list don't add it to the new list
        if 'N/A' in each_list:
            pass

        # adds the list to the new list
        else:
            fixed_list_of_lists.append(each_list)

    # returns new list
    return fixed_list_of_lists


def convert_str_to_float(list_of_lists, col_rank, col_year, col_na, col_eu, col_jp, col_other, col_global):
    """
    Does:
      Takes the list of lists and makes a new list with the numerical iterals

    Parameters:
      •list_of_lists
            •list of lists of all the data to be changed
      •col_rank
            •int pertaining to the rank column
      •col_year
            •int pertaining to the year column
      •col_na
            •int pertaining to the north america column
      •col_eu
            •int pertaining to the europe column
      •col_jp
            •int pertaining to the japan column
      •col_other
            •int pertaining to the other column
      •col_global
            •int pertaining to the global sales column

    Returns:
      List of lists with specified columns converted to integers
    """

    # sets up new list to be added to
    fixed_list = []

    # iterates through lists making a new list for the cleaner list to go into
    for game in list_of_lists:
        small_list = []

        # iterates through indexes and sets the numbers to numbers and their true values
        for index in game:

            # if statement that converts rank and year to integers and adds them to the new list
            if (index == game[col_rank] or index == game[col_year]):
                int_number = int(index)
                small_list.append(int_number)

            # if statement that converts na, eu, jp, and other sales to integers and add them to a new list
            elif (index == game[col_na] or index == game[col_eu] or index == game[col_jp] or index == game[col_other] or index == game[col_global]):
                float_number = float(index)
                float_number_real = float_number * 1000000
                int_number_real = int(float_number_real)
                small_list.append(int_number_real)

            # if its not one of those indexes, just add a string
            else:
                small_list.append(index)

        # add new list to the list of lists
        fixed_list.append(small_list)

    # returns the list of lists
    return fixed_list


def remove_games_before_year(list_of_lists):
    """
    Does:
      Filters the dataset to include only games released in or after 2013

    Parameters:
      •lists of lists
            •(list of lists of the dataset)

    Returns:
      list of lists for games released after 2013
    """
    # sets up an empty list
    fixed_list_of_lists = []

    # for loop to iterate through the lists in the list of lists
    for game in list_of_lists:

      # if the year in the list is after 2013, it is added to the list
      if game[COLUMN_YEAR] >= 2013:
          fixed_list_of_lists.append(game)

    # returns new list
    return fixed_list_of_lists


def main():
    # reading the CSV file into a 2d list
    data = read_file(FILENAME)

    # removing any games that have any missing pieces of data associated with them
    non_empty_data = remove_missing_data(data)

    # converting any numeric values into proper integer format instead of strings
    converted_type_data = convert_str_to_float(non_empty_data, COLUMN_RANK, COLUMN_YEAR, COLUMN_NA, COLUMN_EU,
                                               COLUMN_JP, COLUMN_OTHER, COLUMN_GLOBAL)

    # removing any games before the year range we are working with
    cleaned_data = remove_games_before_year(converted_type_data)
    print(cleaned_data)

main()
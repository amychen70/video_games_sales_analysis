from clean import read_file, remove_missing_data, convert_str_to_float, remove_games_before_year
from analysis import find_genres, get_genre_sizes
from analysis2 import (calc_region_totals, count_total_games, print_regional_values,
                       get_all_genre_averages_by_region)
from heatmap import calculate_relative_portions

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

data = read_file(FILENAME)
non_empty_data = remove_missing_data(data)
converted_type_data = convert_str_to_float(non_empty_data, COLUMN_RANK, COLUMN_YEAR, COLUMN_NA,
                                           COLUMN_EU, COLUMN_JP, COLUMN_OTHER, COLUMN_GLOBAL)
cleaned_data = remove_games_before_year(converted_type_data)

def main():
    genre_list = find_genres(cleaned_data)
    game_numbers_in_each_genre = get_genre_sizes(cleaned_data, genre_list)
    regions_to_cols = {"NA": COLUMN_NA, "EU": COLUMN_EU, "JP": COLUMN_JP, "Other": COLUMN_OTHER}
    regional_averages = get_all_genre_averages_by_region(cleaned_data, regions_to_cols, genre_list, COLUMN_GENRE)
    regional_totals = calc_region_totals(cleaned_data, ["NA", "EU", "JP", "Other"])

    # printing numbers of games in the data set at the start, once a few flawed items were removed,
    # and once our studied range was cut down to size
    print('There were', count_total_games(data), 'games in the original data set')
    print("Of which", count_total_games(non_empty_data), "were not missing any values \n")
    print('But after the games released before 2013 were removed, there were just', count_total_games(cleaned_data),
          'games left.')

    # creating a line space
    print("\n")

    print("Breaking down those games:")
    # printing the genre numbers
    for genre, numbers in game_numbers_in_each_genre.items():
        print("{:<15} ".format("•" + genre + ":"), numbers, sep="")




    # Chart of regional sales of each genre
    print("Absolute sales by genre by region")
    print("-" * 60)
    print_regional_values(regional_totals, genre_list)



    # creating a set of the relative sales (the heatmap did this in its own function,
    # but it didn't save that version so it must be called again)
    relative_sales_by_region = calculate_relative_portions(regional_totals, "total_sales")

    # going through and rounding all their values for readability
    for region, genre_nums in relative_sales_by_region.items():
        for genre, numbers in genre_nums.items():
            relative_sales_by_region[region][genre] = round(numbers, 3)

    print("Relative sales by genre by region")
    print("-" * 60)
    print_regional_values(relative_sales_by_region, genre_list)



    print("Average sales of a single game in a genre in each region")
    print("-" * 60)
    print_regional_values(regional_averages, genre_list)
main()
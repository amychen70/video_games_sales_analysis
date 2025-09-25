from clean import (read_file, remove_missing_data, convert_str_to_float,
                   remove_games_before_year)
from analysis import (calc_region_totals, find_genres, get_genre_sizes,
                      get_genre_total_sales)
import matplotlib.pyplot as plt
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

def plot_sales_vs_num_of_games(num_of_games, sales, colors):
    """
    Does:
        Creates a plot that shows the relationship between number of global sales
        and the number of games in each genre to show if the sales results
        may be related to just the number of games in the list rather than their
        average popularity per game

    Parameters:
      •num_of_games (dict)
          •A dictionary where keys are genre names (str) and values are the
          number of games in each genre (int)
      •sales (dict)
          •A dictionary where keys are genre names (str) and values are the
          total global sales for each genre (int or float)
      •colors (list of str)
          •A list of color strings for plotting points, with colors cycling if
          there are more points than colors

    Returns:
        None:
            •Generates and displays a plot with:
                •Generates and displays a plot with:
                    •Points labeled by genre.
                    •X-axis: Number of games in the genre.
                    •Y-axis: Total global sales.
            •Saves the plot as "Sales vs Number of Games.png".
    """
    # creating a number to increment for selecting colors at each step in the loop
    i = 0

    # going through all the keys (which are the genres) and graphing their
    # number of total sales over the number of games in the genre
    # each is also labeled with their genre and given a color from the input list
    # (repeating if there are more points than colors, though ideally that shouldn't be necessary)
    for genre in num_of_games.keys():
      plt.plot(num_of_games[genre], sales[genre],
               marker = "o", label = genre, color = colors[i % len(colors)])
      i += 1


    # labels
    plt.title("Number of Games in Genre vs Total Sales of the Genre")
    plt.xlabel("Number of Games in the Genre")
    plt.ylabel("Number of Global Sales")
    # making legend of the labels
    plt.legend()

    # saving the figure
    plt.savefig("Sales vs Number of Games.png")
    # showing the graph
    plt.show()


def plot_ratio_bars_of_sales_vs_num_of_games(num_of_games, sales, colors):
  """
    Does:
        Creates a bar plot showing the ratios depicted by the previous scatter
        plot, so as to allow visual comparison in another way

    Parameters:
      •num_of_games (dict)
          •A dictionary where keys are genre names (str) and values are the
          number of games in each genre (int)
      •sales (dict)
          •A dictionary where keys are genre names (str) and values are the
          total global sales for each genre (int or float)
      •colors (list of str)
          •A list of color strings for plotting points, with colors cycling if
          there are more points than colors

    Returns:
        None:
            •Generates and displays a bar plot
            •Saves the plot as "Sales vs Number of Games bar.png".
  """

  i = 0

  # looping through the genres
  for genre in num_of_games.keys():
      # plotting each bar with the number of sales divided by the number of
      # games in that genre
      plt.bar(genre, sales[genre] / num_of_games[genre],
              color = colors[i % len(colors)])
      i += 1

  # labels
  plt.title("Popularity of an \"Average\" Game In Each Genre")
  plt.xlabel("Genre")
  plt.ylabel("Ratio of Sales to Number of Games")

  # rotating the x labels so they don't overlap
  plt.xticks(rotation=75)

  # saving the figure
  plt.savefig("Sales vs Number of Games bar.png")
  # showing the graph
  plt.show()


def main():
    data = read_file(FILENAME)
    non_empty_data = remove_missing_data(data)
    converted_type_data = convert_str_to_float(non_empty_data, COLUMN_RANK, COLUMN_YEAR, COLUMN_NA,
                                               COLUMN_EU, COLUMN_JP, COLUMN_OTHER, COLUMN_GLOBAL)
    cleaned_data = remove_games_before_year(converted_type_data)

    regional_totals = calc_region_totals(cleaned_data, ["NA", "EU", "JP", "Other"])

    genre_list = find_genres(cleaned_data)

    game_numbers_in_each_genre = get_genre_sizes(cleaned_data, genre_list)

    total_sales_by_genre = get_genre_total_sales(cleaned_data, genre_list)

    color_list = ["red", "rebeccapurple", "dimgray", "black", "dodgerblue", "brown",
                  "gold", "grey", "lime", "forestgreen", "purple", "blue"]


    plot_sales_vs_num_of_games(game_numbers_in_each_genre, total_sales_by_genre, color_list)
    plot_ratio_bars_of_sales_vs_num_of_games(game_numbers_in_each_genre, total_sales_by_genre, color_list)


main()
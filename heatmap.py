from clean import read_file, remove_missing_data, convert_str_to_float, remove_games_before_year
from analysis import calc_region_totals, find_genres
import plotly.express as px

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

def calculate_relative_portions(data, total_col):
    """
    Does:
        Takes a series of sales numbers by genre in each region, and finds
        the proportion of the total region's sale that that number
        represents. Those values are then returned in a new dict, each still
        associated with their own regions and genres like before

    Parameters:
      •data (dict)
          •A 2D dictionary where:
              •Outer keys represent region names
              •Inner keys represent genres and total sales for the region
      •total_col (str)
          •Key representing the total sales count in each region's dictionary

    Returns:
        String with total sales of targeted genre in targeted country
    """

    # creating an empty dict to add values into
    result_dict = {}

    # going through each of the regions in the data set
    for region_name, region_data in data.items():

        # creating another dict for the relative sales in a specific region
        portions_dict = {}

        # goes through the per-genre sales in that region
        for genre, sales in region_data.items():

            # i don't want to include the genre with the total sales for the
            # region, so this conditional pulls that one out
            if genre != total_col:

                # each genre's sales number is divided by the region's total
                # sales and the value added to the region's dict
                portions_dict[genre] = sales / region_data[total_col]

        # that region-specific dictionary of values is added to its associated
        # region in the outer dictionary
        result_dict[region_name] = portions_dict
    # loop ends

    # returns the dict
    return result_dict

def reformat_heatmap_data(data):
    """
    Does:
        Changes the regional genre sales portions into a list format so
        it can be used in the heatmap without causing errors

    Parameters:
      •data (dict)
          •A 2D dictionary with region names as keys and their sales
          data as inner dictionaries

    Returns:
        A 2D list of values that plotly can use for a heatmap without issues
    """

    formatted_list = []

    # goes through each of the positions and just makes it a list
    # it loses the labels in the process though, so i'll have to account for
    # that later.
    for region in data.values():
        regional_list = []
        for genre_sales in region.values():
            regional_list.append(round(genre_sales,5))
        formatted_list.append(regional_list)

    return formatted_list


def create_relative_amounts_heatmap(base_sales_data, total_col,
                                    x_title, y_title, color_label, x_labels, y_labels):
    """
    Does:
        Creates a heatmap showing the portion of the sales in each region
        made up by each of the genres

    Parameters:
      •base_sales_data (list)
          •A 2D list with each row being a region and each column being
          each genre's absolute sales numbers
      •total_col (str)
          •The key of the row with the total sums
      •x_title (str)
          •String title of the x axis
      •y_title (str)
          •String title of the y axis
      •color_label (str)
          •String label of the color value
      •x_labels (list of str)
          •List of string names of each of the x values (the genres)
              •would be obtained from that other function that finds the genres
      •y_labels (list of str)
          • List of string names of each of the y values (regions)
              •would have to be given from the user - we don't have any way
              to derive it from the files currently

    Returns:
        None
            •makes the visual and displays the heatmap
    """

    # taking the absolute data and getting a form with relative proportions
    relative_sales = calculate_relative_portions(base_sales_data,
                                                 total_col)

    relative_sales = reformat_heatmap_data(relative_sales)

    # creating the heatmap and storing it in variable "figure"
    figure = px.imshow(relative_sales, text_auto = True,
        labels = dict(x = x_title, y = y_title, color = color_label),
                       x = x_labels, y = y_labels, height = 800)

    # moving the x axis title to the top since it looks better
    figure.update_xaxes(side = "top")

    # showing the heatmap
    figure.show()

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

    # creating the heatmap
    create_relative_amounts_heatmap(regional_totals, "total_sales",
                                    "Genre", "Region", "Fraction of Region's Sales",
                                    genre_list, ["NA", "EU", "JP", "Other"])
main()
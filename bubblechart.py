from clean import read_file, remove_missing_data, convert_str_to_float, remove_games_before_year
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

def calculate_sales_by_genre_region(data):
    """
    Does:
        Aggregates sales data by genre for each region

    Parameters:
      •data (list)
          •A 2D list of cleaned and processed data

    Returns:
        A dictionary with genres as keys and total sales
        as values: {region: {genre: total_sales}}
    """
    regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    genre_sales = {}
    for region in regions:
        genre_sales[region] = {}

    for row in data:
        genre = row[COLUMN_GENRE]
        na_sales = row[COLUMN_NA]
        eu_sales = row[COLUMN_EU]
        jp_sales = row[COLUMN_JP]
        other_sales = row[COLUMN_OTHER]

        # add sales to NA region
        if genre not in genre_sales['NA_Sales']:
            genre_sales['NA_Sales'][genre] = na_sales
        else:
            genre_sales['NA_Sales'][genre] += na_sales

        # add sales to EU region
        if genre not in genre_sales['EU_Sales']:
            genre_sales['EU_Sales'][genre] = eu_sales
        else:
            genre_sales['EU_Sales'][genre] += eu_sales

        # add sales to JP region
        if genre not in genre_sales['JP_Sales']:
            genre_sales['JP_Sales'][genre] = jp_sales
        else:
            genre_sales['JP_Sales'][genre] += jp_sales

        # add sales to Other region
        if genre not in genre_sales['Other_Sales']:
            genre_sales['Other_Sales'][genre] = other_sales
        else:
            genre_sales['Other_Sales'][genre] += other_sales
    return genre_sales

def plot_bubble_chart(genre_sales):
    """
    Does:
        Creates a bubble chart of sales by genre and region

    Parameters:
      •genre_sales (dict)
          •A dictionary of region and genre sales data

    Returns:
        None
    """
    # x variable - region, y variable - genres
    regions = []
    genres = []

    # collect all unique regions and genres
    for region, sales in genre_sales.items():
        if region not in regions:
            regions.append(region)
        for genre in sales.keys():
            if genre not in genres:
                genres.append(genre)

    # prepare the data for plotting
    x = [] # regions
    y = [] # genres
    sizes = [] # bubble sizes

    # prepare data for plotting
    for region_index in range(len(regions)):
        for genre_index in range(len(genres)):
            region = regions[region_index]
            genre = genres[genre_index]
            if genre in genre_sales[region]:
                x.append(region_index)  # Region index
                y.append(genre_index)  # Genre index
                sizes.append(genre_sales[regions[region_index]][genres[genre_index]] / 1e6)

    # adjust bubble sizes
    bubble_sizes = []
    for size in sizes:
        bubble_sizes.append(size * 10)

    # create the chart
    plt.scatter(x, y, s=bubble_sizes, alpha=0.6, edgecolors="w")
    # add labels and title
    plt.xticks(range(len(regions)), regions)
    plt.yticks(range(len(genres)), genres)
    plt.xlabel("Regions")
    plt.ylabel("Genres")
    plt.title("Bubble Chart: Sales by Genre and Region")
    plt.savefig("bubblechart.png", bbox_inches='tight')
    plt.show()

def main():
    data = read_file(FILENAME)
    non_empty_data = remove_missing_data(data)
    converted_type_data = convert_str_to_float(non_empty_data, COLUMN_RANK, COLUMN_YEAR, COLUMN_NA,
                                               COLUMN_EU, COLUMN_JP, COLUMN_OTHER, COLUMN_GLOBAL)
    cleaned_data = remove_games_before_year(converted_type_data)

    # calculate sales by genre
    genre_sales = calculate_sales_by_genre_region(cleaned_data)

    # plot the bubble chart
    plot_bubble_chart(genre_sales)

main()
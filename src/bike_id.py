import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from data_utils import load_indego_data


def bike_id():

    df_trips = load_indego_data(columns=['start_time', 'trip_id', 'bike_id'])
    df_stations = load_indego_data(columns=['station_id', 'status'], folder='stations')

    df_numeric_bike_ids = df_trips[df_trips['bike_id'].apply(lambda x: str(x).isnumeric())].copy()
    df_numeric_bike_ids['bike_id'] = df_numeric_bike_ids['bike_id'].astype(int)

    bike_id_ride_count = df_numeric_bike_ids['bike_id'].value_counts()

    ax = sns.barplot(
        x=bike_id_ride_count.index.astype(str), # Use strings for X-axis labels to prevent numeric scaling
        y=bike_id_ride_count.values, 
        palette="viridis",
        hue=bike_id_ride_count.index.astype(str)
    )

    plt.title('Bike Usage', fontsize=15)
    plt.xlabel('Bike ID', fontsize=12)
    plt.ylabel('Number of Trips', fontsize=12)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))

    output_file = "../output/bike_id/id_ride_frequency.png"
    plt.savefig(output_file)
    print(f"Done! Chart saved to {output_file}")

    with open("../output/bike_id/bike_id_stats.txt", "w") as file:
        file.write(f"The minimum bike id is {df_numeric_bike_ids['bike_id'].min()}\n")
        file.write(f"The maximum bike id is {df_numeric_bike_ids['bike_id'].max()}\n")
        file.write(f"The number of bikes used for rides is {df_trips['bike_id'].nunique()}\n")
        file.write(f"The average number of bikes per dock is {round(df_trips['bike_id'].nunique()/df_stations['station_id'].nunique())}\n")
        file.write(f"The most frequently used bike ID is {bike_id_ride_count.index[0]} with {bike_id_ride_count.values[0]} rides.\n")
        file.write(f"The least frequently used bike ID is {bike_id_ride_count.index[-1]} with {bike_id_ride_count.values[-1]} rides.\n")


if __name__ == "__main__":
    bike_id()
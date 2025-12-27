from data_utils import load_indego_data


def general_stats():

    df_trips = load_indego_data(columns=['start_time', 'trip_id', 'bike_id'])
    df_stations = load_indego_data(columns=['station_id', 'status'], folder='stations')

    df_numeric_bike_ids = df_trips[df_trips['bike_id'].apply(lambda x: str(x).isnumeric())].copy()
    df_numeric_bike_ids['bike_id'] = df_numeric_bike_ids['bike_id'].astype(int)

    with open("../output/general_stats.txt", "w") as file:
        file.write(f"There were {len(df_trips)} from July 2015 through September 2025.\n")
        file.write(f"Trip ids range from {min(df_trips['trip_id'])} to {max(df_trips['trip_id'])}\n")
        file.write(f"The number of unique start stations is {len(df_stations)}\n")
        file.write(f"Station ids range from {min(df_stations['station_id'])} to {max(df_stations['station_id'])}\n")

if __name__ == "__main__":
    general_stats()
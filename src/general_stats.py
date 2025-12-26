from data_utils import load_indego_data


def general_stats():

    df = load_indego_data(columns=['start_time', 'trip_id'])

    with open("../output/general_stats.txt", "w") as file:
        file.write(f"There were {len(df)} from July 2015 through September 2025.\n")
        file.write((f"Trip ids range from {min(df['trip_id'])} to {max(df['trip_id'])}\n"))

if __name__ == "__main__":
    general_stats()
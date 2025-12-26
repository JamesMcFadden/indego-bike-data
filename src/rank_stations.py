import pandas as pd
import s3fs
import pyarrow.dataset as ds
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
S3_TRIPS_PATH = f"{BUCKET_NAME}/processed/trips/"
S3_STATIONS_PATH = f"{BUCKET_NAME}/processed/stations/"
OUTPUT_IMAGE = "../output/station_rankings.png"

def get_station_names(fs):
    print("Loading station metadata...")
    station_files = fs.glob(S3_STATIONS_PATH + "*stations*.parquet")
    
    if not station_files:
        print("ERROR: No station file found in S3.")
        return None
        
    latest_station_file = sorted(station_files)[-1]
    dataset = ds.dataset(latest_station_file, filesystem=fs, format="parquet")
    df = dataset.to_table().to_pandas()
    df['station_id'] = df['station_id'].astype(str)
    return df[['station_id', 'station_name']]

def visualize_ranks(df):
    print("Generating visualization...")
    
    top_20 = df.sort_values('trips_all_time', ascending=False).head(20).copy()
    
    # Melt the dataframe to "long" format for Seaborn plotting
    # This creates a 'Period' column distinguishing 'All Time' vs 'Since 2022'
    df_melted = top_20.melt(
        id_vars=['station_name'], 
        value_vars=['trips_all_time', 'trips_since_2022'],
        var_name='Period', 
        value_name='Trips'
    )
    
    df_melted['Period'] = df_melted['Period'].replace({
        'trips_all_time': 'All Time',
        'trips_since_2022': 'Since 2022'
    })

    plt.figure(figsize=(12, 10))
    sns.set_theme(style="whitegrid")
    
    chart = sns.barplot(
        data=df_melted,
        x='Trips',
        y='station_name',
        hue='Period',
        palette={'All Time': '#95a5a6', 'Since 2022': '#3498db'},
        alpha=0.9
    )

    plt.title('Top 20 Indego Stations: All Time vs. Recent (Since 2022)', fontsize=16, pad=20)
    plt.xlabel('Number of Trips', fontsize=12)
    plt.ylabel('')
    plt.legend(title='Time Period')

    # Add counts at the end of bars (optional polish)
    for container in chart.containers:
        chart.bar_label(container, fmt='%d', padding=3, fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=300)
    print(f"Visualization saved to {OUTPUT_IMAGE}")

def run_analysis():
    fs = s3fs.S3FileSystem()
    
    df_stations = get_station_names(fs)
    
    print("Loading trip data...")
    trip_files = fs.glob(f"{S3_TRIPS_PATH}*trips*.parquet")
    if not trip_files:
        print("No trip data found.")
        return

    dataset = ds.dataset(trip_files, filesystem=fs, format="parquet")
    df_trips = dataset.to_table(columns=['start_station_id', 'start_time']).to_pandas()
    df_trips['station_id'] = df_trips['start_station_id'].astype(str)
    
    print(f"Analyzing {len(df_trips):,} trips...")
    all_time = df_trips['station_id'].value_counts().reset_index()
    all_time.columns = ['station_id', 'trips_all_time']
    
    since_2022 = df_trips[df_trips['start_time'] >= '2022-01-01']['station_id'].value_counts().reset_index()
    since_2022.columns = ['station_id', 'trips_since_2022']

    final_df = all_time.merge(since_2022, on='station_id', how='left')

    if df_stations is not None:
        final_df = final_df.merge(df_stations, on='station_id', how='left')
        # Use Name if available, else ID
        final_df['station_name'] = final_df['station_name'].fillna(final_df['station_id'])
    
    final_df['trips_since_2022'] = final_df['trips_since_2022'].fillna(0).astype(int)

    visualize_ranks(final_df)

if __name__ == "__main__":
    run_analysis()
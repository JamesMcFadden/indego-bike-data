import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from data_utils import load_indego_data

def ride_timing():

    df = load_indego_data(columns=['start_time', 'duration', 'passholder_type'])

    df['hour_bin'] = df['start_time'].dt.hour
    df['weekday_bin'] = df['start_time'].dt.weekday

    print(f"Plotting {len(df):,} trips by hour of day...")

    plt.figure(figsize=(12, 7))
    sns.set_theme(style="white")

    sns.histplot(
        df['hour_bin'], 
        bins=24,
        color='#34495e', 
        edgecolor='white',
        linewidth=0.5
    )

    plt.title(f'Distribution of Ride Occurance by hour', fontsize=16, pad=20)
    plt.xlabel('Hour of Day', fontsize=12)
    plt.ylabel('Frequency (Number of Rides)', fontsize=12)

    plt.legend()
    plt.tight_layout()

    output_file = f"../output/ride_timing/ride_timing_by_hour.png"
    plt.savefig(output_file, dpi=300)
    print(f"Success! Plot saved as {output_file}")



if __name__ == "__main__":
    ride_timing()
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from utils import load_indego_data

def ride_occurance_by_hour():

    df = load_indego_data(columns=['start_time', 'duration'])

    df['hour_bin'] = df['start_time'].dt.hour

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

    output_file = f"../output/ride_timing/ride_occurance_by_hour.png"
    plt.savefig(output_file, dpi=300)
    print(f"Success! Plot saved as {output_file}")


def ride_occurance_by_weekday():

    df = load_indego_data(columns=['start_time', 'duration'])
    df['weekday_bin'] = df['start_time'].dt.weekday
    print(f"Plotting {len(df):,} trips by weekday...")

    plt.figure(figsize=(12, 7))
    sns.set_theme(style="white")

    sns.histplot(
        df['weekday_bin'], 
        bins=7,
        color='#34495e', 
        edgecolor='white',
        linewidth=0.5
    )

    plt.title(f'Distribution of Ride Occurance by weekday', fontsize=16, pad=20)
    plt.xlabel('Weekday', fontsize=12)
    plt.ylabel('Frequency (Number of Rides)', fontsize=12)

    plt.legend()
    plt.tight_layout()

    output_file = f"../output/ride_timing/ride_occurance_by_weekday.png"
    plt.savefig(output_file, dpi=300)
    print(f"Success! Plot saved as {output_file}")


def ride_duration_by_hour():
    df = load_indego_data(columns=['start_time', 'duration'])
    df = df[df['duration'] <= 240]  # Filter out rides longer than 4 hours
    df['hour_bin'] = df['start_time'].dt.hour
    ride_duration_by_hour = df.groupby('hour_bin')['duration'].mean().reset_index()

    print(f"Plotting {len(df):,} trips by hour...")

    plt.figure(figsize=(12, 7))
    sns.set_theme(style="white")

    ax = sns.barplot(
        data=ride_duration_by_hour, 
        x='hour_bin', 
        y='duration', 
        palette="viridis",
        hue='hour_bin',
        legend=False
    )

    plt.title('Average Ride Duration by Hour of Day', fontsize=16, pad=20)
    plt.xlabel('Hour of Day (24-hour clock)', fontsize=12)
    plt.ylabel('Average Duration (Minutes)', fontsize=12)
    
    # Add a horizontal line for the overall daily average
    overall_mean = df['duration'].mean()
    plt.axhline(overall_mean, color='red', linestyle='--', alpha=0.6, label=f'Daily Avg: {overall_mean:.1f}m')
    plt.legend()

    # Label the bars with their values for clarity
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points',
                    fontsize=9)

    plt.tight_layout()

    output_file = f"../output/ride_timing/ride_duration_by_hour.png"
    plt.savefig(output_file, dpi=300)
    print(f"Success! Plot saved as {output_file}")


def ride_duration_by_weekday():
    df = load_indego_data(columns=['start_time', 'duration'])
    df = df[df['duration'] <= 240]  # Filter out rides longer than 4 hours
    df['weekday_bin'] = df['start_time'].dt.weekday
    ride_duration_by_weekday = df.groupby('weekday_bin')['duration'].mean().reset_index()
    print(f"Plotting {len(df):,} trips by weekday...")

    plt.figure(figsize=(12, 7))
    sns.set_theme(style="white")

    ax = sns.barplot(
        data=ride_duration_by_weekday, 
        x='weekday_bin', 
        y='duration', 
        palette="viridis",
        hue='weekday_bin',
        legend=False
    )

    plt.title('Average Ride Duration by Weekday', fontsize=16, pad=20)
    plt.xlabel('Weekday', fontsize=12)
    plt.ylabel('Average Duration (Minutes)', fontsize=12)
    
    # Add a horizontal line for the overall daily average
    overall_mean = df['duration'].mean()
    plt.axhline(overall_mean, color='red', linestyle='--', alpha=0.6, label=f'Daily Avg: {overall_mean:.1f}m')
    plt.legend()

    # Label the bars with their values for clarity
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points',
                    fontsize=9)

    plt.tight_layout()

    output_file = f"../output/ride_timing/ride_duration_by_weekday.png"
    plt.savefig(output_file, dpi=300)
    print(f"Success! Plot saved as {output_file}")


if __name__ == "__main__":
    pass
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from utils import load_indego_data


def duration(limit_minutes: int = 120):

    df = load_indego_data(columns=['start_time', 'duration'])

    with open("../output/duration/duration_stats.txt", "w") as file:
        file.write(f"Average ride time is {round(np.mean(df['duration']))} minutes\n")
        file.write(f"Median ride time is {round(np.median(df['duration']))} minutes\n")

    df_filtered = df[df['duration'] <= limit_minutes]
    
    print(f"Plotting {len(df_filtered):,} trips under {limit_minutes} minutes...")

    plt.figure(figsize=(12, 7))
    sns.set_theme(style="white")

    sns.histplot(
        df_filtered['duration'], 
        bins=min(limit_minutes, 200),
        color='#34495e', 
        kde=True, # Adds a kernel density line to see the 'smooth' trend
        edgecolor='white',
        linewidth=0.5
    )

    plt.title(f'Distribution of Ride Durations (Under {limit_minutes} mins)', fontsize=16, pad=20)
    plt.xlabel('Duration in Minutes', fontsize=12)
    plt.ylabel('Frequency (Number of Rides)', fontsize=12)
    
    # Add vertical line for the mean
    mean_val = df_filtered['duration'].mean()
    plt.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.1f}m')
    plt.legend()

    plt.tight_layout()

    output_file = f"../output/duration/ride_duration_up_to_{limit_minutes}_minutes.png"
    plt.savefig(output_file, dpi=300)
    print(f"Success! Plot saved as {output_file}")

if __name__ == "__main__":
    duration(180)
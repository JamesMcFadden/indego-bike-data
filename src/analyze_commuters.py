import pandas as pd
import matplotlib.pyplot as plt
import os

from data_utils import load_indego_data

def analyze_commuter_behavior():
    
    df = load_indego_data(columns=['start_time', 'passholder_type'])

    print(f"Data loaded. Total trips: {len(df):,}")

    df['hour'] = df['start_time'].dt.hour
    df['rider_group'] = df['passholder_type'].apply(
        lambda x: 'Commuter' if 'Indego' in str(x) else 'Casual'
    )

    hourly_counts = df.groupby(['hour', 'rider_group']).size().unstack()

    print("Generating plot...")
    plt.style.use('ggplot')
    ax = hourly_counts.plot(kind='line', figsize=(12, 6), linewidth=2)
    ax.set_title("Philadelphia Bike Share: Commuter vs. Casual Usage", fontsize=16)
    ax.set_xlabel("Hour of Day", fontsize=12)
    ax.set_ylabel("Total Number of Trips", fontsize=12)
    plt.xticks(range(0, 24))
    
    output_file = "commuter_analysis.png"
    plt.savefig(output_file)
    print(f"Done! Chart saved to {output_file}")

if __name__ == "__main__":
    analyze_commuter_behavior()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_utils import load_indego_data


def plot_monthly_rides():

    print("Fetching start_time data from S3...")
    df = load_indego_data(columns=['start_time'])
    
    if df.empty:
        print("No data found.")
        return

    df['start_time'] = pd.to_datetime(df['start_time'])
    df['month'] = df['start_time'].dt.to_period('M')
    
    monthly_counts = df.groupby('month').size()
    monthly_counts.index = monthly_counts.index.to_timestamp()

    print("Generating monthly trend plot...")
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="darkgrid")
    plt.plot(monthly_counts.index, monthly_counts.values, 
             marker='o', linestyle='-', color='#1abc9c', linewidth=2.5)
    plt.title('Total Indego Rides per Month', fontsize=16, pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Rides', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_file = "../output/usage_trends/monthly_ride_trends.png"
    plt.savefig(output_file, dpi=300)
    print(f"Success! Plot saved as {output_file}")


def plot_yearly_rides():

    print("Fetching start_time data from S3...")
    df = load_indego_data(columns=['start_time'])
    
    if df.empty:
        print("No data found.")
        return

    df['start_time'] = pd.to_datetime(df['start_time'])
    df['year'] = df['start_time'].dt.to_period('Y')
    yearly_counts = df.groupby('year').size()
    yearly_counts.index = yearly_counts.index.to_timestamp()

    print("Generating yearly trend plot...")
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="darkgrid")
    plt.plot(yearly_counts.index, yearly_counts.values, 
             marker='o', linestyle='-', color='#1abc9c', linewidth=2.5)
    plt.title('Total Indego Rides per Year', fontsize=16, pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Rides', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_file = "../output/usage_trends/yearly_ride_trends.png"
    plt.savefig(output_file, dpi=300)
    print(f"Success! Plot saved as {output_file}")

if __name__ == "__main__":
    plot_monthly_rides()
    plot_yearly_rides()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_utils import load_indego_data

def plot_yearly_rides():
    # 1. Load only the necessary column (Optimization)
    print("Fetching start_time data from S3...")
    df = load_indego_data(columns=['start_time'])
    
    if df.empty:
        print("No data found.")
        return

    # 2. Process Data
    # Ensure datetime format
    df['start_time'] = pd.to_datetime(df['start_time'])
    
    # Create a Year period (e.g., '2023')
    df['year'] = df['start_time'].dt.to_period('Y')
    
    # Count rides per year
    yearly_counts = df.groupby('year').size()
    
    # Convert index back to timestamp for better plotting
    yearly_counts.index = yearly_counts.index.to_timestamp()

    # 3. Visualization
    print("Generating yearly trend plot...")
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="darkgrid")
    
    # Create the line plot
    plt.plot(yearly_counts.index, yearly_counts.values, 
             marker='o', linestyle='-', color='#1abc9c', linewidth=2.5)

    # 4. Formatting
    plt.title('Total Indego Rides per Year', fontsize=16, pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Rides', fontsize=12)
    
    # Format the X-axis to show years clearly
    plt.xticks(rotation=45)
    
    # Add a horizontal grid for easier value estimation
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    
    # 5. Save the result
    output_file = "../output/yearly_ride_trends.png"
    plt.savefig(output_file, dpi=300)
    print(f"Success! Plot saved as {output_file}")

if __name__ == "__main__":
    plot_yearly_rides()
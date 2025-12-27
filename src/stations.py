import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils import load_indego_data


def station_analysis():

    print("Fetching station data from S3...")
    df = load_indego_data(columns=['go_live_date', 'status'], folder='stations')
    
    if df.empty:
        print("No data found.")
        return

    active_df = df[df['status'] == 'Active'].copy()
    active_df = active_df.sort_values('go_live_date')
    
    growth = active_df.groupby('go_live_date').size().cumsum().reset_index()
    growth.columns = ['date', 'station_count']
    
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")
    
    # We use a 'step' plot because station counts change at discrete moments in time
    plt.plot(growth['date'], growth['station_count'], 
             drawstyle='steps-post', color='#2ecc71', linewidth=2.5, label='Active Stations')
    
    # Fill the area for better visual density
    plt.fill_between(growth['date'], growth['station_count'], 
                     step="post", alpha=0.2, color='#2ecc71')
    
    plt.title('Indego Network Expansion: Active Stations Over Time', fontsize=16, pad=20)
    plt.xlabel('Launch Year', fontsize=12)
    plt.ylabel('Total Number of Stations', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Annotate the final count
    final_count = growth['station_count'].iloc[-1]
    final_date = growth['date'].iloc[-1].strftime('%Y-%m')
    plt.annotate(f'Total: {final_count}\n({final_date})', 
                 xy=(growth['date'].iloc[-1], final_count),
                 xytext=(-60, 10), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='black'))

    plt.tight_layout()
    plt.savefig('../output/stations/active_stations_over_time.png', dpi=300)
    with open("../output/stations/station_stats.txt", "w") as file:
        file.write(f"Current number of active stations: {final_count}\n")


if __name__ == "__main__":
    station_analysis()
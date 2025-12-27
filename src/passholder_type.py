import matplotlib.pyplot as plt
import seaborn as sns

from utils import load_indego_data

def passholder_behavior():
    
    df = load_indego_data(columns=['start_time', 'passholder_type', 'plan_duration'])

    print(f"Data loaded. Total trips: {len(df):,}")

    duration_counts = df['plan_duration'].value_counts()
    with open('../output/passholder_type/counts_plan_duration.txt', 'w') as f:
        f.write("Indego Plan Duration Analysis\n")
        f.write("=" * 30 + "\n")
        f.write(duration_counts.to_string())
        f.write("\n" + "=" * 30)

    pass_holder_type_counts = df['passholder_type'].value_counts()
    with open('../output/passholder_type/counts_passholder_type.txt', 'w') as f:
        f.write("Indego Passholder Type Analysis\n")
        f.write("=" * 30 + "\n")
        f.write(pass_holder_type_counts.to_string())
        f.write("\n" + "=" * 30)

    df['hour'] = df['start_time'].dt.hour
    day_pass_by_hour = df[df['passholder_type']=="Day Pass"].groupby('hour')['passholder_type'].count()
    indego_30_by_hour = df[df['passholder_type']=="Indego30"].groupby('hour')['passholder_type'].count()
    indego_365_by_hour = df[df['passholder_type']=="Indego365"].groupby('hour')['passholder_type'].count()

    plt.style.use('ggplot')
    sns.set_theme(style="white")
    plt.plot(day_pass_by_hour, label='Day Pass')
    plt.plot(indego_30_by_hour, label='Indego30')
    plt.plot(indego_365_by_hour, label='Indego365')
    plt.title("Ride Occurance by Hour", fontsize=16)
    plt.xlabel("Hour of Day", fontsize=12)
    plt.ylabel("Total Number of Trips", fontsize=12)
    plt.xticks(range(0, 24))
    plt.legend()
    plt.tight_layout()
    
    output_file = "../output/passholder_type/passholder_usage_by_hour.png"
    plt.savefig(output_file)
    print(f"Done! Chart saved to {output_file}")


    df['weekday'] = df['start_time'].dt.weekday
    day_pass_by_weekday = df[df['passholder_type']=="Day Pass"].groupby('weekday')['passholder_type'].count()
    indego_30_by_weekday = df[df['passholder_type']=="Indego30"].groupby('weekday')['passholder_type'].count()
    indego_365_by_weekday = df[df['passholder_type']=="Indego365"].groupby('weekday')['passholder_type'].count()

    plt.style.use('ggplot')
    sns.set_theme(style="white")
    plt.plot(day_pass_by_weekday, label='Day Pass')
    plt.plot(indego_30_by_weekday, label='Indego30')
    plt.plot(indego_365_by_weekday, label='Indego365')
    plt.title("Ride Occurance by Weekday", fontsize=16)
    plt.xlabel("Weekday", fontsize=12)
    plt.ylabel("Total Number of Trips", fontsize=12)
    plt.xticks(range(0, 7))
    plt.legend()
    plt.tight_layout()
    
    output_file = "../output/passholder_type/passholder_usage_by_weekday.png"
    plt.savefig(output_file)
    print(f"Done! Chart saved to {output_file}")

if __name__ == "__main__":
    passholder_behavior()
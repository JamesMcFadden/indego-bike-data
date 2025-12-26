import matplotlib.pyplot as plt

from data_utils import load_indego_data

def bike_type_comparison():
    
    df = load_indego_data(columns=['start_time', 'bike_type'])


    df_standard = df[df['bike_type'] == 'standard']
    df_electric = df[df['bike_type'] == 'electric']

    # print(round(100*df['bike_type'].value_counts()['standard']/len(df)), "% of rides were on standard bikes")

    with open("./output/bike_type/bike_comparison.txt", "w") as file:
        file.write(f"{round(100*df['bike_type'].value_counts()['standard']/len(df))}% of rides were on standard bikes\n")

if __name__ == "__main__":
    bike_type_comparison()
import pandas as pd
import os
import glob
from dotenv import load_dotenv

# Load environment variables (AWS keys, etc.)
load_dotenv()

# Configuration
DATA_FOLDER = 'data_trips'
BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

def clean_file(file_path):
    # Get the filename without the path or extension (e.g., 'indego-trips-2025-q3')
    base_name = os.path.basename(file_path).replace('.csv', '')
    s3_path = f's3://{BUCKET_NAME}/processed/trips/{base_name}.parquet'

    print(f"\n--- Processing {base_name} ---")

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Convert 'start_time' and 'end_time' columns to datetime
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    
    # Convert categorical columns to category type
    categorical_cols = ['trip_route_category', 'passholder_type', 'bike_type']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')

    # Convert 'bike_id' column to string
    df['bike_id'] = df['bike_id'].astype(str)
    
    # Remove duplicate rows based on 'trip_id'
    df = df.drop_duplicates(subset=['trip_id'])
    
    return df, base_name, s3_path

def upload_file(df, base_name, s3_path):

        try:
            # Upload to S3 as Parquet
            print(f"Uploading to {s3_path}...")
            df.to_parquet(s3_path, index=False)
            print(f"Successfully processed and uploaded {base_name}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    # Find all CSV files in the data folder
    search_path = os.path.join(DATA_FOLDER, "*.csv")
    csv_files = glob.glob(search_path)

    if not csv_files:
        print(f"No CSV files found in {DATA_FOLDER}")

    print(f"Found {len(csv_files)} files to process.")

    for file_path in csv_files:
        df, base_name, s3_path = clean_file(file_path)
        upload_file(df, base_name, s3_path)
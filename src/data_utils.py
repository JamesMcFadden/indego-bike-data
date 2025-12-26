import pandas as pd
import s3fs
import pyarrow.dataset as ds
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

def load_indego_data(columns=None, folder="trips", start_year=None):
    """
    Centralized loader for Indego data. 
    Change S3 logic here, and it updates everywhere.
    """
    fs = s3fs.S3FileSystem()

    path = f"{BUCKET_NAME}/processed/{folder}"
    
    # Find files
    files = fs.glob(os.path.join(path, "*.parquet"))

    # 2. Filter by Year (if requested)
    if start_year:
        filtered_files = []
        for f in files:
            # Extract year from filename using Regex (looks for 4 digits)
            # Matches '2023' in 'indego-trips-2023-q1.parquet'
            match = re.search(r'(\d{4})', f)
            if match:
                file_year = int(match.group(1))
                if file_year >= start_year:
                    filtered_files.append(f)
        
        if not filtered_files:
            print(f"No files found from {start_year} onwards.")
            return pd.DataFrame()
            
        print(f"Filtered down to {len(filtered_files)} files (Year >= {start_year}).")
        files_to_load = filtered_files
    else:
        files_to_load = files
    
    # Load via PyArrow
    dataset = ds.dataset(files_to_load, filesystem=fs, format="parquet")
    table = dataset.to_table(columns=columns)
    df = table.to_pandas()
    return df

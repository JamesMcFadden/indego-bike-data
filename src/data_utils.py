import pandas as pd
import s3fs
import pyarrow.dataset as ds
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

def load_indego_data(columns=None, folder="trips"):
    """
    Centralized loader for Indego data. 
    Change S3 logic here, and it updates everywhere.
    """
    fs = s3fs.S3FileSystem()

    path = f"{BUCKET_NAME}/processed/{folder}"
    
    # Find files
    files = fs.glob(os.path.join(path, "*.parquet"))
    
    # Load via PyArrow
    dataset = ds.dataset(files, filesystem=fs, format="parquet")
    table = dataset.to_table(columns=columns)
    df = table.to_pandas()
    return df

from data_pipeline import load_data,clean_data,add_columns
from config import RAW_DATA_PATH
if __name__ == '__main__':
    raw_df = load_data(RAW_DATA_PATH)
    clean_df = clean_data(raw_df)
    clean_df = add_columns(clean_df)

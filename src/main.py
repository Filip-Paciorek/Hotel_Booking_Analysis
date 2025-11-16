from data_pipeline import load_data,clean_data,add_columns,aggregate_data
import pandas as pd
from config import RAW_DATA_PATH,PROCESSED_DATA_PATH
def process_chunk(chunk):
    """Processes a chunk of data"""
    clean_chunk = clean_data(chunk)
    clean_chunk = add_columns(clean_chunk)
    clean_chunk = aggregate_data(clean_chunk)
    return clean_chunk
if __name__ == '__main__':
    #sets base size of a chunk
    chunk_size = 20000
    list_of_aggregated_chunks = []
    #go over all the data
    csv_iterator = pd.read_csv(RAW_DATA_PATH,chunksize=chunk_size)
    for i,chunk in enumerate(csv_iterator):
        print(f'PROCESSING CHUNK NR.{i+1}')
        processed_chunk = process_chunk(chunk)
        list_of_aggregated_chunks.append(processed_chunk)
    print('ALL CHUNKS AGGREGATED. MERGING...')
    #aggregate the chunks
    df_aggregated = pd.concat(list_of_aggregated_chunks,ignore_index=True)

    grouping_columns = [
    #SLICERS COLUMNS
    'hotel','arrival_date_year','distribution_channel','reserved_room_type',   
    #AXIS COLUMNS
    'arrival_date_month','market_segment','country','lead_time_group','customer_segment','required_car_parking_spaces','is_repeated_guest','adr_bucket']
    #now aggregate again to lessen the num of rows
    agg_definitions = {
        'total_revenue': pd.NamedAgg(column='total_revenue', aggfunc='sum'),
        'total_nights': pd.NamedAgg(column='total_nights', aggfunc='sum'),
        'cancellations': pd.NamedAgg(column='cancellations', aggfunc='sum'),
        'avg_adr': pd.NamedAgg(column='avg_adr', aggfunc='mean'),
        'total_bookings': pd.NamedAgg(column='total_bookings', aggfunc='sum') 
    }
    df_final_report = df_aggregated.groupby(grouping_columns,observed=True).agg(**agg_definitions).reset_index()
    total_rows = df_final_report['total_bookings'].sum()
    print(f'ALL CHUNKS MERGED. SIZE REDUCED FROM {total_rows} TO {df_final_report.shape[0]}') 
    print(f'CALCULATING FINAL COLUMNS...')
    #add columns to improve speed of excel spreadsheet
    df_final_report['cancellation_rate'] = df_final_report['cancellations'] / df_final_report['total_bookings']
    df_final_report['avg_revenue_per_booking'] = df_final_report['total_revenue'] / df_final_report['total_bookings']
    df_final_report['avg_stay_length'] = df_final_report['total_nights'] / df_final_report['total_bookings']
    print(f'PARSING TO CSV...')
    #Parse the file
    df_final_report.to_csv(PROCESSED_DATA_PATH,index=False)

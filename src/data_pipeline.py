import pandas as pd
def load_data(path):
    """Loads data from CSV."""
    df = pd.read_csv(path)
    return df
def clean_data(df):
    """Gets rid of missing values and useless columns, simplifies by merging columns"""
    df = df[df['country'].notna()]
    df = df[df['children'].notna()]
    df = df[df['adr'] >= 0]
    df['total_nights'] = (df['stays_in_weekend_nights'] + df['stays_in_week_nights'])
    df = df[df['total_nights']>0]
    df = df.drop(columns=['agent','company','reservation_status','reservation_status_date','arrival_date_week_number','arrival_date_day_of_month','deposit_type','assigned_room_type','booking_changes','stays_in_weekend_nights','stays_in_week_nights'],axis=1)
    return df
def assign_customer_segment(row):
    total_people = row['adults'] + row['children'] + row['babies']
    if row['adults'] ==1 and total_people == 1:
        return 'Solo'
    if row['adults'] == 2 and total_people == 2:
        return 'Couple'
    if row['children'] > 0 or row['babies'] > 0:
        return 'Family'
    if row['adults'] == 0:
        return 'Invalid'
    return 'Other'

def add_columns(df):
    """Creates new columns to make data easier to present/analyse"""
    df['revenue'] = df['adr'] * df['total_nights']
    df['customer_segment'] = df.apply(assign_customer_segment,axis=1)
    bins = [-1,75,125,200,float('inf')]
    labels = ['Budget (0-75)','Standard (76-125)','Premium (126-200)','Luxury (201+)']
    df['adr_bucket'] = pd.cut(df['adr'], bins=bins, labels=labels, right=True)
    bins = [-1, 0, 7, 30, 90, 180, 800]
    labels = ['Same Day', '1-7 Days', '8-30 Days', '1-3 Months', '3-6 Months', '6+ Months']
    df['lead_time_group'] = pd.cut(df['lead_time'], bins=bins, labels=labels, right=True)
    return df
        

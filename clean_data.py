"""
Part 1: Data Cleaning Script
This script cleans messy customer and order data

What it does:
- Removes duplicate customers
- Validates email addresses
- Fixes date formats
- Handles missing values
- Generates cleaning reports
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings

# File paths - where to find and save data
RAW_DATA_PATH = Path('data/raw')
PROCESSED_DATA_PATH = Path('data/processed')
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)


def parse_date(val):
    """Parse date supporting multiple formats"""
    if pd.isna(val):
        return pd.NaT
    
    # Try different date formats commonly found in data
    formats = ['%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y']
    for fmt in formats:
        try:
            return pd.to_datetime(val, format=fmt)
        except:
            continue
    
    # If none work, log a warning and return NaT (Not a Time)
    warnings.warn(f"Could not parse date: {val}")
    return pd.NaT


def validate_email(email):
    """Check if email is valid (contains @ and .)"""
    if pd.isna(email):
        return False
    email_str = str(email).strip()
    # Simple check: email must have @ and .
    return '@' in email_str and '.' in email_str


def clean_customers(input_path, output_path):
    """Clean customers.csv according to specifications"""
    print("\n" + "="*60)
    print("CLEANING CUSTOMERS DATA")
    print("="*60)
    
    # Load data
    df = pd.read_csv(input_path)
    rows_before = len(df)
    nulls_before = df.isnull().sum()
    
    print(f"\nRows before cleaning: {rows_before}")
    print(f"\nNull counts before cleaning:")
    print(nulls_before)
    
    # 1. Remove duplicates based on customer_id, keeping most recent signup_date
    df['signup_date'] = df['signup_date'].apply(parse_date)
    df_sorted = df.sort_values('signup_date', ascending=False)
    duplicates_removed = len(df) - len(df_sorted.drop_duplicates(subset=['customer_id'], keep='first'))
    df = df_sorted.drop_duplicates(subset=['customer_id'], keep='first')
    
    # 2. Standardize email addresses to lowercase
    df['email'] = df['email'].str.lower().str.strip()
    
    # 3. Flag invalid emails
    df['is_valid_email'] = df['email'].apply(validate_email)
    
    # 4. Parse signup_date (already done above)
    df['signup_date'] = df['signup_date'].dt.strftime('%Y-%m-%d')
    
    # 5. Strip whitespace from name and region
    df['name'] = df['name'].str.strip()
    df['region'] = df['region'].str.strip()
    
    # 6. Fill missing region with 'Unknown'
    df['region'] = df['region'].fillna('Unknown')
    
    # Save cleaned data
    df = df.sort_values('customer_id').reset_index(drop=True)
    df.to_csv(output_path, index=False)
    
    # Print report
    rows_after = len(df)
    nulls_after = df.isnull().sum()
    
    print(f"\nRows after cleaning: {rows_after}")
    print(f"Duplicate rows removed: {duplicates_removed}")
    print(f"\nNull counts after cleaning:")
    print(nulls_after)
    print(f"\nInvalid emails flagged: {(~df['is_valid_email']).sum()}")
    print(f"\nCleaned data saved to: {output_path}")


def clean_orders(input_path, output_path):
    """Clean orders.csv according to specifications"""
    print("\n" + "="*60)
    print("CLEANING ORDERS DATA")
    print("="*60)
    
    # Load data
    df = pd.read_csv(input_path)
    rows_before = len(df)
    nulls_before = df.isnull().sum()
    
    print(f"\nRows before cleaning: {rows_before}")
    print(f"\nNull counts before cleaning:")
    print(nulls_before)
    
    # 1. Parse order_date with multiple formats
    df['order_date'] = df['order_date'].apply(parse_date)
    
    # 2. Drop rows where both customer_id and order_id are null
    unrecoverable = df['customer_id'].isnull() & df['order_id'].isnull()
    rows_dropped = unrecoverable.sum()
    df = df[~unrecoverable]
    
    # 3. Fill missing amount with median amount grouped by product
    median_by_product = df.groupby('product')['amount'].median()
    df['amount'] = df.apply(
        lambda row: median_by_product.get(row['product'], row['amount']) 
        if pd.isna(row['amount']) else row['amount'],
        axis=1
    )
    
    # 4. Normalize status column
    status_mapping = {
        'done': 'completed',
        'canceled': 'cancelled',
        'complete': 'completed',
        'pend': 'pending'
    }
    df['status'] = df['status'].str.lower().str.strip()
    df['status'] = df['status'].replace(status_mapping)
    
    # Ensure only valid statuses
    valid_statuses = {'completed', 'pending', 'cancelled', 'refunded'}
    df['status'] = df['status'].apply(lambda x: x if x in valid_statuses else 'pending')
    
    # 5. Add derived column order_year_month
    df['order_year_month'] = df['order_date'].dt.strftime('%Y-%m')
    
    # Format order_date
    df['order_date'] = df['order_date'].dt.strftime('%Y-%m-%d')
    
    # Save cleaned data
    df = df.sort_values('order_id').reset_index(drop=True)
    df.to_csv(output_path, index=False)
    
    # Print report
    rows_after = len(df)
    nulls_after = df.isnull().sum()
    
    print(f"\nRows after cleaning: {rows_after}")
    print(f"Unrecoverable rows dropped: {rows_dropped}")
    print(f"\nNull counts after cleaning:")
    print(nulls_after)
    print(f"\nCleaned data saved to: {output_path}")


def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("DATA CLEANING PIPELINE")
    print("="*60)
    
    # Clean customers
    clean_customers(
        RAW_DATA_PATH / 'customers.csv',
        PROCESSED_DATA_PATH / 'customers_clean.csv'
    )
    
    # Clean orders
    clean_orders(
        RAW_DATA_PATH / 'orders.csv',
        PROCESSED_DATA_PATH / 'orders_clean.csv'
    )
    
    print("\n" + "="*60)
    print("CLEANING COMPLETE!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()

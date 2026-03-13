"""
Part 2: Data Analysis Script
This script combines cleaned data and generates insights

What it does:
- Merges customer, order, and product data
- Calculates monthly revenue
- Finds top customers
- Analyzes by category and region
"""

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# File paths
RAW_DATA_PATH = Path('data/raw')
PROCESSED_DATA_PATH = Path('data/processed')


def load_data(filepath):
    """Load CSV with error handling"""
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"File is empty: {filepath}")


def merge_datasets():
    """Merge cleaned datasets"""
    print("\n" + "="*60)
    print("MERGING DATASETS")
    print("="*60)
    
    # Load cleaned data
    customers = load_data(PROCESSED_DATA_PATH / 'customers_clean.csv')
    orders = load_data(PROCESSED_DATA_PATH / 'orders_clean.csv')
    products = load_data(RAW_DATA_PATH / 'products.csv')
    
    print(f"\nLoaded {len(customers)} customers")
    print(f"Loaded {len(orders)} orders")
    print(f"Loaded {len(products)} products")
    
    # Left-join orders onto customers
    orders_with_customers = pd.merge(
        orders,
        customers,
        on='customer_id',
        how='left'
    )
    
    # Report unmatched customers
    no_customer = orders_with_customers['name'].isnull().sum()
    print(f"\nOrders with no matching customer: {no_customer}")
    
    # Left-join products onto orders_with_customers
    full_data = pd.merge(
        orders_with_customers,
        products,
        left_on='product',
        right_on='product_name',
        how='left'
    )
    
    # Report unmatched products
    no_product = full_data['product_name'].isnull().sum()
    print(f"Orders with no matching product: {no_product}")
    
    print(f"\nFull merged dataset: {len(full_data)} rows")
    
    return full_data


def monthly_revenue_analysis(df):
    """Compute monthly revenue trend"""
    print("\n" + "="*60)
    print("MONTHLY REVENUE ANALYSIS")
    print("="*60)
    
    # Filter completed orders only
    completed = df[df['status'] == 'completed'].copy()
    
    # Group by order_year_month
    monthly = completed.groupby('order_year_month').agg({
        'amount': 'sum'
    }).reset_index()
    
    monthly.columns = ['month', 'total_revenue']
    monthly = monthly.sort_values('month')
    
    # Save output
    output_path = PROCESSED_DATA_PATH / 'monthly_revenue.csv'
    monthly.to_csv(output_path, index=False)
    
    print(f"\nGenerated monthly revenue data: {len(monthly)} months")
    print(f"Saved to: {output_path}")
    
    return monthly


def top_customers_analysis(df):
    """Identify top 10 customers by total spend"""
    print("\n" + "="*60)
    print("TOP CUSTOMERS ANALYSIS")
    print("="*60)
    
    # Filter completed orders only
    completed = df[df['status'] == 'completed'].copy()
    
    # Convert order_date to datetime for churn calculation
    completed['order_date'] = pd.to_datetime(completed['order_date'])
    
    # Get latest date in dataset
    latest_date = completed['order_date'].max()
    churn_threshold = latest_date - timedelta(days=90)
    
    # Group by customer
    customer_stats = completed.groupby('customer_id').agg({
        'amount': 'sum',
        'name': 'first',
        'region': 'first',
        'order_date': 'max'
    }).reset_index()
    
    customer_stats.columns = ['customer_id', 'total_spend', 'name', 'region', 'last_order_date']
    
    # Add churn indicator
    customer_stats['churned'] = customer_stats['last_order_date'] < churn_threshold
    
    # Get top 10
    top_10 = customer_stats.nlargest(10, 'total_spend')
    
    # Drop last_order_date for output
    top_10 = top_10[['customer_id', 'name', 'region', 'total_spend', 'churned']]
    
    # Save output
    output_path = PROCESSED_DATA_PATH / 'top_customers.csv'
    top_10.to_csv(output_path, index=False)
    
    print(f"\nIdentified top 10 customers")
    print(f"Churned customers in top 10: {top_10['churned'].sum()}")
    print(f"Saved to: {output_path}")
    
    return top_10


def category_performance_analysis(df):
    """Analyze performance by product category"""
    print("\n" + "="*60)
    print("CATEGORY PERFORMANCE ANALYSIS")
    print("="*60)
    
    # Filter completed orders with valid category
    completed = df[(df['status'] == 'completed') & df['category'].notna()].copy()
    
    # Group by category
    category_stats = completed.groupby('category').agg({
        'amount': ['sum', 'mean', 'count']
    }).reset_index()
    
    category_stats.columns = ['category', 'total_revenue', 'avg_order_value', 'num_orders']
    category_stats = category_stats.sort_values('total_revenue', ascending=False)
    
    # Save output
    output_path = PROCESSED_DATA_PATH / 'category_performance.csv'
    category_stats.to_csv(output_path, index=False)
    
    print(f"\nAnalyzed {len(category_stats)} categories")
    print(f"Saved to: {output_path}")
    
    return category_stats


def regional_analysis(df):
    """Analyze metrics by region"""
    print("\n" + "="*60)
    print("REGIONAL ANALYSIS")
    print("="*60)
    
    # Filter completed orders with valid region
    completed = df[(df['status'] == 'completed') & df['region'].notna()].copy()
    
    # Group by region
    regional_stats = completed.groupby('region').agg({
        'customer_id': 'nunique',
        'order_id': 'count',
        'amount': 'sum'
    }).reset_index()
    
    regional_stats.columns = ['region', 'num_customers', 'num_orders', 'total_revenue']
    
    # Calculate average revenue per customer
    regional_stats['avg_revenue_per_customer'] = (
        regional_stats['total_revenue'] / regional_stats['num_customers']
    ).round(2)
    
    regional_stats = regional_stats.sort_values('total_revenue', ascending=False)
    
    # Save output
    output_path = PROCESSED_DATA_PATH / 'regional_analysis.csv'
    regional_stats.to_csv(output_path, index=False)
    
    print(f"\nAnalyzed {len(regional_stats)} regions")
    print(f"Saved to: {output_path}")
    
    return regional_stats


def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("DATA ANALYSIS PIPELINE")
    print("="*60)
    
    # Merge datasets
    full_data = merge_datasets()
    
    # Run analyses
    monthly_revenue_analysis(full_data)
    top_customers_analysis(full_data)
    category_performance_analysis(full_data)
    regional_analysis(full_data)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()

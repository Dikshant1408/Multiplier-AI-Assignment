"""
Backend API - Serves data to the frontend
This is a simple REST API that reads CSV files and returns JSON data
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

# Create the API app
app = FastAPI(title="Sales Dashboard API")

# Allow frontend to access this API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Where to find the data files
DATA_PATH = Path(__file__).parent.parent / 'data' / 'processed'


def load_csv_data(filename):
    """Load CSV file with error handling"""
    filepath = DATA_PATH / filename
    try:
        df = pd.read_csv(filepath)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Data file not found: {filename}. Please run data cleaning and analysis scripts first."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading data: {str(e)}"
        )


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/api/revenue")
def get_revenue():
    """Get monthly revenue data"""
    return load_csv_data('monthly_revenue.csv')


@app.get("/api/top-customers")
def get_top_customers():
    """Get top 10 customers by total spend"""
    return load_csv_data('top_customers.csv')


@app.get("/api/categories")
def get_categories():
    """Get category performance data"""
    return load_csv_data('category_performance.csv')


@app.get("/api/regions")
def get_regions():
    """Get regional analysis data"""
    return load_csv_data('regional_analysis.csv')


@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Data Analysis Dashboard API",
        "endpoints": {
            "health": "/health",
            "revenue": "/api/revenue",
            "top_customers": "/api/top-customers",
            "categories": "/api/categories",
            "regions": "/api/regions"
        }
    }

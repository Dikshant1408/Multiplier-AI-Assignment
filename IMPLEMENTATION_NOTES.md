# Implementation Notes

## Project Overview

This project implements a complete data analysis pipeline with:
- Data cleaning and validation
- Multi-dataset merging and analysis
- REST API backend
- Interactive React dashboard

## Technical Decisions

### Part 1: Data Cleaning

**Date Parsing Strategy:**
- Implemented custom parser supporting 3 formats: YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY
- Returns `pd.NaT` for unparseable dates with warning
- Used `apply()` for flexibility over `pd.to_datetime()` with multiple formats

**Email Validation:**
- Basic validation checking for '@' and '.' presence
- Flagged invalid emails rather than removing them (preserves data)
- Standardized to lowercase for consistency

**Duplicate Handling:**
- Sorted by `signup_date` descending before deduplication
- Kept most recent record using `drop_duplicates(keep='first')`

**Missing Data Strategy:**
- Region: Filled with 'Unknown' (categorical default)
- Amount: Filled with median grouped by product (preserves distribution)
- Unrecoverable rows: Dropped only when both customer_id and order_id are null

### Part 2: Data Analysis

**Merge Strategy:**
- Used explicit left joins to preserve all order records
- Reported unmatched records for data quality monitoring
- Matched products on `product` to `product_name` field

**Churn Definition:**
- 90-day threshold from latest date in dataset
- Based on last completed order date
- Binary flag for easy filtering

**Analysis Outputs:**
1. Monthly Revenue: Aggregated completed orders by year-month
2. Top Customers: Ranked by total spend with churn status
3. Category Performance: Revenue, avg order value, and count by category
4. Regional Analysis: Customer count, orders, revenue, and per-customer metrics

### Part 3: Full Stack Dashboard

**Backend (FastAPI):**
- Chose FastAPI for automatic API documentation and type validation
- Implemented CORS for cross-origin requests
- Used pathlib for cross-platform path handling
- Error handling with appropriate HTTP status codes

**Frontend (React + Recharts):**
- Recharts chosen for declarative chart syntax and responsiveness
- Implemented loading and error states for better UX
- Sortable table for customer data exploration
- Responsive grid layout adapting to mobile screens

**Design Patterns:**
- Separation of concerns: data processing, API, and UI layers
- Configuration at top of files (no hardcoded paths)
- Error handling at each layer
- Modular functions for testability

## Bonus Features Implemented

1. ✅ **Pytest Unit Tests** (tests/test_clean_data.py)
   - Date parsing tests for all formats
   - Email validation tests
   - Integration tests for cleaning logic

2. ✅ **Docker Support** (Dockerfile + docker-compose.yml)
   - Containerized backend with volume mount for data
   - Health check endpoint
   - Easy deployment with `docker-compose up`

3. ✅ **Sortable Table** (Frontend)
   - Click column headers to sort
   - Visual indicators for sort direction
   - Maintains state across re-renders

4. ✅ **Enhanced Error Handling**
   - User-friendly error messages
   - Retry functionality
   - Loading states with spinner

## Code Quality

**PEP 8 Compliance:**
- 4-space indentation
- Max line length 100 characters
- Descriptive variable names
- Docstrings for all functions

**Best Practices:**
- Type hints where beneficial
- Comprehensive error handling
- Logging and reporting
- No raw loops where pandas methods work
- Explicit merge parameters

## Performance Considerations

- Used pandas vectorized operations over loops
- Efficient groupby aggregations
- Minimal data copying
- CSV format for simplicity (could upgrade to Parquet for larger datasets)

## Testing

Run tests with:
```bash
pytest tests/ -v
```

Current test coverage:
- Date parsing: 5 tests
- Email validation: 5 tests
- Data cleaning integration: 3 tests

## Deployment

### Local Development
```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend
cd frontend
npm start
```

### Docker Deployment
```bash
# Build and run
docker-compose up --build

# Stop
docker-compose down
```

## Future Enhancements

1. **Database Integration**: Replace CSV with PostgreSQL/MongoDB
2. **Authentication**: Add JWT-based auth for API
3. **Caching**: Implement Redis for frequently accessed data
4. **Real-time Updates**: WebSocket for live dashboard updates
5. **Advanced Analytics**: ML models for churn prediction
6. **Export Functionality**: Download reports as PDF/Excel
7. **Date Range Filters**: Interactive filtering on dashboard
8. **Search Functionality**: Full-text search across datasets

## Known Limitations

1. **Data Volume**: Current implementation suitable for datasets up to ~100K rows
2. **Concurrency**: Single-threaded processing (could parallelize with Dask)
3. **Validation**: Basic email validation (could use regex for RFC compliance)
4. **Time Zones**: Assumes all dates in same timezone
5. **Currency**: Assumes single currency (USD)

## Dependencies

### Python
- pandas 2.1.3 - Data manipulation
- fastapi 0.104.1 - Web framework
- uvicorn 0.24.0 - ASGI server
- pytest 7.4.3 - Testing framework

### JavaScript
- react 18.2.0 - UI framework
- recharts 2.10.3 - Charts
- axios 1.6.2 - HTTP client

## File Structure

```
.
├── data/
│   ├── raw/              # Original CSV files
│   └── processed/        # Cleaned outputs
├── backend/              # FastAPI application
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # React application
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── public/
│   └── package.json
├── tests/                # Unit tests
│   ├── __init__.py
│   └── test_clean_data.py
├── clean_data.py         # Part 1 script
├── analyze.py            # Part 2 script
├── setup.py              # Setup automation
├── docker-compose.yml    # Docker orchestration
└── README.md             # User documentation
```

## Time Spent

- Part 1 (Data Cleaning): ~2 hours
- Part 2 (Analysis): ~2 hours
- Part 3 (Full Stack): ~4 hours
- Bonus Features: ~2 hours
- Documentation: ~1 hour
- **Total: ~11 hours**

## Assumptions

1. All monetary values in USD
2. Dates in dataset span reasonable range (no future dates)
3. Product names in orders match product_name in products.csv
4. Customer IDs are unique identifiers
5. Order IDs are unique and sequential
6. Status values are limited to known set
7. Region names are consistent (no typos like "Nrth" vs "North")
8. Email addresses follow basic format (no internationalized domains)

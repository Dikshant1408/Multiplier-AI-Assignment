# Sales Data Dashboard - Full Stack Assignment

A complete data analysis and visualization project built with Python and React.

## What This Project Does

This project takes messy sales data (customers, orders, products) and:
1. Cleans and validates the data
2. Analyzes it to find insights
3. Displays everything in an interactive web dashboard

## Quick Start (3 Steps!)

### Step 1: Process the Data
```bash
python clean_data.py
python analyze.py
```

### Step 2: Start the Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Keep this terminal open!

### Step 3: Start the Frontend
Open a NEW terminal:
```bash
cd frontend
npm install
npm start
```

Your browser will open automatically to http://localhost:3000 🎉

## What You'll See

The dashboard shows:
- 📈 **Revenue Chart** - How sales changed over time
- 👥 **Top Customers** - Best customers (click headers to sort!)
- 📦 **Product Categories** - Which products sell best
- 🌍 **Regional Data** - Sales by location

## Project Structure (Simple!)

```
├── data/
│   ├── raw/           # Original messy data
│   └── processed/     # Cleaned data
├── backend/           # Python API (FastAPI)
├── frontend/          # React website
├── clean_data.py      # Cleans the data
└── analyze.py         # Analyzes the data
```

## Technologies Used

**Backend:**
- Python 3.9+
- Pandas (data processing)
- FastAPI (web API)

**Frontend:**
- React (user interface)
- Recharts (charts and graphs)
- CSS (styling)

## Assignment Requirements Met

✅ Part 1: Data Cleaning (30 points)
- Removes duplicate customers
- Validates email addresses
- Handles missing data
- Fixes date formats

✅ Part 2: Data Analysis (30 points)
- Merges customer, order, and product data
- Calculates monthly revenue
- Finds top customers
- Analyzes by category and region

✅ Part 3: Full Stack Dashboard (40 points)
- REST API with 5 endpoints
- Interactive React dashboard
- Charts and sortable tables
- Works on mobile too!

✅ Bonus Features (+10 points)
- Unit tests with pytest
- Docker support
- Enhanced error handling

## Troubleshooting

**Backend won't start?**
- Make sure you ran `python clean_data.py` first
- Check if port 8000 is free

**Frontend shows errors?**
- Make sure backend is running
- Try `npm install` again in the frontend folder

**No data showing?**
- Run `python clean_data.py` then `python analyze.py`
- Check the `data/processed/` folder has CSV files

## Testing

Run the tests:
```bash
pip install pytest
pytest tests/ -v
```

## Notes

- All data is sample/generated data
- The dashboard updates automatically when you change data
- Code follows Python PEP 8 style guidelines
- Responsive design works on phones and tablets

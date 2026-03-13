# Quick Start Guide

Get the dashboard running in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- Node.js 16+ and npm installed
- Terminal/Command Prompt

## Step-by-Step Instructions

### 1. Install Python Dependencies (30 seconds)

```bash
pip install pandas numpy fastapi uvicorn
```

### 2. Process the Data (10 seconds)

```bash
python clean_data.py
python analyze.py
```

You should see output confirming data was cleaned and analyzed.

### 3. Start the Backend (5 seconds)

Open a new terminal window:

```bash
cd backend
uvicorn main:app --reload
```

Keep this terminal open. You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 4. Install Frontend Dependencies (2 minutes)

Open another new terminal window:

```bash
cd frontend
npm install
```

### 5. Start the Dashboard (10 seconds)

In the same terminal:

```bash
npm start
```

Your browser should automatically open to http://localhost:3000

## Verify It Works

You should see:
- 📈 Monthly Revenue Trend chart
- 👥 Top 10 Customers table (sortable)
- 📦 Category Performance charts
- 🌍 Regional Analysis cards

## Troubleshooting

### Backend won't start
- Make sure you ran `python clean_data.py` and `python analyze.py` first
- Check that port 8000 is not in use

### Frontend shows error
- Make sure backend is running on port 8000
- Check browser console for specific errors
- Try refreshing the page

### Data not showing
- Verify files exist in `data/processed/` folder
- Check backend terminal for error messages
- Visit http://localhost:8000/docs to test API directly

## What's Next?

- Read `README.md` for detailed documentation
- Check `IMPLEMENTATION_NOTES.md` for technical details
- Run tests: `pytest tests/ -v`
- Try Docker: `docker-compose up --build`

## Need Help?

Common issues:

**"Module not found" error**
```bash
pip install -r backend/requirements.txt
```

**"Port already in use"**
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

**Frontend won't compile**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Success Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Dashboard loads without errors
- [ ] Charts display data
- [ ] Table is sortable
- [ ] No console errors

If all checked, you're good to go! 🎉

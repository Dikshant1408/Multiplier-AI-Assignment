# Student Guide - Full Stack Assignment

## What I Built

A complete data analysis system that:
1. Takes messy sales data
2. Cleans it up
3. Analyzes it
4. Shows it in a nice dashboard

Think of it like: **Raw Data → Clean Data → Insights → Pretty Charts**

---

## The Three Main Parts

### 🧹 Part 1: Data Cleaning (`clean_data.py`)

**What it does:**
- Removes duplicate customers
- Fixes email addresses
- Handles different date formats
- Fills in missing information

**How to run:**
```bash
python clean_data.py
```

**What you'll see:**
```
CLEANING CUSTOMERS DATA
Rows before: 11
Rows after: 10
Duplicates removed: 1
✓ Cleaned!
```

---

### 📊 Part 2: Data Analysis (`analyze.py`)

**What it does:**
- Combines customer, order, and product data
- Calculates monthly sales
- Finds best customers
- Groups by category and region

**How to run:**
```bash
python analyze.py
```

**What you'll see:**
```
MERGING DATASETS
Loaded 10 customers
Loaded 15 orders
✓ Analysis complete!
```

---

### 🌐 Part 3: Web Dashboard

**Two pieces:**

#### Backend (`backend/main.py`)
- Python API that serves data
- Like a waiter bringing food to your table

**How to run:**
```bash
cd backend
uvicorn main:app --reload
```

#### Frontend (`frontend/src/App.js`)
- React website that shows the data
- Like the menu and plates at a restaurant

**How to run:**
```bash
cd frontend
npm start
```

---

## Understanding the Code

### Data Cleaning Example

```python
# Before cleaning:
customer_id  name         email
1           John Doe     JOHN@EMAIL.COM
1           John Doe     john@email.com  # Duplicate!
2           Jane Smith   jane.smith      # Missing @

# After cleaning:
customer_id  name         email              is_valid_email
1           John Doe     john@email.com     True
2           Jane Smith   jane.smith         False
```

### API Example

```python
@app.get("/api/revenue")
def get_revenue():
    # Read the CSV file
    df = pd.read_csv('monthly_revenue.csv')
    # Convert to JSON
    return df.to_dict(orient='records')
```

When you visit `http://localhost:8000/api/revenue`, you get:
```json
[
  {"month": "2023-01", "total_revenue": 1500.00},
  {"month": "2023-02", "total_revenue": 2300.00}
]
```

### React Component Example

```javascript
// Fetch data from API
useEffect(() => {
  axios.get('http://localhost:8000/api/revenue')
    .then(response => setRevenueData(response.data))
}, []);

// Show it in a chart
<LineChart data={revenueData}>
  <Line dataKey="total_revenue" />
</LineChart>
```

---

## Common Questions

**Q: Why do I need both backend and frontend?**
A: Backend handles data (Python is good at this). Frontend shows it nicely (React is good at this).

**Q: What's an API?**
A: It's like a menu at a restaurant. Frontend asks "Can I have the revenue data?" and backend says "Here you go!"

**Q: Why use pandas?**
A: Pandas makes working with data super easy. Instead of loops, you can do things like `df.groupby('region').sum()`.

**Q: What's CORS?**
A: It's a security thing. We enable it so frontend (port 3000) can talk to backend (port 8000).

---

## Technologies Explained Simply

| Technology | What It Does | Why We Use It |
|------------|--------------|---------------|
| **Python** | Programming language | Good for data processing |
| **Pandas** | Data library | Makes data cleaning easy |
| **FastAPI** | Web framework | Creates the API quickly |
| **React** | UI library | Makes interactive websites |
| **Recharts** | Chart library | Creates pretty graphs |
| **Uvicorn** | Server | Runs the Python API |
| **npm** | Package manager | Installs JavaScript libraries |

---

## File Structure Explained

```
project/
│
├── data/
│   ├── raw/              ← Original messy data
│   └── processed/        ← Cleaned data
│
├── backend/
│   ├── main.py          ← API code
│   └── requirements.txt  ← Python packages needed
│
├── frontend/
│   ├── src/
│   │   ├── App.js       ← Main React component
│   │   └── App.css      ← Styling
│   └── package.json     ← JavaScript packages needed
│
├── clean_data.py        ← Step 1: Clean data
├── analyze.py           ← Step 2: Analyze data
└── README.md            ← Instructions
```

---

## What I Learned

1. **Data Cleaning**: Real data is messy! Need to handle duplicates, missing values, different formats.

2. **APIs**: Backend and frontend communicate through HTTP requests.

3. **React**: Components, state, and effects make interactive UIs.

4. **Full Stack**: Understanding both backend (data) and frontend (display) is powerful.

5. **Error Handling**: Always expect things to go wrong and handle it gracefully.

---

## Tips for Presenting

1. **Start with the problem**: "Sales data was messy and hard to understand"

2. **Show the solution**: "I built a system that cleans, analyzes, and visualizes it"

3. **Demo the dashboard**: Open http://localhost:3000 and show:
   - Click table headers to sort
   - Point out the different charts
   - Mention it works on mobile

4. **Explain the tech**: "Used Python for data processing, FastAPI for the API, and React for the UI"

5. **Mention extras**: "Also added tests and Docker support"

---

## If Something Breaks

**Backend error?**
- Check if data files exist in `data/processed/`
- Make sure you ran `clean_data.py` and `analyze.py`

**Frontend error?**
- Check if backend is running (http://localhost:8000/health)
- Look at browser console (F12) for errors

**Import error?**
- Run `pip install -r backend/requirements.txt`
- Or `npm install` in frontend folder

---

## Next Steps to Improve

1. Add user authentication
2. Store data in a real database (PostgreSQL)
3. Add more charts and filters
4. Deploy to the cloud (Heroku, AWS)
5. Add real-time updates with WebSockets

---

## Resources Used

- Pandas documentation: https://pandas.pydata.org/docs/
- FastAPI tutorial: https://fastapi.tiangolo.com/
- React docs: https://react.dev/
- Recharts examples: https://recharts.org/

---

**Remember**: This is a learning project. It's okay if it's not perfect. The important thing is understanding how all the pieces work together!

Good luck with your presentation! 🚀

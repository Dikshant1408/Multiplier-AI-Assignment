import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

function App() {
  const [revenueData, setRevenueData] = useState([]);
  const [customersData, setCustomersData] = useState([]);
  const [categoriesData, setCategoriesData] = useState([]);
  const [regionsData, setRegionsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortConfig, setSortConfig] = useState({ key: 'total_spend', direction: 'desc' });

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [revenue, customers, categories, regions] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/revenue`),
        axios.get(`${API_BASE_URL}/api/top-customers`),
        axios.get(`${API_BASE_URL}/api/categories`),
        axios.get(`${API_BASE_URL}/api/regions`)
      ]);

      setRevenueData(revenue.data);
      setCustomersData(customers.data);
      setCategoriesData(categories.data);
      setRegionsData(regions.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch data. Make sure the backend is running and data is processed.');
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedCustomers = [...customersData].sort((a, b) => {
    if (a[sortConfig.key] < b[sortConfig.key]) {
      return sortConfig.direction === 'asc' ? -1 : 1;
    }
    if (a[sortConfig.key] > b[sortConfig.key]) {
      return sortConfig.direction === 'asc' ? 1 : -1;
    }
    return 0;
  });

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading dashboard data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-box">
          <h2>⚠️ Error Loading Data</h2>
          <p>{error}</p>
          <button onClick={fetchAllData} className="retry-button">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>📊 Sales Data Dashboard</h1>
        <p>Full Stack Internship Assignment - Data Analysis & Visualization</p>
      </header>

      <main className="dashboard-container">
        {/* Revenue Trend Section */}
        <section className="dashboard-section">
          <h2>📈 Monthly Revenue Trend</h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="total_revenue" 
                  stroke="#0088FE" 
                  strokeWidth={2}
                  name="Revenue"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* Top Customers Section */}
        <section className="dashboard-section">
          <h2>👥 Top 10 Customers</h2>
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th onClick={() => handleSort('name')} className="sortable">
                    Name {sortConfig.key === 'name' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('region')} className="sortable">
                    Region {sortConfig.key === 'region' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('total_spend')} className="sortable">
                    Total Spend {sortConfig.key === 'total_spend' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('churned')} className="sortable">
                    Status {sortConfig.key === 'churned' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                  </th>
                </tr>
              </thead>
              <tbody>
                {sortedCustomers.map((customer, index) => (
                  <tr key={index}>
                    <td>{customer.name}</td>
                    <td>{customer.region}</td>
                    <td>${customer.total_spend.toFixed(2)}</td>
                    <td>
                      <span className={`status-badge ${customer.churned ? 'churned' : 'active'}`}>
                        {customer.churned ? '⚠️ Churned' : '✓ Active'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Category Performance Section */}
        <section className="dashboard-section">
          <h2>📦 Category Performance</h2>
          <div className="charts-row">
            <div className="chart-half">
              <h3>Revenue by Category</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={categoriesData}
                    dataKey="total_revenue"
                    nameKey="category"
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    label={(entry) => entry.category}
                  >
                    {categoriesData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="chart-half">
              <h3>Orders by Category</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={categoriesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="category" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="num_orders" fill="#00C49F" name="Number of Orders" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </section>

        {/* Regional Analysis Section */}
        <section className="dashboard-section">
          <h2>🌍 Regional Analysis</h2>
          <div className="cards-container">
            {regionsData.map((region, index) => (
              <div key={index} className="region-card">
                <h3>{region.region}</h3>
                <div className="metric">
                  <span className="metric-label">Customers</span>
                  <span className="metric-value">{region.num_customers}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Orders</span>
                  <span className="metric-value">{region.num_orders}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Total Revenue</span>
                  <span className="metric-value">${region.total_revenue.toFixed(2)}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Avg per Customer</span>
                  <span className="metric-value">${region.avg_revenue_per_customer.toFixed(2)}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <p>Created for Full Stack Internship Assignment © 2024</p>
      </footer>
    </div>
  );
}

export default App;

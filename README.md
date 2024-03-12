

# Streamlit Sales Dashboard

This project provides a dynamic sales dashboard built with the Streamlit framework. It allows users to upload an Excel file containing sales data and visualizes key metrics, sales performance, and budget analysis.

**Features**

* Interactive KPIs and gauges for key financial metrics
* Monthly sales comparisons across business units and scenarios
* Budget vs. forecast analysis
* In-memory SQL queries using DuckDB for efficient data manipulation
* Visualizations powered by Plotly

**Setup**

1. **Clone this repository:**
   ```bash
   git clone https://github.com/gholakioko/streamlit-sales-dashboard.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   (Ensure you have a file named `requirements.txt` listing the following: `streamlit`, `pandas`, `duckdb`, `plotly`)

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py 
   ```
   (Replace `app.py` with the name of your main Python script)

**Usage**

1. Use the sidebar to upload an Excel file containing sales data.
2. The dashboard will automatically populate with charts and metrics.

**Data Format**

The dashboard expects an Excel file with columns similar to the following:

* Year
* Month
* Scenario (e.g., 'Actuals', 'Budget', 'Forecast')
* Business Unit
* Account
* Sales

**Credits**

* Streamlit: [https://streamlit.io/](https://streamlit.io/)
* Pandas: [https://pandas.pydata.org/](https://pandas.pydata.org/)
* DuckDB: [https://duckdb.org/](https://duckdb.org/)
* Plotly: [https://plotly.com/python/](https://plotly.com/python/)

Portions of this project may have been inspired by or adapted from the work of [https://github.com/andfanilo](https://github.com/andfanilo).



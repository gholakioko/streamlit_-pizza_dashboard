# Import necessary libraries
import streamlit as st
import pandas as pd
import duckdb as duck 
import random
import plotly.express as px
import plotly.graph_objects as go

# Configure Streamlit page settings
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# Title of the Streamlit dashboard
st.title("Sales Streamlit Dashboard")

# Sidebar configuration for file upload
with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Choose a file")

# If no file is uploaded, display info message and stop the script
if uploaded_file is None:
    st.info("Upload a file through config", icon="ℹ️")
    st.stop()

# Data loading function with caching
@st.cache_data
def load_data(path: str):
    df = pd.read_excel(path)
    return df

# Load data from the uploaded file
df = load_data(uploaded_file)

# List of all months for later use
all_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Expander to preview loaded data
with st.expander("Data Preview"):
    st.dataframe(
        df,
        column_config={"Year": st.column_config.NumberColumn(format="%d")},
    )

# Function to plot a metric with optional graph
def plot_metric(
    label, value, prefix="", suffix="", show_graph=False, color_graph=""
):
    fig = go.Figure()
    
    fig.add_trace(
        go.Indicator(
            value=value,
            number={"prefix": prefix, "suffix": suffix, "font.size": 28},
            gauge={"axis": {"visible": False}},
            title={"text": label, "font": {"size": 24}},
        )
    )
    
    if show_graph:
        fig.add_trace(
            go.Scatter(
               y=random.sample(range(0, 101), 30),
               hoverinfo="skip",
               fill="tozeroy",
               fillcolor=color_graph,
               line={"color": color_graph},
            )
        )
        
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        height=100,
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Function to plot a gauge chart
def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
) -> None:
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={"suffix": indicator_suffix, "font.size": 26},
            gauge={"axis": {"range": [0, max_bound], "tickwidth": 1},
                   "bar": {"color": indicator_color}},
            title={"text": indicator_title, "font": {"size": 28}},
        )
    )
    
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Function to plot the top-right plot of the dashboard
def plot_top_right():
    sales_data = duck.sql(
        f"""
        # SQL Query to extract monthly sales for each business unit and scenario
        WITH sales_data AS (
            UNPIVOT(
                SELECT
                    Scenario,
                    business_unit,
                    {','.join(all_months)}
                    FROM df
                    WHERE Year='2023'
                    AND Account = 'Sales'                    
                )
            ON {','.join(all_months)}
            INTO 
                NAME month
                VALUE sales
        ),
        aggregated_sales AS (
            SELECT
                Scenario,
                business_unit,
                SUM(sales) AS sales
                FROM sales_data
                GROUP BY business_unit, Scenario
        )
        SELECT * FROM aggregated_sales
        """
    ).df()
    
    # Plotting the bar chart
    fig = px.bar(
        sales_data,
        x="business_unit",
        y="sales",
        color="Scenario",
        barmode="group",
        text_auto=".2s",
        title="Sales for Year 2023",
        height=400,
    )
    
    # Customize chart layout
    fig.update_traces(
        textfont_size=12,
        textangle=0,
        textposition="outside",
        cliponaxis=False,
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

# Function to plot the bottom-left plot of the dashboard
def plot_bottom_left():
    sales_data = duck.sql(
        f"""
        # SQL Query to extract monthly budget vs forecast for the software business unit
        WITH sales_data as (
            SELECT 
            Scenario,
            {','.join(all_months)}
            FROM df
            WHERE Year = '2023' 
            AND Account = 'Sales'
            AND business_unit = 'Software'
        )
        UNPIVOT sales_data 
        ON {','.join(all_months)}
        INTO
            NAME month
            VALUE sales
        """
    ).df()
    
    # Plotting the line chart
    fig = px.line(
        sales_data, 
        x="month", 
        y="sales",
        color="Scenario",
        markers=True,
        text="sales",
        title="Monthly Budget vs Forecast 2023",
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

# Function to plot the bottom-right plot of the dashboard
def plot_bottom_right():
    sales_data = duck.sql(
        f"""
        # SQL Query to extract actual yearly sales per account
        WITH sales_data AS (
            UNPIVOT ( 
                SELECT 
                    Account,Year,{','.join([f'ABS({month}) AS {month}' for month in all_months])}
                    FROM df 
                    WHERE Scenario='Actuals'
                    AND Account!='Sales'
                ) 
            ON {','.join(all_months)}
            INTO
                NAME year
                VALUE sales
        ),
        aggregated_sales AS (
            SELECT
                Account,
                Year,
                SUM(sales) AS sales
            FROM sales_data
            GROUP BY Account, Year
        )
        SELECT * FROM aggregated_sales
        """
    ).df()
    
    # Plotting the bar chart
    fig = px.bar(
        sales_data,
        x="Year",
        y="sales",
        color="Account",
        title="Actual Yearly Sales Per Account",
    )
    st.plotly_chart(fig, use_container_width=True)

# Streamlit layout configuration
top_left_column, top_right_column = st.columns((2, 1))
bottom_left_column, bottom_right_column = st.columns(2)

# Top left column layout
with top_left_column:
    column_1, column_2, column_3, column_4 = st.columns(4)
    
    with column_1:

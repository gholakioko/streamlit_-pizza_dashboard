import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon = ":bar_chart:",
    layout="wide"
) # set the page layout to be wide
st.title("Sales Streamlit Dashboard")
st.markdown("_Prototype v0.4.1_")

@st.cache_data 
def load_data(file):
    data = pd.read_excel(file)
    # do a light cleaning here
    return data


# set up a sidebar to upload the file
with  st.sidebar:
    st.header("configuration")
    #let the user upload the file
    uploaded_file = st.file_uploader("Choose a file to upload")
    
if uploaded_file is None:
    st.info("Please select a file to upload", icon="ℹ️")
    st.stop()

df = load_data(uploaded_file)
# display the data
with st.expander("Data Preview"):
    st.dataframe(df, 
                 column_config={
                     "Year":st.column_config.NumberColumn(format="%d") # format the year column so it doesn't have comma
                 },
    )
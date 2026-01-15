import streamlit as st
import pandas as pd
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Data Cleaning",page_icon="🔎",layout='centered')
st.title("📊🔎 DATA CLEANING APPLICATION")
st.write("Upload a **CSV** or an **EXCEL** File Containing Raw Data To Get A Cleaned Data")

# File uploader for CSV or Excel
uploaded = st.file_uploader("Upload CSV or Excel File", type=['csv', 'xlsx', 'xls'])


if uploaded is not None:
    try:
        # Read file into dataframe
        if uploaded.name.endswith('.csv'):
            df = pd.read_csv(uploaded)
            # converting bool columns as str
            bool_cols = df.select_dtypes(include=['bool']).columns
            df[bool_cols] =  df[bool_cols].astype('str')
        elif uploaded.name.endswith('xlsx', 'xls'):
            df = pd.read_excel(uploaded)
            # converting bool columns as str
            bool_cols = df.select_dtypes(include=['bool']).columns
            df[bool_cols] =  df[bool_cols].astype('str')
        else:
            st.error("Unsupported file format")
            df = None
    except Exception as e:
        st.error("Could Not Read Excel / CSV File. Please Check The File Format")
        st.exception(e)
        st.stop()

    st.success("Upload Successfull!")
    st.write("### Preview of data")
    st.dataframe(df.head())

    # Display missing values and duplicate info
    st.write("Missing values per column:")
    st.write(df.isnull().sum())
    st.write(f"Total duplicate rows: {df.duplicated().sum()}")

    # Button to remove missing values
    if st.button("Click Here To Remove Missing Values"):
        df_clean = df.dropna()
        st.write("### Data after removing missing values")
        st.write(df_clean)
    
    # Button to handle missing values (fill with mean for numeric)
    if st.button("Click Here To Handle Missing Values"):
        df_clean = df.fillna(df.mean(numeric_only=True))
        st.write("### Data after handling missing values (filled with mean)")
        st.write(df_clean)
        
    # Button to remove duplicate rows
    if st.button("Click Here To Remove Duplicate Values"):
        df_clean = df.drop_duplicates()
        st.write("### Data after removing duplicates")
        st.write(df_clean)
    
    # Provide option to download cleaned data
    if 'df_clean' in locals():
        to_download = df_clean
    else:
        to_download = df

    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
        processed_data = output.getvalue()
        return processed_data
    
    st.download_button(label="Download Your Cleaned CSV / Excel File",
                       data=to_excel(to_download),
                       file_name='cleaned_data.xlsx',
                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
else:
  st.info("Please Upload A CSV Or An Excel FIle To Get Started")
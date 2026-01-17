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
        elif uploaded.name.endswith(('.xlsx', '.xls')):
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

    st.write("### Data Overview")
    st.write("Number of Rows : ",df.shape[0])
    st.write("Number of Columns : ", df.shape[1])
    st.write("Number of Missing Values : ",df.isnull().sum().sum())
    st.write("Total Duplicate Rows : ",df.duplicated().sum())

    # Display missing values and duplicate info
    st.write("Missing values per column:")
    st.write(df.isnull().sum())

    total_missing = df.isnull().sum().sum()
    total_duplicates = df.duplicated().sum()
    
    st.divider()

    if total_missing == 0 and total_duplicates == 0:
        st.success("🎉 Data is clean! No missing or duplicate values found.")
    else:
        st.subheader("⚙️ Cleaning Options")

        col1, col2 = st.columns(2)

        # Missing values handling
        with col1:
            handle_missing = st.checkbox("Handle Missing Values")

            if handle_missing:
                missing_option = st.selectbox(
                    "Choose missing value handling method",
                    [
                        "Drop rows with missing values",
                        "Fill with mean (numeric)",
                        "Fill with median (numeric)",
                        "Fill with mode",
                        "Fill with custom value"
                    ]
                )

                if missing_option == "Fill with custom value":
                    custom_value = st.text_input("Enter custom value")

        # Duplicate handling
        with col2:
            remove_duplicates = st.checkbox("Remove Duplicate Rows")

        # 3. Apply cleaning
        cleaned_df = df.copy()

        if handle_missing:
            if missing_option == "Drop rows with missing values":
                cleaned_df = cleaned_df.dropna()

            elif missing_option == "Fill with mean (numeric)":
                cleaned_df = cleaned_df.fillna(cleaned_df.mean(numeric_only=True))

            elif missing_option == "Fill with median (numeric)":
                cleaned_df = cleaned_df.fillna(cleaned_df.median(numeric_only=True))

            elif missing_option == "Fill with mode":
                cleaned_df = cleaned_df.fillna(cleaned_df.mode().iloc[0])

            elif missing_option == "Fill with custom value":
                cleaned_df = cleaned_df.fillna(custom_value)

        if remove_duplicates:
            cleaned_df = cleaned_df.drop_duplicates()

        st.write("### ✅ Cleaned Data Preview")
        st.dataframe(cleaned_df)

        st.write("### Cleaned Data Summary")
        st.write("Number of Rows : ",cleaned_df.shape[0])
        st.write("Number of Columns : ",cleaned_df.shape[1])
        st.write("Number of Missing Values : ",cleaned_df.isnull().sum().sum())
        st.write("Total Duplicate Rows : ",cleaned_df.duplicated().sum())
        st.write("Missing values per column:")
        st.write(cleaned_df.isnull().sum())

        # 4. Download cleaned data
        def download_file(df, uploaded):
            buffer = BytesIO()

            if uploaded.name.endswith('.csv'):
                df.to_csv(buffer, index=False)
                mime = "text/csv"
                file_name = "cleaned_data.csv"
            else:
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                file_name = "cleaned_data.xlsx"

            buffer.seek(0)
            return buffer, file_name, mime

        buffer, file_name, mime = download_file(cleaned_df, uploaded)
        
        st.download_button(
            label="⬇️ Download Cleaned Data",
            data=buffer,
            file_name=file_name,
            mime=mime
        )
    
else:
  st.info("Please Upload A CSV Or An Excel FIle To Get Started")

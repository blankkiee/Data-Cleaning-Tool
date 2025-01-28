import streamlit as st
import pandas as pd

# Title
st.title("Data Cleaning Tool")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.dataframe(df)

    # Cleaning Options
    st.sidebar.header("Cleaning Options")
    
    # Remove Duplicates
    remove_duplicates = st.sidebar.checkbox("Remove Duplicates")
    
    # Handle Missing Values
    st.sidebar.subheader("Handle Missing Values")
    missing_option = st.sidebar.radio(
        "Choose how to handle missing values:",
        ("None", "Drop Rows", "Fill with Mean", "Fill with Median", "Fill with Specific Value")
    )
    specific_value = None
    if missing_option == "Fill with Specific Value":
        specific_value = st.sidebar.text_input("Enter the value to fill missing cells:")
    
    # Drop Columns
    st.sidebar.subheader("Drop Columns")
    drop_columns = st.sidebar.multiselect("Select columns to drop:", df.columns)
    
    # Apply Cleaning
    if st.button("Clean Data"):
        # Remove duplicates
        if remove_duplicates:
            df = df.drop_duplicates()

        # Handle missing values
        if missing_option == "Drop Rows":
            df = df.dropna()
        elif missing_option == "Fill with Mean":
            df = df.fillna(df.mean())
        elif missing_option == "Fill with Median":
            df = df.fillna(df.median())
        elif missing_option == "Fill with Specific Value" and specific_value is not None:
            df = df.fillna(specific_value)
        
        # Drop columns
        if drop_columns:
            df = df.drop(columns=drop_columns)

        st.subheader("Cleaned Data")
        st.dataframe(df)

        # Download cleaned data
        cleaned_csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cleaned Data as CSV",
            data=cleaned_csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

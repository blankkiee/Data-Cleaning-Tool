import streamlit as st
import pandas as pd
import design  # Import the design module

# Title
design.render_title()

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file)
    design.render_raw_data_section(df)

    # Sidebar Cleaning Options (Not fully functional yet)
    remove_duplicates, missing_option, specific_value, drop_columns = design.render_sidebar(df.columns)
    
    # Apply Cleaning
    if st.button("Clean Data"):
        # Remove duplicates
        if remove_duplicates:
            df = df.drop_duplicates()

        # Handle missing values (options needs improvements)
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

        # Display Cleaned Data
        design.render_cleaned_data_section(df)

        # Download Cleaned Data
        design.render_download_button(df)

    # Visualization Section
    design.render_visualization_section(df)

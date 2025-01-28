import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO  # For downloading chart as an image (can use different package)

def render_title():
    """Render the app title."""
    st.title("Data Cleaning and Visualization Tool")

def render_sidebar(df_columns):
    """Render sidebar components for data cleaning and visualization options."""
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
    drop_columns = st.sidebar.multiselect("Select columns to drop:", list(df_columns) if not df_columns.empty else [])
    
    return remove_duplicates, missing_option, specific_value, drop_columns

def render_raw_data_section(df):
    """Render the raw data section."""
    st.subheader("Raw Data")
    st.dataframe(df)

def render_cleaned_data_section(df):
    """Render the cleaned data section."""
    st.subheader("Cleaned Data")
    st.dataframe(df)

def render_visualization_section(df):
    """Render the data visualization section."""
    st.subheader("Data Visualization")

    # Visualization type selection
    visualization_type = st.selectbox("Select a Visualization Type", 
                                       ["None", "Bar Chart", "Line Chart", "Scatter Plot", "Histogram"])
    
    if visualization_type != "None":
        # Select columns for x and y axes
        x_col = st.selectbox("Select X-Axis", options=df.columns)
        y_col = st.selectbox("Select Y-Axis", options=df.columns)

        if st.button("Generate Visualization"):
            st.write(f"### {visualization_type}")
            plt.figure(figsize=(10, 5))

            if visualization_type == "Bar Chart":
                sns.barplot(x=df[x_col], y=df[y_col])
            elif visualization_type == "Line Chart":
                plt.plot(df[x_col], df[y_col], marker='o')
                plt.xlabel(x_col)
                plt.ylabel(y_col)
            elif visualization_type == "Scatter Plot":
                sns.scatterplot(x=df[x_col], y=df[y_col])
            elif visualization_type == "Histogram":
                sns.histplot(data=df, x=x_col, kde=True)

            # Display the plot
            st.pyplot(plt)

            # Download Chart Button
            chart_buffer = BytesIO()
            plt.savefig(chart_buffer, format="png")  # Save the plot to a BytesIO buffer
            chart_buffer.seek(0)  # Rewind to the beginning of the buffer

            st.download_button(
                label="Download Chart as PNG",
                data=chart_buffer,
                file_name=f"{visualization_type.replace(' ', '_').lower()}_chart.png",
                mime="image/png"
            )

            # Close the plot for overlap prevention
            plt.close()

def render_download_button(df):
    """Render the download button for cleaned data."""
    cleaned_csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Cleaned Data as CSV",
        data=cleaned_csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

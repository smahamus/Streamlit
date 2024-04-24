import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    data = pd.read_csv('museums.csv', low_memory=False)
    data['Zip Code (Administrative Location)'] = data['Zip Code (Administrative Location)'].astype(str)
    columns_to_remove = ['Museum ID', 'Legal Name', 'Employer ID Number', 'Tax Period', 'Zip Code (Physical Location)', 'Locale Code (NCES)', 'County Code (FIPS)', 'State Code (FIPS)', 'Region Code (AAM)', 'Institution Name', 'Street Address (Physical Location)', 'City (Physical Location)', 'State (Physical Location)', 'Alternate Name']
    clean_data = data.drop(columns=columns_to_remove, errors='ignore')
    # Rename latitude and longitude for compatibility with st.map()
    clean_data.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace=True)
    return clean_data

def main():
    st.title('Museum Information in the USA')

    # Load and clean data
    museum_data = load_data()

    # Display the data as a table
    st.write(museum_data)

    # Data Summarization and Statistics
    st.header("Data Summarization and Statistics")
    total_museums = len(museum_data)
    st.subheader(f"Total Number of Museums: {total_museums}")
    average_income = museum_data.groupby('Museum Type')['Income'].mean().round(2)
    st.subheader("Average Income Per Museum Type")
    st.write(average_income)

    # Data Visualization
    st.header("Data Visualization")
    museum_types = museum_data['Museum Type'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(museum_types, labels=museum_types.index, autopct='%1.1f%%')
    plt.title('Distribution of Museums by Type')
    st.pyplot(plt)

    st.subheader("Relationship Between Income and Revenue")
    fig, ax = plt.subplots()
    museum_data.plot(kind='scatter', x='Income', y='Revenue', ax=ax)
    st.pyplot(fig)

    st.subheader("Museums on the Map")
    if 'latitude' in museum_data.columns and 'longitude' in museum_data.columns:
        museum_data = museum_data.dropna(subset=['latitude', 'longitude'])
        st.map(museum_data)

if __name__ == "__main__":
    main()

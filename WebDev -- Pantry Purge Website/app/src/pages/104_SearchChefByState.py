import streamlit as st
import requests
import pandas as pd
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Add sidebar links
SideBarLinks()
st.title("Search For Fellow Chef")

st.write("Search For Chefs By Country")

# Input field for Country
country = st.text_input("Enter The Country Of Interest:")

# Fetch chefs based on Country
if country:
    url = f'http://api:4000/c/chefs/region/{country}'
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            chefs = response.json()

            # Check if there are chefs in the country
            if chefs:
                # Create a DataFrame to display the chefs as a table
                df = pd.DataFrame(chefs)

                # Display the table of chefs
                st.write("### Chefs Found in Country:", country)
                st.dataframe(df)  # Display chefs in a table

            else:
                st.warning(f"No chefs found in {country}. Please try a different country.")
        
        else:
            st.error(f"Failed to fetch chefs. Status code: {response.status_code}")
            st.write(f"API Error: {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the data: {str(e)}")


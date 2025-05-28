import streamlit as st
import requests
import pandas as pd
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Add sidebar links
SideBarLinks()

st.write("# Your Recipes")

# Input field for Chef ID
chef_id = st.number_input("Enter Chef ID", step=1)

# Fetch recipes based on Chef ID
if chef_id:
    url = f'http://api:4000/r/chefs/{int(chef_id)}/recipes'
    response = requests.get(url)
    

    try:
        # Check if the response is successful
        if response.status_code == 200:
            recipes = response.json()
            
            st.dataframe(recipes)
        else:
            st.write(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.write(f"Error occurred: {str(e)}")
else:
    st.write("Please enter a valid Chef ID.")


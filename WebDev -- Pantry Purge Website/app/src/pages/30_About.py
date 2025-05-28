import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    PantryPurge is a brand-new recipe database that allows users to search for recipes that fit their exact needs.  
    
    # Why we created this platform: 
    This app will allow users to save money by making best use of what they already have in their kitchen to prevent waste. 
    It will also take the hassle out of finding a recipe which you have all the ingredients for. Our search engine will be more open-ended than competitors, allowing novice cooks to work with 
    what they have and making cooking more accessible to even the most casual users.

    # How to use the platform: 
    Users can search by listing the ingredients they have in their pantry/fridge so they can be matched with recipes
    that best utilize those ingredients. They can also filter by other criteria such as prep time, cuisine, and dietary restrictions. 
    

    """
        )

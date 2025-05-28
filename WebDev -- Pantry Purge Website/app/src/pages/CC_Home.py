
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Casual Cook Home")
st.write("Welcome to the Casual Cook Home Page!")

st.header("Features")
if st.button("Search for Recipes"):
    st.switch_page("pages/search_recipes.py")
if st.button("View Featured Recipes"):
    st.switch_page("pages/featured_recipes.py")
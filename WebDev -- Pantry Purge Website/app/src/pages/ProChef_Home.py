import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Welcome Professional Chef, Anthony")
st.write("Welcome to the Professional Chef Home Page!")

if st.button("View Your Recipes"):
    st.switch_page("pages/100_ViewRecipes.py")

if st.button("Add A Recipe"):
    st.switch_page("pages/101_AddRecipe.py")

if st.button("Submit to Newsletter"):
    st.switch_page("pages/102_NewsletterSubmit.py")

if st.button("View Nearby Chefs"):
    st.switch_page("pages/104_SearchChefByState.py")

if st.button("Delete Recipe"):
    st.switch_page("pages/103_DeleteChefRecipe.py")




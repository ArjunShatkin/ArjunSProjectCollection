
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("Featured Recipes")

featured_url = "http://api:4000/cc/recipes/featured"
response = requests.get(featured_url)

if response.status_code == 200:
    recipes = response.json()
    if recipes:
        for recipe in recipes:
            st.write("\n\n")
            st.write(f" {recipe.get('RecipeName')}")
            st.write(recipe.get('Description'))
            if st.button("View Recipe", key=f"view_{recipe['RecipeID']}"):
                st.session_state["selected_id"] = recipe['RecipeID']
                st.switch_page("pages/recipe_profile.py")
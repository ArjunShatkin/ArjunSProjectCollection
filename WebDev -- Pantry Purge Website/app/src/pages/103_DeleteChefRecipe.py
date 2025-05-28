import streamlit as st
import requests
from datetime import datetime

st.title("Delete your Recipe")

with st.form("Delete Chef Recipe"):
  chef_id = st.text_input("Chef ID")
  recipe_id = st.text_input("Recipe ID")
  submission = st.form_submit_button("Delete Recipe")

if submission:
    data = {}
    data['RecipeID'] = recipe_id
    data['ChefID'] = chef_id

    st.write(data)
    endpoint = f"http://api:4000/r/recipes/{int(recipe_id)}/del"
    
                
    response = requests.delete(endpoint)

    if response.status_code == 200:
            st.success(f"Successfully deleted recipe with ID {recipe_id}.")
    else:
        st.error(f"Failed to delete recipe. Status code: {response.status_code}")
        st.json(response.json())
import streamlit as st
import requests
import pandas as pd
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.title("Submit to Newsletter")

with st.form("Newsletter"):
  chef_id = st.text_input("Chef ID")
  recipe_id = st.text_input("Recipe ID")
  sub_status = st.selectbox("Submission Status", ["Not Submitted", "Submitted"], index=0)
  submission = st.form_submit_button("Submit Recipe")

if submission:
    data = {}
    data['RecipeID'] = recipe_id
    data['ChefID'] = chef_id
    data ['SubStatus'] = sub_status

    st.write(data)

    response = requests.post(f'http://api:4000/r/recipes/{int(recipe_id)}/newsletter', json=data)
    
    if response.status_code == 200:
            st.success(f"Successfully submitted newsletter with for Recipe ID {recipe_id}.")
    else:
        st.error(f"Failed to submit newsletter. Status code: {response.status_code}")
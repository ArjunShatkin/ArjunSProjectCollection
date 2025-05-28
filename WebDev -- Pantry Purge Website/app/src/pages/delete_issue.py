import streamlit as st
import requests
from modules.nav import SideBarLinks


SideBarLinks()

with st.form("Delete Issue"):
  issueid = st.number_input("Issue ID")
  submission = st.form_submit_button("Delete Issue")

if submission:
    data = {}
    data['Issue'] = issueid
   

    st.write(data)
    endpoint = f"http://api:4000/i/issues/{int(issueid)}/del"
    
                
    response = requests.delete(endpoint)

    if response.status_code == 200:
            st.success(f"Successfully deleted recipe with ID {issueid}.")
    else:
        st.error(f"Failed to delete recipe. Status code: {response.status_code}")
        st.json(response.json())

import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import json

st.set_page_config(layout = 'wide')
# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Recipe analytics")
st.write('')
st.write('')

url = 'http://api:4000/a/recipes/analytics'

response = requests.get(url)
if response.status_code == 200:
    results = response.json()
    df = pd.DataFrame(results)
else:
    print(f"Error: {response.text}")

df
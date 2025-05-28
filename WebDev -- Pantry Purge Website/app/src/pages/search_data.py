import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import json
import matplotlib.pyplot as plt

st.set_page_config(layout = 'wide')
# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Search Data")
st.write('')
st.write('')
groupby = st.selectbox('Group by:', ['Ingredients', 'Dietary Preferences'])
days = st.number_input('Time interval (days):', min_value=1, value=180, max_value = 365)
bars = st.number_input('Number of bars:', min_value=3, value=8, max_value = 20)
if groupby == 'Ingredients':
    url = 'http://api:4000/a/search/ingredients'
else:
    url = 'http://api:4000/a/search/dietrestrict'

response = requests.get(f'{url}?days={days}')
if response.status_code == 200:
    results = response.json()
    df = pd.DataFrame(results)
else:
    print(f"Error: {response.text}")

fig, ax = plt.subplots()
if groupby == 'Ingredients':
    ax.bar(df['IngredientName'][:bars], df['PastWeekSearches'][:bars])
    ax.set_xticklabels(df['IngredientName'][:bars], rotation = 45, ha='right', fontsize=100/bars)
    ax.set_title(f'Top ingredients searched in the last {days} days')
else:
    ax.bar(df['RestName'][:bars], df['PastWeekSearches'][:bars])
    ax.set_xticklabels(df['RestName'][:bars], rotation = 45, ha='right', fontsize=100/bars)
    ax.set_title(f'Top dietary restrictions searched in the last {days} days')

st.pyplot(fig)
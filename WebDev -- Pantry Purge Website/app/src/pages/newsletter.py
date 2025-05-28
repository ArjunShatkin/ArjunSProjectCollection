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

st.title(f"Review Newsletter Submissions")
st.write('')
st.write('')

url = 'http://api:4000/a/newsletter'

response = requests.get(url)
if response.status_code == 200:
    results = response.json()
    df = pd.DataFrame(results)
else:
    print(f"Error: {response.text}")

for row in df.itertuples(index=True, name='Row'):
    if row.SubStatus == 'Pending':
        st.markdown(
            f"""
            <div style="background-color:#f9f9f9; padding:20px; border-radius:10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="color:#333;">{row.RecipeName}</h3>
                <p style="font-size:16px;"><strong>Cuisine: </strong>{row.Cuisine}</p>
                <p style="font-size:16px;">{row.Description}</p>
                <p style="font-size:18px;"><strong>Submitted: </strong>{row.SubDate}</p>
                <p style="font-size:16px;"><strong>Average Rating:</strong> {row.AvgRating} ⭐</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        sub_id = row.SubID

        with col1:
            if st.button(f"✅ Accept {row.RecipeName} to Newsletter", key=f"accept_{row.Index}"):
                response = requests.put('http://api:4000/a/newsletter', json={"SubStatus": "Accepted", "SubID": sub_id})
                if response.status_code == 200:
                    st.success(f"Accepted {row.RecipeName}!")

        with col2:
            if st.button(f"❌ Reject {row.RecipeName} from Newsletter", key=f"reject_{row.Index}"):
                response = requests.put('http://api:4000/a/newsletter', json={"SubStatus": "Rejected", "SubID": sub_id})
                if response.status_code == 200:
                    st.error(f"Rejected {row.RecipeName}!")

df
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.write("# All Users")


users = requests.get('http://api:4000/u/users').json()
try:
  st.dataframe(users)
except:
  st.write("could not connect to databade to get users!")


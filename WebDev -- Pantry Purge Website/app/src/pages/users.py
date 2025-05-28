import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.write("# All Users")

if st.button('View Users', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/all_users.py')


if st.button('User Analysis', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/user_analysis.py')

if st.button('Update User', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/update_user.py')


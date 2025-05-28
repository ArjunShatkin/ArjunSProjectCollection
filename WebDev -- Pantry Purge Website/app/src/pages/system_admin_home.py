import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('System Admin Home Page')

if st.button('Issues', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/systems_issues.py')

if st.button('Users', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/users.py')
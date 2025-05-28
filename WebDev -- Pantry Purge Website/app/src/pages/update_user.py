import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.write("# Change User Status")

with st.form("Edit Issue"):
  user_id = st.number_input("Input User ID:")
  name = st.text_input("Input Username:")
  Status = st.selectbox("Status of the User", ("active","Disabled"))

  submitted = st.form_submit_button("Submit Issue")

if submitted:
  data = {}
  data['UserId'] = user_id
  data ['Username'] = name
  data ['UserStatus'] = Status
  st.write(data)

  requests.put('http://api:4000/u/users', json = data)
  st.write("User has been update")


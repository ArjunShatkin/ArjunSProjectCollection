import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.write("# New Issue")


with st.form("Edit Issue"):
  issue_id = st.number_input("Input Issue ID:")
  user = st.number_input("Input User ID:")
  time = st.text_input("Enter the Time:")
  Priority = st.text_input("Priority of the  Issue:")
  Status = st.text_input("Status of the Issue:")
  Title = st.text_input("Title the issue:")
  Description = st.text_area("Summarize the Issue Occuring:")
  Resolved = st.text_input("Enter the Time when the Issue is resolved:")

  submitted = st.form_submit_button("Submit Issue")

  if submitted:
    data = {}
    data['IssueID'] = issue_id
    data['UserID'] = user
    data ['EnteredTime'] = time
    data ['Priority'] = Priority
    data ['Status'] = Status
    data ['Title'] = Title
    data ['Description'] = Description
    data ['ResolvedDate'] = Resolved
    st.write(data)


    requests.post('http://api:4000/i/issues',json = data)
    





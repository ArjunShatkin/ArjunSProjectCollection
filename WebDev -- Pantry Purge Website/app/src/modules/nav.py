# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


## ------------------------ Examples for Role of usaid_worker ------------------------
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction_Test.py", label="Regression Prediction", icon="🏦"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/system_admin_home.py", label="Admin Home", icon="🏦")
    st.sidebar.page_link("pages/users.py", label="Users", icon="👤")
    st.sidebar.page_link("pages/systems_issues.py", label="Issues", icon="🖥️")
    
    

#### ------------------------ Casual Cook Role ------------------------
def CCPageNav():
    st.sidebar.page_link("pages/CC_Home.py", label="Casual Cook Home", icon="🖥️")
    st.sidebar.page_link("pages/search_recipes.py", label="Search", icon="🍽️")
    st.sidebar.page_link("pages/featured_recipes.py", label="Featured Recipes", icon="⭐")

#### ------------------------ Data Analyst Role ------------------------
def analyst(): 
    st.sidebar.page_link("pages/search_data.py", label = "View Search Data", icon="📈")
    st.sidebar.page_link("pages/recipe_analytics.py", label = "View Recipe Analytics", icon="📊")
    st.sidebar.page_link("pages/newsletter.py", label = "View Newsletter Submissions", icon="📨")


#### ------------------------ Data Analyst Role ------------------------
def prochef(): 
    st.sidebar.page_link("pages/100_ViewRecipes.py", label = "View Your Recipes", icon="🧾")
    st.sidebar.page_link("pages/101_AddRecipe.py", label = "Add A Recipe", icon="📝")
    st.sidebar.page_link("pages/102_NewsletterSubmit.py", label = "Submit to Newsletter", icon="📰")
    st.sidebar.page_link("pages/104_SearchChefByState.py", label = "View Nearby Chefs", icon="🧑‍🍳")
    st.sidebar.page_link("pages/103_DeleteChefRecipe.py", label = "Delete Recipe", icon="❌")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "pol_strat_advisor":
            PolStratAdvHomeNav()
            WorldBankVizNav()
            MapDemoNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "usaid_worker":
            PredictionNav()
            ApiTestNav()
            ClassificationNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()
            

        if st.session_state["role"] == "casual_cook":
            CCPageNav()


    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")

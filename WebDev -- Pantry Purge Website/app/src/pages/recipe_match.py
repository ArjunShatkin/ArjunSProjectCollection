
import streamlit as st
import requests

st.title("Search for Recipes")
st.write("Enter the ingredients you have on hand (comma-separated):")
ingredients_input = st.text_input("Ingredients", "chicken, rice, broccoli")

if st.button("Search"):
    ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",")]
    url = "http://api:4000/casual_cooks/recipes/match"
    response = requests.post(url, json={"ingredients": ingredients})
    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            st.write("Matching Recipes:")
            for recipe in recipes:
                st.write(f"- {recipe['name']}")
                st.write(f"  Ingredients: {', '.join(recipe['ingredients'])}")
                st.write(f"  Instructions: {recipe['instructions']}")
        else:
            st.write("No matching recipes found.")
    else:
        st.write("Error fetching recipes. Please try again later.")
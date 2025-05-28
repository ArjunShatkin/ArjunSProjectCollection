
import streamlit as st
import requests
from modules.nav import SideBarLinks
import pandas as pd

SideBarLinks()

recipe_id = st.session_state["selected_id"]
profile_url = f"http://api:4000/cc/recipes/{recipe_id}/profile"
response = requests.get(profile_url)

if response.status_code == 200:
    data = response.json()

    st.title(data.get('RecipeName'))

    columns = st.columns(2)
    left_column = columns[0]
    right_column = columns[1]

    left_column.write(f"Difficulty: {data.get('Difficulty')}")
    left_column.write(f"Cuisine: {data.get('Cuisine')}")
    left_column.write(f"Servings: {data.get('Servings')}")
    left_column.write(f"Prep Time (mins): {data.get('PrepTimeMins')}")
    left_column.write(f"Cook Time (mins): {data.get('CookTimeMins')}")
    left_column.write(f"Average Rating: {data.get('AvgRating')}")

    right_column.write(f"Number of Views: {data.get('NumViews')}")
    right_column.write(f"Number of Shares: {data.get('NumShares')}")
    right_column.write(f"Featured: {'Yes' if data.get('Featured') else 'No'}")
    right_column.write(f"Published: {data.get('PublishDate')}")

    right_column.subheader("Caloric Breakdown")
    caloric_placeholders = right_column.empty()
    caloric_breakdown = data.get("Calories", [])
    if caloric_breakdown:
        calorie_data = []
        for row in caloric_breakdown:
            calorie_data.append({"Ingredient:": row.get("IngredientName"),
                                 "Cal/Unit:": row.get("CalPerUnit"),
                                 "Measure Unit:": row.get("MeasureUnit"),
                                 "Quantity:": row.get("Quantity"),
                                 "Total Ingredient Calories:": row.get("TotalIngredientCalories"),
                                 "Calories Per Serving:": row.get("CaloriesPerServing")})
        df = pd.DataFrame(calorie_data)
        caloric_placeholders.table(df)

    right_column.subheader("Adjust Servings")
    new_servings = right_column.number_input("Enter your choice of servings.", min_value=1, value=data.get("Servings", 1))

    if right_column.button("Adjust Servings"):
        adjust_url = f"http://api:4000/cc/recipes/{recipe_id}/adjust"
        adjusted_response = requests.get(adjust_url, params={"new_servings": new_servings})
        adjusted_data = adjusted_response.json()

        if adjusted_data:
            adjusted_calories = []
            for ingredient in adjusted_data:
                total_ingredient_calories = round(row.get("CalPerUnit") * ingredient.get("AdjustedQuantity"), 2)
                calories_per_serving = round(total_ingredient_calories / new_servings, 2)
                adjusted_calories.append({"Ingredient:": ingredient.get("IngredientName"),
                                          "Cal/Unit:": row.get("CalPerUnit"),
                                          "Measure Unit:": ingredient.get("MeasureUnit"),
                                          "Quantity:": ingredient.get("AdjustedQuantity"),
                                          "Total Ingredient Calories:": total_ingredient_calories,
                                          "Calories Per Serving:": calories_per_serving})
            df_adjusted = pd.DataFrame(adjusted_calories)
            caloric_placeholders.table(df_adjusted)

    left_column.subheader("Description")
    left_column.write(f"{data.get('Description')}")

    video_url = data.get("VideoUrl")
    if video_url:
        left_column.image(video_url, caption="Recipe Video")

    st.write("\n\n")
    st.write("-----------------------------------------------------")
    st.write("\n\n")

    st.subheader("Reviews")
    st.write("Number of Reviews:", data.get('NumReviews'))
    reviews = data.get("Reviews")
    if reviews:
        for review in reviews:
            st.write(f"- Published: {review.get('ReviewDate')}"
                     f"\n\n"
                     f"\tBy {review.get('CookName', 'Anonymous')}"
                     f"\n\n"
                     f"\t{review.get('ReviewText')}"
                     f"\n\n"
                     f"\t(Rating: {review.get('Rating')})")
            st.write("\n\n")
    else:
        st.write("No reviews posted.")


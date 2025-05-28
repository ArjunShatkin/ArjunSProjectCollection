from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
import json
import traceback
import datetime

recipes = Blueprint('recipes', __name__)
chefs = Blueprint('chefs', __name__)

# ------------------------------------------------------------
# POST /recipes - Create and publish a new recipe -- User Story 3.6
# ------------------------------------------------------------

@recipes.route('/recipes', methods=['POST'])
def create_recipe():
    current_app.logger.info('POST /recipes route')

    data = request.json

    recipe_name = data.get('RecipeName')
    chef_id = data.get('ChefID')
    servings = data.get('Servings', 4)
    difficulty = data.get('Difficulty', 'Medium')
    calories = data.get('Calories', 0)
    description = data.get('Description', '')
    cuisine = data.get('Cuisine', 'General')
    prep_time_mins = data.get('PrepTimeMins', 30)
    cook_time_mins = data.get('CookTimeMins', 45)
    publish_date = data.get('PublishDate', '2025-01-01')
    video_url = data.get('VideoUrl','')

    # Required field validation
    if not recipe_name:
        return jsonify({"error": "RecipeName is required."}), 400

    try:
        cursor = db.get_db().cursor()

        query = '''
            INSERT INTO Recipe (
                RecipeName, ChefID, Servings, Difficulty, Calories, 
                Description, Cuisine, PrepTimeMins, CookTimeMins, 
                PublishDate, VideoUrl
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        values = (
            recipe_name, chef_id, servings, difficulty, calories,
            description, cuisine, prep_time_mins, cook_time_mins, publish_date, video_url
        )

        cursor.execute(query, values)
        new_id = cursor.lastrowid

        db.get_db().commit()

        return jsonify({
            "message": "Recipe created successfully.",
            "recipe_id": new_id
        }), 200

    except Exception as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500



# ------------------------------------------------------------
# Post a recipe to be considered for the newsletter -- User Story 3.3
# ------------------------------------------------------------

@recipes.route('/recipes/<int:recipe_id>/newsletter', methods=['POST'])
def submit_recipe_for_newsletter(recipe_id):
    current_app.logger.info(f'POST /recipes/{recipe_id}/newsletter route')

    data = request.get_json()
    current_app.logger.debug(f"Received data: {data}")  # Log incoming data
    
    chef_id = data.get('ChefID')
    
    sub_status = data.get('SubStatus', 'Pending')
    sub_date = datetime.datetime.now()

    if not chef_id:
        return jsonify({"error": "ChefID is required."}), 400

    try:
        cursor = db.get_db().cursor()

        query = '''
            INSERT INTO Newsletter (ChefID, RecipeID, SubStatus, SubDate)
            VALUES (%s, %s, %s, %s);
        '''
        values = (chef_id, recipe_id, sub_status, sub_date)
        cursor.execute(query, values)
        
        sub_id = cursor.lastrowid

        db.get_db().commit()

        return jsonify({
            "message": "Recipe submission to newsletter successful.",
            "SubID": sub_id,
            "ChefID": chef_id,
            "RecipeID": recipe_id,
            "SubStatus": sub_status,
            "SubDate": sub_date.isoformat()
        }), 200

    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Exception: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
        # return jsonify({sub_id}), 500


# ------------------------------------------------------------
# Search for chef by country -- User Story 3.5
# ------------------------------------------------------------

@chefs.route('/chefs/region/<string:country_name>', methods=['GET'])
def get_chefs_in_given_country(country_name):
    current_app.logger.info(f'GET /chefs/region/{country_name} route')

    try:
        cursor = db.get_db().cursor()

        # Find chefs in the provided country
        query = """
            SELECT ChefID, FirstName, LastName, CuisineSpecialty, YearsExp, City, Country
            FROM Chef
            WHERE Country = %s;
        """
        cursor.execute(query, (country_name,))
        chefs = cursor.fetchall()
        
        #  Return the list of chefs in the given country
        return jsonify(chefs), 200

    except Exception as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------------
# View a list of recipes for a given chef -- User Story 3.1
# ------------------------------------------------------------

@recipes.route('/chefs/<int:chef_id>/recipes', methods=['GET'])
def get_chef_recipes(chef_id):
    try:
        # Connect and create a cursor
        conn = db.get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                RecipeID, RecipeName, NumShares, NumViews, NumReviews, 
                IsFeatured, PublishDate
            FROM Recipe
            WHERE ChefID = %s
        """, (chef_id,))

        # Fetch rows
        rows = cursor.fetchall()

        # Create proper JSON response
        response = make_response(jsonify(rows))
        response.mimetype = 'application/json'
        response.status_code = 200
        return response

    except Exception as e:
        # Fail safe
        print("Error:", str(e))
        return jsonify({"error": "Something went wrong."}), 500

# ------------------------------------------------------------
# Delete A Recipe
# ------------------------------------------------------------
@recipes.route('/recipes/<int:recipe_id>/del', methods=['DELETE'])
def delete_recipe(recipe_id):
    current_app.logger.info(f'DELETE /recipes/{recipe_id} route')

    try:
        conn = db.get_db()
        cursor = conn.cursor()

        # Then delete the recipe itself
        cursor.execute("DELETE FROM Recipe WHERE RecipeID = %s;", (recipe_id,))

        # First delete related entries in Newsletter
        cursor.execute("DELETE FROM Newsletter WHERE RecipeID = %s;", (recipe_id,))

        conn.commit()

        return jsonify({"message": f"Recipe with ID {recipe_id} successfully deleted."}), 200

    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Error deleting recipe: {e}")
        return jsonify({"error": str(e)}), 500



# ------------------------------------------------------------
# Add an Ingredient to A recipe -- Part 2 of User Story 3.6
# ------------------------------------------------------------

@recipes.route('/recipes/ingredient', methods=['POST'])
def add_ingredient():
    current_app.logger.info(f'POST /recipes/ingredient route')


    data = request.json

    recipe_id = data.get('RecipeID')
    ingredient_id = data.get('IngredientID')
    quantity = data.get('Quantity', 1.0)

    # Validate required fields
    if not recipe_id or not ingredient_id:
        return jsonify({"error": "RecipeID and IngredientID are required."}), 400

    try:
        cursor = db.get_db().cursor()

        # Insert into RecipeIngredient
        query = '''
            INSERT INTO RecipeIngredient (
                RecipeID, IngredientID, Quantity
            )
            VALUES (%s, %s, %s);
        '''
        values = (recipe_id, ingredient_id, quantity)

        cursor.execute(query, values)
        db.get_db().commit()

        return jsonify({
            "message": "Ingredient linked to recipe successfully.",
            "recipe_id": recipe_id,
            "ingredient_id": ingredient_id
        }), 200

    except Exception as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500
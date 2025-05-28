from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
users = Blueprint('users', __name__)
issues = Blueprint('issues', __name__)

# Get all the products from the database, package them up,
# and return them to the client
@users.route('/users', methods=['GET'])
def get_all_users():

    cursor = db.get_db().cursor()
    
    query = '''
        SELECT  userid, 
                username, 
                datecreated, 
                UserStatus  
        FROM User
    '''
    
    # Same process as above
    
    cursor.execute(query)
    theData = cursor.fetchall()

    
    response = make_response(theData)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response

@users.route('/users', methods=['PUT'])
def new_user():
    current_app.logger.info('PUT /users route')
    user_info = request.json
    user_id = user_info['UserId']
    user_name = user_info['Username']
    status = user_info['UserStatus']

    query = 'UPDATE users SET status = %s where id = %s'
    data = (user_name, status, user_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'new user added'


@users.route('/users/date', methods=['GET'])
def creation_date_count():

    cursor = db.get_db().cursor()
    
    query = '''
        Select month(datecreated) as month, Count(*) as number_of_users
        from User
        group by month(DateCreated)
    '''
    
    # Same process as above
    
    cursor.execute(query)
    theData = cursor.fetchall()

    
    response = make_response(theData)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response
    
@issues.route('/issues', methods=['GET'])
def get_all_issues():

    cursor = db.get_db().cursor()
    
    query = '''
        Select  IssueID, UserID, EnteredTime, Priority, Status, Title, Description, ResolvedDate
        From Issue
    '''
    
    # Same process as above
    
    cursor.execute(query)
    theData = cursor.fetchall()

    
    response = make_response(theData)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response

@issues.route('/issues/prior', methods=['GET'])
def prior_issues():

    cursor = db.get_db().cursor()
    
    query = '''
        Select  IssueID, UserID, EnteredTime, Priority, Status, Title, Description, ResolvedDate
        From Issue
        Where ResolvedDate IS NOT NULL
    '''
    
    # Same process as above
    
    cursor.execute(query)
    theData = cursor.fetchall()

    
    response = make_response(theData)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response

@issues.route('/issues', methods = ['POST'])
def add_new_issue():
    
    the_data = request.json 
    current_app.logger.info(the_data)

    issue_id = the_data['IssueID']
    user = the_data['UserID']
    time = the_data ['EnteredTime']
    Priority = the_data ['Priority']
    Status = the_data ['Status']
    Title = the_data ['Title']
    Description = the_data ['Description']
    Resolved = the_data ['ResolvedDate']

    query = f'''
        INSERT INTO Issue (IssueID, UserID, EnteredTime, Priority, Status, Title, Description, ResolvedDate)
        VALUES ('{issue_id}','{user}', '{time}', '{Priority}','{Status}', '{Title}', '{Description}','{Resolved}')
    '''
    # TODO: Make sure the version of the query above works properly
    # Constructing the query
    # query = 'insert into products (product_name, description, category, list_price) values ("'
    # query += name + '", "'
    # query += description + '", "'
    # query += category + '", '
    # query += str(price) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added issue")
    response.status_code = 200
    return response


@issues.route('/issues/<int:issueid>/del', methods=['DELETE'])
def delete_issue(issueid):
    current_app.logger.info(f'DELETE /issues/{issueid} route')

    try:
        conn = db.get_db()
        cursor = conn.cursor()

        # Then delete the recipe itself
        cursor.execute("DELETE FROM Issue WHERE IssueID = %s;", (issueid,))


        conn.commit()

        return jsonify({"message": f"Recipe with ID {issueid} successfully deleted."}), 200

    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Error deleting recipe: {e}")
        
        return jsonify({"error": str(e)}), 500





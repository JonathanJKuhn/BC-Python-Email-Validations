from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self, data):
        self.id = data['id']
        self.fname = data['first_name']
        self.lname = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __repr__( self ):
        return(
            f'Id: {self.id}\n'
            f'First Name: {self.fname}\n'
            f'Last Name: {self.lname}\n'
            f'Email: {self.email}\n'
            f'Created At: {self.created_at}\n'
            f'Updated At: {self.updated_at}\n'

        )
    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        res = connectToMySQL('users_schema').query_db(query, data)

        return cls(res[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_schema').query_db(query)
        users = []

        for user in results:
            users.append(cls(user))
        
        return users

    @staticmethod
    def add(data):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, NOW(), NOW());"

        return connectToMySQL('users_schema').query_db(query, data)
    @staticmethod
    def update(data):
        query = "UPDATE users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db(query, data) 
    
    @staticmethod
    def delete(data):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL('users_schema').query_db(query, data)

    @staticmethod
    def validate_user(user):
        # We want to make sure that user is giving us good data before querying the db
        is_valid = True
        if len(user['fname']) <= 0:
            flash("First Name must not be empty.")
            is_valid = False
        if len(user['lname']) <= 0:
            flash("Last Name must not be empty.")
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        
        # We want to make sure that the email isn't already in use
        if is_valid:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            result = connectToMySQL('users_schema').query_db(query, user)
            if result:
                flash("Email already exists.")
                is_valid = False

        return is_valid
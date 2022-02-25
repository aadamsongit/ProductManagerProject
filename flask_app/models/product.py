from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user

class Product:
    def __init__(self, data):
        self.id = data['id']
        self.product_name = data['product_name']
        self.quantity = data['quantity']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.user = []

    @staticmethod
    def validate_product(form_data):
        is_valid = True
        if len(form_data['product_name']) < 3:
            flash("Product name must be at least 3 characters long")
            is_valid = False
        if len(form_data['quantity']) < 1:
            flash("Quantity must be at least 1 characters long.")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters long")
            is_valid = False
        return is_valid

    @classmethod
    def add_product(cls, data):
        query = "INSERT INTO products (product_name, quantity, description, user_id, created_at, updated_at) VALUES (%(product_name)s, %(quantity)s, %(description)s, %(user_id)s, NOW(), NOW());"
        results = connectToMySQL('products_schema').query_db(query, data)
        return results

    @classmethod
    def all_products_this_user(cls, data):
        query = "SELECT * FROM products LEFT JOIN users ON users.id = %(user_id)s;"
        results = connectToMySQL('products_schema').query_db( query, data)

        all_products = []

        for row in results:
            product = cls(row)
            print(row['email'])

            user_data = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
            }

            product.user = user.User(user_data)
            all_products.append(product)

        return all_products

    @classmethod
    def get_one_product(cls, data):
            query = "SELECT * FROM products LEFT JOIN users on products.user_id = users.id WHERE products.id = %(id)s;"
            results = connectToMySQL('products_schema').query_db (query, data)

            product = cls(results[0])

            user_data = {
                "id" : results[0]['users.id'],
                "first_name" : results[0]['first_name'],
                "last_name" : results[0]['last_name'],
                "email" : results[0]['email'],
                "password" : results[0]['password'],
                "created_at" : results[0]['users.created_at'],
                "updated_at" : results[0]['users.updated_at'],
            }

            product.user = user.User(user_data)

            return product

    @classmethod
    def update_product(cls, data):
        query = "UPDATE products SET product_name = %(product_name)s, quantity = %(quantity)s, description = %(description)s, updated_at = NOW() WHERE id= %(id)s"
        results = connectToMySQL('products_schema').query_db(query, data)

        return results

    @classmethod
    def delete_product (cls, data):
        query = "DELETE FROM products WHERE id = %(id)s;"
        results = connectToMySQL('products_schema').query_db(query, data)
        return results 
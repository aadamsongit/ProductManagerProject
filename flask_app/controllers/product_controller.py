from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.product import Product

@app.route("/product/<int:id>")
def read_oneproduct(id):

    data = {
        
        "id": id
    }

    user_data = {
        
        "user_id": session["user_id"]
    }

    user = User.get_user_info(user_data)
    return render_template("showone.html", product = Product.get_one_product(data), user=user)

@app.route("/add_product", methods=['POST'])
def add_new_product():
    
    if "user_id" not in session: 
        return redirect("/logout")
    if not Product.validate_product(request.form):
        return redirect("/new")

    data = {
        "product_name" : request.form['product_name'],
        "quantity" : request.form['quantity'],
        "description" : request.form['description'],
        "user_id" : session['user_id']
    }
    
    Product.add_product(data)
    return redirect("/dashboard")

@app.route("/new")
def new_product():
    data = {
        "user_id" : session['user_id']
    }

    user = User.get_user_info(data)
    return render_template("add.html", user=user)

@app.route("/update/<int:id>", methods=['POST'])
def update_product(id):
    if not Product.validate_product(request.form):
        return redirect(f"/edit/{id}")

    data = {
        "id" : id,
        "product_name" : request.form['product_name'],
        "quantity" : request.form['quantity'],
        "description" : request.form['description'],
    }

    Product.update_product(data)
    return redirect("/dashboard")

@app.route("/edit/<int:id>")
def edit_product(id):
    data = {
        "id" : id
    }

    data1 = {
        "user_id" : session['user_id']
    }

    user = User.get_user_info(data1)
    product = Product.get_one_product(data)
    return render_template("edit.html", product=product, user=user)

@app.route("/<int:id>/delete")
def delete_product(id):

    data = {
        "id" : id,
    }

    Product.delete_product(data)
    return redirect("/dashboard")
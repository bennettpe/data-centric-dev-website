import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MONGODB CONFIGURATION
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb://admin_cookbook:Data_Centric_development_project04@ds229790.mlab.com:29790/online_cookbook'
mongo = PyMongo(app)

# INDEX/HOME PAGE
@app.route('/')

@app.route('/base')
def base():
    return render_template('base.html') 

# REGISTER USER
@app.route('/register_user')
def register_user():
    return render_template("register_user.html")
    
# SIGN IN USER
@app.route('/sign_in_user')
def sign_in_user():
    return render_template("sign_in_user.html")  
    
# ADD FORM RECIPE
@app.route('/add_form_recipe')
def add_form_recipe():
    return render_template("add_form_recipe.html") 
    
# EDIT FORM RECIPE
@app.route('/edit_form_recipe')
def edit_form_recipe():
    return render_template("edit_form_recipe.html") 
    
# LIST CUISINE RECIPES
@app.route('/list_cuisine_recipes')
def list_cuisine_recipes():
    return render_template("list_cuisine_recipes.html") 
    
# LIST ALL RECIPES
@app.route('/list_all_recipes')
def list_all_recipes():
    return render_template("list_all_recipes.html")  

# MY RECIPES
@app.route('/my_recipes')
def my_recipes():
    return render_template("my_recipes.html")  
    
# SEARCH RECIPES
@app.route('/search_recipes')
def search_recipes():
    return render_template("search_recipes.html")

# VIEW RECIPE
@app.route('/view_recipe')
def view_recipe():
    return render_template("view_recipe.html")    
    
# SITE STATISICS
@app.route('/site_statistics')
def site_statistics():
    return render_template("site_statistics.html")
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
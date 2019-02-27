import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from forms import RegisterForm, SigninForm

app = Flask(__name__)
app.secret_key = '5149fde2f2f15a6f77dddf0f319b20c6'

# BCRYPT CONFIGURATION
bcrypt = Bcrypt(app)

# MONGODB CONFIGURATION
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb://admin_cookbook:project04@ds213665.mlab.com:13665/online_cookbook'
                           
mongo = PyMongo(app)
    
# FUNCTION: GET ALLERGENS DB DOCUMENT
def get_allergens_document():
        allergens = mongo.db.allergens.find().sort("allergen_name", 1)
        return allergens
        
# FUNCTION: CREATE ALLERGENS LIST
def create_allergens_list():
        allergens_document = get_allergens_document()
        allergens_list = [allergens_record["allergen_name"]
                             for allergens_record in allergens_document] 
        return allergens_list     
        
# FUNCTION: GET CATEGORIES DB DOCUMENT
def get_categories_document():
        categories = mongo.db.categories.find().sort("category_name", 1)
        return categories

# FUNCTION: CREATE CATEGORIES LIST
def create_categories_list():
        categories_document = get_categories_document()
        categories_list = [categories_record["category_name"]
                             for categories_record in categories_document]
        return categories_list                      
                             
# FUNCTION: GET CUISINES DB DOCUMENT
def get_cuisines_document():
        cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)
        return cuisines 
        
# FUNCTION: CREATE CUISINES LIST
def create_cuisines_list():
        cuisines_document = get_cuisines_document()
        cuisines_list = [cuisines_record["cuisine_name"]
                             for cuisines_record in cuisines_document] 
        return cuisines_list         
      
# FUNCTION: GET DIFFICULTIES DB DOCUMENT
def get_difficulties_document():
        difficulties = mongo.db.difficulties.find().sort("difficulty_name", -1)
        return difficulties
        
# FUNCTION: CREATE DIFFICULTIES LIST
def create_difficulties_list():
        difficulties_document = get_difficulties_document()
        difficulties_list = [difficulties_record["difficulty_name"]
                             for difficulties_record in difficulties_document] 
        return difficulties_list 
        
# FUNCTION: GET MAIN INGREDIENTS DB DOCUMENT
def get_main_ingredients_document():
        main_ingredients = mongo.db.main_ingredients.find().sort("main_ingredient", 1)
        return main_ingredients
        
# FUNCTION: CREATE MAIN INGREDIENTS LIST
def create_main_ingredients_list():
        main_ingredients_document = get_main_ingredients_document()
        main_ingredients_list = [main_ingredients_record["main_ingredient"]
                             for main_ingredients_record in main_ingredients_document] 
        return main_ingredients_list 
        
# FUNCTION: GET RECIPES DB DOCUMENT
def get_recipes_document_by_cuisine():
        recipes = mongo.db.recipes.find().sort("recipe_name", 1)
        return recipes
  
    
# INDEX/HOME PAGE
@app.route('/')

@app.route('/base')
def base():
    if 'username' in session:
        return render_template('base.html',
        welcome_message ='Welcome ' + str(session['username']) + ' To')
        
    return render_template('base.html',
    welcome_message ='Welcome To')


# REGISTER NEW USER via WTForm
@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
                                
    if form.validate_on_submit():
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})
        
        # Check for existing user to avoid re-registering existing user
        if existing_user is None:
            # hash password using flask-bcrypt
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            # insert username & hashed password into mongo.db.users
            users.insert({'username':  request.form['username'], 'password' : hashed_password})
            session['username'] = request.form['username']
            return redirect(url_for('sign_in_user'))
        else:
            flash("Username already registered", 'danger')     
        
    return render_template("register_user.html", title='Register', form=form)

    
# SIGN IN USER via WTForm
@app.route('/sign_in_user',methods=['GET', 'POST'])
def sign_in_user():
    form = SigninForm()
    
    if form.validate_on_submit(): 
         if 'username' in session:
              flash("You are already signed in!")
         else:      
             users = mongo.db.users
             user_signin   = users.find_one({'username' : request.form['username']})
         
             # Check if username exsits in mongodb.
             if user_signin:
                 # Check if hashed password in mongo.db.users = password entered in WTForm.
                  if bcrypt.check_password_hash(user_signin['password'],(request.form['password']).encode('utf-8')):
                      session['username'] = request.form['username']
                      return redirect(url_for('search_recipes'))
                  else: 
                      flash("Invalid username or password", 'danger')    
        
    return render_template("sign_in_user.html", title='Signin', form=form)


# SIGN OUT USER
@app.route('/sign_out_user',methods=['GET', 'POST'])
def sign_out_user():
    if request.method == 'GET':
        session.pop('username', None)
        session.pop('_flashes', None)
        flash("you have signed out", 'success')
    return render_template("base.html")    

        
# BY RECIPE(S)
@app.route('/by_recipes')
def by_recipes():
        # allergens
        allergens_document = get_allergens_document()
        # list comprehensions used to create list
        allergens_list = [allergens_record["allergen_name"]
                             for allergens_record in allergens_document]
                             
        # categories
        categories_document = get_categories_document()
        categories_list = [categories_record["category_name"]
                             for categories_record in categories_document] 
                            
        # cuisines
        cuisines_document = get_cuisines_document()
        
        # difficulties                     
        difficulties_document = get_difficulties_document()
        difficulties_list = [difficulties_record["difficulty_name"]
                             for difficulties_record in difficulties_document]
        # Reverse difficulties_list
        difficulties_list = difficulties_list[::-1] 
        
        # main_ingredients
        main_ingredients_document = get_main_ingredients_document()
        main_ingredients_list = [main_ingredients_record["main_ingredient"]
                             for main_ingredients_record in main_ingredients_document] 

        return render_template("by_recipes.html", 
                                cuisines_document = cuisines_document,
                                allergens_list    = allergens_list,
                                categories_list   = categories_list,
                                difficulties_list = difficulties_list,
                                main_ingredients_list = main_ingredients_list,
                                welcome_message ='Welcome ' + str(session['username'])) 


# NOT BY ALLERGENS
@app.route('/not_by_allergen/<allergen_name>')
def not_by_allergen(allergen_name):
        recipes_document_by_allergen = mongo.db.recipes.find({"allergen_name": {'$nin': [allergen_name]}}).sort("cuisine_name", 1)
        # Counts total amount of recipes not by allergen selected
        recipe_allergen_count = mongo.db.recipes.find({"allergen_name": {'$nin': [allergen_name]}}).count()
        return render_template("not_by_allergen.html",
                                recipe_allergen_count        = recipe_allergen_count,
                                allergen_name                = allergen_name,
                                recipes_document_by_allergen = recipes_document_by_allergen)

                                
# BY CATEGORY
@app.route('/by_category/<category_name>')
def by_category(category_name):
        recipes_document_by_category = mongo.db.recipes.find({"category_name": category_name}).sort("cuisine_name", 1)
        # Counts total amount of recipes by category selected
        recipe_category_count = mongo.db.recipes.find({ "category_name": category_name }).count()
        return render_template("by_category.html",
                                recipe_category_count        = recipe_category_count,
                                category_name                = category_name,
                                recipes_document_by_category = recipes_document_by_category)


# BY CUISINE
@app.route('/by_cuisine/<cuisine_name>')
def by_cuisine(cuisine_name):
        recipes_document_by_cuisine = mongo.db.recipes.find({"cuisine_name": cuisine_name})
        # Counts total amount of recipes by cuisine seleted
        recipe_cuisine_count = mongo.db.recipes.find({ "cuisine_name": cuisine_name }).count()
        return render_template("by_cuisine.html", 
                                recipe_cuisine_count        = recipe_cuisine_count,
                                cuisine_name                = cuisine_name,
                                recipes_document_by_cuisine = recipes_document_by_cuisine)    
                                

# BY DIFFICULTY
@app.route('/by_difficulty/<difficulty_name>')
def by_difficulty(difficulty_name):
        recipes_document_by_difficulty = mongo.db.recipes.find({"difficulty_name": difficulty_name}).sort("cuisine_name", 1)
        # Counts total amount of recipes by difficulty selected
        recipe_difficulty_count = mongo.db.recipes.find({ "difficulty_name": difficulty_name }).count()
        return render_template("by_difficulty.html",
                                recipe_difficulty_count        = recipe_difficulty_count,
                                difficulty_name                = difficulty_name,
                                recipes_document_by_difficulty = recipes_document_by_difficulty)


# BY MAIN INGREDIENT
@app.route('/by_main_ingredient/<main_ingredient>')
def by_main_ingredient(main_ingredient):
        recipes_document_by_main_ingredient = mongo.db.recipes.find({"main_ingredient": main_ingredient}).sort("cuisine_name", 1)
        # Counts total amount of recipes by main ingredient selected
        recipe_main_ingredient_count = mongo.db.recipes.find({ "main_ingredient": main_ingredient }).count()
        return render_template("by_main_ingredient.html",
                                recipe_main_ingredient_count        = recipe_main_ingredient_count,
                                main_ingredient                     = main_ingredient,
                                recipes_document_by_main_ingredient = recipes_document_by_main_ingredient)


# BY MY RECIPES
@app.route('/by_my_recipes/<username>')
def by_my_recipes(username):
    if 'username' in session:
        user_document_by_signed_in_username = mongo.db.users.find_one({"username": username})
        recipes_document_by_signed_in       = mongo.db.recipes.find({"username": session['username']}).sort("cuisine_name", 1)
        recipes_document_by_signed_in_count = recipes_document_by_signed_in.count()
        return render_template("by_my_recipes.html",
                                recipes_document_by_signed_in_count = recipes_document_by_signed_in_count,
                                user_document_by_signed_in_username = user_document_by_signed_in_username,
                                recipes_document_by_signed_in       = recipes_document_by_signed_in,
                                message = "Your recipes")
    else:
        return redirect(url_for('index',
                        message="You don't have any recipes!"))
                                    
                                    
# VIEW DETAILS RECIPE
@app.route('/view_details_recipe/<recipe_id>')
def view_details_recipe(recipe_id):
       recipes_document_by_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
       return render_template("view_details_recipe.html",
                                recipes_document_by_recipe = recipes_document_by_recipe)


# VIEW MY DETAILS RECIPE
@app.route('/view_my_details_recipe/<recipe_id>')
def view_my_details_recipe(recipe_id):
       recipes_document_by_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
       return render_template("view_my_details_recipe.html",
                                recipes_document_by_recipe = recipes_document_by_recipe)
                                
                                
# ADD RECIPE
@app.route('/<username>/add_recipe',methods=['GET', 'POST'])
def add_recipe(username):
    allergens_list        = create_allergens_list()
    categories_list       = create_categories_list()
    cuisines_list         = create_cuisines_list()
    difficulties_list     = create_difficulties_list()
    # Reverse difficulties_list
    #difficulties_list = difficulties_list[::-1] 
    main_ingredients_list = create_main_ingredients_list()
    
    if 'username in session':
        username = session['username']
        if request.method == 'POST': 
           recipes = mongo.db.recipes
        
           # create required lists
           allergen_name_getlist         = request.form.getlist('allergen_name')
           allergen_name_list            = [i for i in allergen_name_getlist]
           category_name_getlist         = request.form.getlist('category_name')
           category_name_list            = [i for i in category_name_getlist]
           recipe_ingredients_list       = request.form.getlist('recipe_ingredient')
           recipe_ingredients_list_empty = [i for i in recipe_ingredients_list if i != ""]
           recipe_method_list            = request.form.getlist('recipe_method')
           recipe_method_list_empty      = [i for i in recipe_method_list if i != ""]
    
           # create new recipe
           new_recipe = {
            'allergen_name'      : allergen_name_list,
            'author_name'        : request.form.get('author_name'),
            'category_name'      : category_name_list,
            'cooking_time'       : request.form.get('cooking_time'),
            'cuisine_name'       : request.form.get('cuisine_name'),
            'difficulty_name'    : request.form.get('difficulty_name'),
            'main_ingredient'    : request.form.get('main_ingredient'),
            'preparation_time'   : request.form.get('preparation_time'),
            'recipe_description' : request.form.get('recipe_description'),
            'recipe_ingredients' : recipe_ingredients_list,
            'recipe_method'      : recipe_method_list,
            'recipe_name'        : request.form.get('recipe_name'),
            'recipe_url'         : request.form.get('recipe_url'),
            'ratings_score'      : int(0),
            'servings_num'       : request.form.get('servings_num'),
            'username'           : username
           }
           print(new_recipe)
           #insert new recipe into mongoDB recipes document
           recipes.insert_one(new_recipe)
           
           # Check main_ingredients document to see if main_ingredient added in recipe
           # already exists, if not add to main_ingredients document
           main_ingredient     = mongo.db.main_ingredients
           current_ingredients = main_ingredient.find_one({'main_ingredient': request.form.get('main_ingredient')})
           if request.form['main_ingredient']: 
                if current_ingredients is None:
                   main_ingredient.insert({
                   'main_ingredient': request.form.get('main_ingredient')
                   })
                return redirect(url_for('base'))    
        return render_template("add_recipe.html",
                                allergens_list        = allergens_list,
                                categories_list       = categories_list, 
                                cuisines_list         = cuisines_list,
                                difficulties_list     = difficulties_list,
                                main_ingredients_list = main_ingredients_list)
    return render_template('sign_in_user.html',
                   message='Please sign in to add your recipe!')                            


# DELETE RECIPE
@app.route('/<username>/delete_recipe/<recipe_id>')
def delete_recipe(username, recipe_id):
    if 'username' in session:
        # Delete selected recipe
        mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
        return redirect(url_for('by_my_recipes', username=session['username']))
    return render_template('sign_out_user.html',
                    message='Please sign in to delete your recipe!')


# EDIT RECIPE
@app.route('/<username>/edit_recipe/<recipe_id>', methods=['GET','POST'])
def edit_recipe(username, recipe_id):
    if 'username' in session:
        
        # find selected recipe
        find_my_recipe   = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        
        # split allergen_name into separate variables
        allergens_recipe = find_my_recipe['allergen_name']
        allergens_list   = create_allergens_list()
        print(allergens_recipe)
        print(allergens_list)
   
        # split category_name into separate variables
        categories_recipe = find_my_recipe['category_name']
        categories_list   = create_categories_list()
        print(categories_recipe)
        print(categories_list)
    
        return render_template('edit_recipe.html',
                                recipe                = find_my_recipe,
                                allergens_list        = allergens_list,
                                allergens_recipe      = allergens_recipe,
                                categories_list       = categories_list,
                                categories_recipe     = categories_recipe,
                                cuisines_list         = create_cuisines_list(),
                                difficulties_list     = create_difficulties_list(),
                                main_ingredients_list = create_main_ingredients_list(),
                                username  = session['username']) 
    return render_template('sign_in_user.html',
                   message='Please sign in to edit your recipe!')


# UPDATE RECIPE
@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    if 'username' in session:
        recipe = mongo.db.recipes
        # Update selected edited recipe
        recipe.update(
                {'_id': ObjectId(recipe_id)}, 
                {
                    'allergen_name': request.form.getlist('allergen_name'),
                    'author_name': request.form.get('author_name'),
                    'category_name': request.form.getlist('category_name'),
                    'cooking_time': request.form.get('cooking_time'),
                    'cuisine_name': request.form.get('cuisine_name'),
                    'difficulty_name': request.form.get('difficulty_name'),
                    'main_ingredient': request.form.get('main_ingredient'),
                    'preparation_time': request.form.get('preparation_time'),
                    'recipe_description': request.form.get('recipe_description'),
                    'recipe_ingredients': request.form.getlist('recipe_ingredients'),
                    'recipe_method': request.form.getlist('recipe_method'),
                    'recipe_name': request.form.get('recipe_name'),
                    'recipe_url': request.form.get('recipe_url'),
                    'ratings_score': request.form.get('ratings_score'),
                    'servings_num': request.form.get('servings_num'),
                    'username': session['username']
                })
        return redirect(url_for('view_my_details_recipe', recipe_id=recipe_id, username=session['username'])) 

                                        
# VOTE LIKE RECIPE
@app.route('/vote_like_recipe/<recipe_id>/<cuisine_name>', methods=["GET", "POST"])
def vote_like_recipe(recipe_id, cuisine_name):
    recipe = mongo.db.recipes
    recipe.update(
            {'_id': ObjectId(recipe_id)}, 
            {
                '$inc': {'ratings_score': 1} #Increment by +1
            })
    return redirect(url_for('vote_if_negative',
                             cuisine_name=cuisine_name))


# VOTE DISLIKE RECIPE
@app.route('/vote_dislike_recipe/<recipe_id>/<cuisine_name>', methods=["GET", "POST"])
def vote_dislike_recipe(recipe_id, cuisine_name):
    recipe = mongo.db.recipes
    recipe.update(
            {'_id': ObjectId(recipe_id)}, 
            {
                '$inc': {'ratings_score': -1} #Increment by -1
            })    
    return redirect(url_for('vote_if_negative',
                             cuisine_name=cuisine_name))   
 
 
# CHECK IF ANY VOTES ARE NEGATIVE AND SET TO ZERO
@app.route('/vote_if_negative/<cuisine_name>', methods=["GET", "POST"])
def vote_if_negative(cuisine_name):
    recipe = mongo.db.recipes
    recipe.update(
            {'ratings_score': { '$lt': 0 }}, 
            {
                 '$set': {'ratings_score': 0 }
            })
    return redirect(url_for('by_cuisine',
                             cuisine_name=cuisine_name))
                             
                             
# SITE STATISICS
@app.route('/site_statistics')
def site_statistics():
    return render_template("site_statistics.html")

    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
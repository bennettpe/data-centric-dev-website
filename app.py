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

           
# INDEX/HOME PAGE
@app.route('/')
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('base.html',
        recipes=mongo.db.recipes.find(),
        cuisines=mongo.db.cuisines.find(),
        categories=mongo.db.categories.find(),
        difficulties=mongo.db.difficulties.find(),
        main_ingredients=mongo.db.main_ingredients.find(),
        allergens=mongo.db.allergens.find(),
        welcome_message ='Welcome ' + str(session['username']) + ' To')
        
    return render_template('base.html',
    recipes=mongo.db.recipes.find(),
    cuisines=mongo.db.cuisines.find(),
    categories=mongo.db.categories.find(),
    difficulties=mongo.db.difficulties.find(),
    main_ingredients=mongo.db.main_ingredients.find(),
    allergens=mongo.db.allergens.find(),
    welcome_message ='Welcome To')


#REGISTER NEW USER via WTForm
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

    
#SIGN IN USER via WTForm
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


#SIGN OUT USER
@app.route('/sign_out_user',methods=['GET', 'POST'])
def sign_out_user():
    if request.method == 'GET':
        session.pop('username', None)
        session.pop('_flashes', None)
        flash("you have signed out", 'success')
    return render_template("base.html")    
        
    
# ADD FORM RECIPE
@app.route('/add_form_recipe')
def add_form_recipe():
    return render_template('add_form_recipe.html')

    
# EDIT FORM RECIPE
@app.route('/edit_form_recipe')
def edit_form_recipe():
    return render_template("edit_form_recipe.html") 

 
# LIST CATEGORY RECIPES
@app.route('/list_category_recipes/<category>')
def list_category_recipes(category):
    return render_template("list_category_recipes.html",
           categories=mongo.db.categories.find(),
           category=category)

        
# LIST CUISINE RECIPES
@app.route('/list_cuisine_recipes/<cuisine>')
def list_cuisine_recipes(cusine):
    return render_template("list_cuisine_recipes.html") 


# GET DIFFICULTIES DOCUMENT
@app.route('/get_difficulties_document')
def get_difficulties_document():
        return render_template("test.html", 
        difficulties=mongo.db.difficulties.find())

        
# LIST ALL RECIPES
@app.route('/list_all_recipes')
def list_all_recipes():
        return render_template('list_all_recipes.html',
        welcome_message ='Welcome ' + str(session['username'])) 

        
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
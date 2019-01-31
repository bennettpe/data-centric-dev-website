from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

#WTFORM FOR REGISTER USER
class RegisterForm(FlaskForm):
    username         = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
    password         = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=8, message='Password must be 8 characters long')]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    submit           = SubmitField('Register Account') 
    

# WTFORM FOR SIGN IN USER    
class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
    password = PasswordField('Password', validators=[DataRequired()]) 
    submit   = SubmitField('Sign In') 
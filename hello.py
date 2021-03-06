from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import InputRequired, Email, Length
from os import environ
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


myapp = Flask(__name__)
myapp.config['SECRET_KEY'] = 'Secretsecret'
myapp.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
myapp.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kacperus912@kacpert62200:Kochammatt912@kacpert62200.postgres.database.azure.com/Uzytkownicy'
myapp.debug = True
#'dbname='User' user='kacperus912@kacpert62200' host='kacpert62200.postgres.database.azure.com' password='Kochammatt912' port='5432' sslmode='true''
Bootstrap(myapp)
db = SQLAlchemy(myapp)
login_manager = LoginManager()
login_manager.init_app(myapp)
login_manager.login_view = 'login'

@myapp.route('/')

def hello():
    return render_template('index.html')

#Stworzenie bazy danych 
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
#####################################


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Formularz logowania i rejestracji
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Niepoprawny email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=8, max=80)])
###############################################


###############################################
@myapp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
       user = User.query.filter_by(username=form.username.data).first()
       if user:
           if check_password_hash(user.password, form.password.data):
               login_user(user, remember=form.remember.data)
               return redirect(url_for('dashboard'))
         
       return redirect('/blad')
        
        # return '<h1>' + form.username.data + ' ' + form.password.data
    return render_template('login.html',form=form)


######################################################
@myapp.route('/signup',  methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            return redirect('/nowy')
        except:
            return redirect('/blad')

        
       # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' +form.password.data

    return render_template('signup.html', form= form)
#####################################################################



@myapp.route('/nowy')
def nowy():
    return render_template('Nowyuzytkownik.html')

@myapp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@myapp.route('/blad')
def blad():
    return render_template('blad.html')

@myapp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello'))

##############################################################



if __name__ == '__main__':
    myapp.run()
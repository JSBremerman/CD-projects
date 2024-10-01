from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
bcrypt = Bcrypt(app)


@app.route('/')
def default():
    return redirect('/users/home_login')

@app.route('/users/home_login')
def home_login():
    return render_template('login.html')

@app.route('/users/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': session['user_id']}
    return render_template('home.html', user = User.get_user(data), recipes = Recipe.get_all())

@app.route('/users/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    id = User.save({
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    })
    session['user_id'] = id
    return redirect('/users/home')


@app.route('/users/login', methods=['POST'])
def login():
    user = User.check_email(request.form['email'])
    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Login Credentials', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/users/home')

@app.route('/users/logout')
def logout():
    session.clear()
    flash('Please login to continue', 'login')
    return redirect('/')
    






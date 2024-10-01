from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def users():
    return render_template('login_register.html')

@app.route('/users/create', methods=['POST']) 
def create():
    if not User.validate_registration(request.form):
        return redirect('/users')
    id = User.save({
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    })
    flash('Account registered', 'registration')
    session['user_id'] = id
    return redirect('/users/dashboard')

@app.route('/users/login', methods=['POST'])
def login():
    user = User.check_email(request.form['email'])
    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Credentials', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/users/dashboard')

@app.route('/users/logout')
def logout():
    session.clear()
    flash('Please login to continue', 'login')
    return redirect('/')

@app.route('/users/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Not logged in', 'login')
        return redirect('/')
    data = {'id': session['user_id']}
    return render_template('dashboard.html', user = User.get_this_user(data))



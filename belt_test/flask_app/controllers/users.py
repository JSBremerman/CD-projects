from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
bcrypt = Bcrypt(app)


@app.route('/')
def default():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
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
    return redirect('/dashboard')

@app.route('/login_user', methods=['POST'])
def login_user():
    user = User.check_email(request.form['email'])
    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Login Credentials', 'login')
        return redirect('/')
    session['user_id'] = user.id
    print('this is the session user id', user.id)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash('Please login to continue', 'login')
    return redirect('/')
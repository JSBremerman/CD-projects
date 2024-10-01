from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User

@app.route('/')
def users():
    return render_template('users.html', users = User.get_all())

@app.route('/create', methods=['POST'])
def create():
    session['form'] = {}
    data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            }
    user_info = User.validate_user(data)
    if user_info == True:
        id = User.save(data)
        return redirect(f'/show/{ id }')
    else:
        session['form'] = data
        return redirect('/create_user')

@app.route('/create_user')
def create_user():
    return render_template('create.html')

@app.route('/home')
def home():
    return redirect('/')

@app.route('/show/<int:id>')
def show(id):
    data = {'id': id}
    return render_template('show.html', user=User.get_one(data))

@app.route('/update/<int:id>')
def update_id(id):
    data = {'id': id}
    return render_template('update.html', user=User.get_one(data))

@app.route('/update', methods=['POST'])
def update():
    User.update(request.form)
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    User.delete(id)
    return redirect('/')

@app.route('/register/user', methods=['POST'])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'username': request.form['username'],
        'password': pw_hash
    }
    user_id = User.register(data)
    session['user_id'] = user_id
    return redirect('/dashboard')
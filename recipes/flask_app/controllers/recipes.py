from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
bcrypt = Bcrypt(app)


@app.route('/recipes/view/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': session['user_id']}
    id = {'id': id}
    return render_template('view_recipe.html', user = User.get_user(data), last = User.get_user(data), recipes = Recipe.get_one(id))

@app.route('/recipes/new')
def new_recipe():
    return render_template('add_recipe.html')

@app.route('/recipes/new/save', methods = ['POST'])
def save_recipe():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'dish_name': request.form['dish_name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_thirty': request.form['under_thirty'],
        'date': request.form['date']
    }
    Recipe.save_recipe(data)
    return redirect('/users/home')

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': id}
    return render_template('edit_recipe.html', recipe = Recipe.get_one_recipe(data))

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': id}
    Recipe.delete(data)
    return redirect('/users/home')


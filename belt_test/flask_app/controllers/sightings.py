from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
bcrypt = Bcrypt(app)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': session['user_id']}
    return render_template('dashboard.html', user=User.get_user(data), sightings = Sighting.get_all_sightings())

@app.route('/sighting/new')
def new_sighting():
    data = {'id': session['user_id']}
    return render_template('new_sighting.html', user = User.get_user(data))

@app.route('/sighting/view/<int:id>')
def view_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': session['user_id']}
    data2 = {'id': id}
    return render_template('view_sighting.html', user=User.get_user(data), sightings = Sighting.get_one_sighting(data2))

@app.route('/sighting/edit/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': id}
    data2 = {'id': session['user_id']}
    return render_template('edit_sighting.html', sighting = Sighting.edit_this_sighting(data), user=User.get_user(data2))

@app.route('/sighting/delete/<int:id>')
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': id}
    Sighting.delete(data)
    return redirect('/dashboard')

@app.route('/sighting/save', methods=['POST'])
def save_sighting():
    if 'user_id' not in session:
        return redirect('/')
    if not Sighting.validate_sighting(request.form):
        return redirect('/sighting/new')
    data = {
        'user_id': session['user_id'],
        'location': request.form['location'],
        'info': request.form['info'],
        'date': request.form['date'],
        'num_of_squatches': request.form['num_of_squatches']
    }
    Sighting.save_sighting(data)
    return redirect('/dashboard')

@app.route('/sighting/update/<int:id>', methods=['POST'])
def update_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Sighting.validate_sighting(request.form):
        return redirect(f'/sighting/edit/{id}')
    data = {
        'id': id,
        'location': request.form['location'],
        'info': request.form['info'],
        'date': request.form['date'],
        'num_of_squatches': request.form['num_of_squatches']
    }
    Sighting.update(data)
    return redirect('/dashboard')


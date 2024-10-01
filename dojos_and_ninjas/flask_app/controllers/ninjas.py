from flask import render_template, redirect, request

from flask_app import app

from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo

@app.route('/ninjas')
def ninjas():
    return render_template('ninjas.html', dojos = Dojo.get_all())

@app.route('/ninjas/add_ninja', methods=['POST'])
def add_ninja():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "age": request.form["age"],
        "dojo_id": request.form['dojo_id']
    }
    Ninja.save(data)
    return redirect(f"/dojos/{request.form['dojo_id']}")

@app.route('/ninjas/update/<int:id>')
def show_ninja(id):
    data = {'id': id}
    return render_template('edit.html',  ninja = Ninja.get_ninja(data))

@app.route('/ninjas/update/push/<int:id>', methods=['POST'])
def push_update(id):
    Ninja.update_ninja(request.form)
    return redirect(f'/dojos/{ id }')

@app.route('/ninjas/delete/<int:id>/<int:dojo_id>')
def delete(id, dojo_id):
    dojo_id = dojo_id
    Ninja.delete_ninja(id)
    return redirect(f'/dojos/{dojo_id}')

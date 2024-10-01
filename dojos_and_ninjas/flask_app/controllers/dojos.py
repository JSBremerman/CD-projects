from flask import render_template, redirect, request

from flask_app import app

from flask_app.models.dojo import Dojo


@app.route('/')
def home():
    return redirect('/dojos')

@app.route('/dojos')
def dojos():
    return render_template('dojos.html', dojos = Dojo.get_all())

@app.route('/ninjas_at_dojo')
def ninjas_at_dojo():
    return render_template('ninjas_at_dojo.html')

@app.route('/dojos/add_dojo', methods=['POST'])
def add_dojo():
    data = {'name': request.form['name'],}
    Dojo.save(data)
    return redirect('/dojos')

@app.route('/dojos/<int:id>')
def dojo_show(id):
    data = {'id': id}
    return render_template('dojo_show.html', dojo=Dojo.ninjas_at_dojo(data))

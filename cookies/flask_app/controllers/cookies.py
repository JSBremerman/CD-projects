from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.cookie import Cookie

@app.route('/')
def home():
    return redirect('/cookies')

@app.route('/cookies')
def cookies():
    return render_template('cookie_orders.html', users = Cookie.get_all())

@app.route('/cookies/edit/<int:id>')
def edit_cookies(id):
    data = {'id': id}
    return render_template('change_order.html', user = Cookie.get_user(data))

@app.route('/cookies/update/<int:id>', methods=['POST'])
def update_cookies(id):
    if not Cookie.is_valid(request.form):
        return redirect(f'/cookies/edit/{id}')
    Cookie.update_cookies({
        'id': request.form['id'],
        'name': request.form['name'],
        'cookie_type': request.form['cookie_type'],
        'num_of_boxes': request.form['num_of_boxes']
    })
    return redirect('/cookies')

@app.route('/cookies/new_order')
def new_cookies_order():
    return render_template('new_order.html')

@app.route('/cookies/order', methods=['POST'])
def order_cookies():
    if not Cookie.is_valid(request.form):
        return redirect('/cookies/new_order')
    Cookie.save({
        'name': request.form['name'],
        'cookie_type': request.form['cookie_type'],
        'num_of_boxes': request.form['num_of_boxes']
    })
    return redirect('/cookies')


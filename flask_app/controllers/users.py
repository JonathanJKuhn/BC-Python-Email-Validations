from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.user import User

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def users():
    userList = User.get_all()
    return render_template('/users.html', users=userList)

@app.route('/user/<int:userId>')
def show_user(userId):
    data = {'id': userId}
    user_data = User.get_user(data)
    return render_template('/user.html',user=user_data)

@app.route('/user/new')
def new_user():
    return render_template('/new.html')

@app.route('/user/create', methods=['POST'])
def create_user():
    data = {
        'fname': request.form.get('fname'),
        'lname': request.form.get('lname'),
        'email': request.form.get('email')
        }
    if not User.validate_user(data):
        for key in data:
            session[key] = data[key]
        return redirect('/user/new')
    session.clear()
    User.add(data)
    return redirect('/users')

@app.route('/user/<int:userId>/edit')
def edit_user(userId):
    data = {'id' : userId}
    user_data = User.get_user(data)
    return render_template('/edit.html',user=user_data)

@app.route('/user/<int:userId>/update', methods=['POST'])
def update_user(userId):
    data = {
        'id': request.form.get('id'),
        'fname': request.form.get('fname'),
        'lname': request.form.get('lname'),
        'email': request.form.get('email')
    }
    User.update(data)
    return redirect(f'/user/{userId}')

@app.route('/user/<int:userId>/delete')
def delete_user(userId):
    data = {'id': userId}
    User.delete(data)
    return redirect('/users')
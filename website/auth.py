import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User

auth = Blueprint('auth', __name__)
url = 'http://44.195.223.194:8000/'
url2 = 'http://3.214.121.253:8000/'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        data = {
            'email': email,
            'password_hash': password
        }
        response = requests.get(f'{url2}user', data=data)
        if response.status_code == 200:
            flash('Logged in succesfully!', category='success')
            response_data = response.json()
            if response_data:
                print("caca!")
                print(response_data[0])
                login_user(User(response_data[0]), remember=True)
                return redirect(url_for('views.home'))
        flash("Incorrect email or password, try again.", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')

        data = {
            name,
            lastname,
            email,
            password
        }
        response = requests.post(f'{url}users', data=data)
        if response.status_code == 200:
            registeredUser = response.json()
            # Ver como Juan está devolviendo la id al hacer post...
            data = {
                registeredUser['id'],
                name,
                lastname,
                email,
                password
            }

            login_user(User(data), remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash("Failed to add user.", category='error')
            
    return render_template("sign_up.html", user=current_user)

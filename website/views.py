from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .__init__ import url, url2
import requests

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        user_id = current_user.id
        title = request.form.get('title')
        description = request.form.get('description')
        data ={
            "title": title,
            "description": description
        }
        print(data)
        print(f'{url}user/{user_id}')        
        response = requests.post(f'{url}user/{user_id}', data=data)
        if response.status_code == 200:
            flash('Goal added succesfully!', category='success')
            response_data = response.json()
        else:
            flash("Error: Goal not added, try again.", category='error')

    goals = []
    response = requests.get(f'{url}user/{current_user.id}')
    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            goals = response_data
    print(goals)
    return render_template("home.html", user=current_user, goals=goals)
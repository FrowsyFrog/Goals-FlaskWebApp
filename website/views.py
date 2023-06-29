from flask import Blueprint, render_template, request, flash, redirect, url_for
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

@views.route('goal/delete/<int:goal_id>', methods=['POST'])
@login_required
def delete(goal_id):
    response = requests.delete(f'{url}goal/{goal_id}')
    if response.status_code == 200:
        flash('Goal deleted succesfully!', category='success')
    else:
        flash('Failed to delete goal.', category='error')
    
    return redirect(url_for('views.home'))

@views.route('/goal/edit/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def edit(goal_id):
    response = requests.get(f'{url}goal/{goal_id}')
    goal = response.json()
    print(goal)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        data = {
            "title": title,
            "description": description,
            "is_completed": 0
        }
        print(data)
        print(f'{url}goal/{goal[0]}')        
        response = requests.put(f'{url}goal/{goal_id}', data=data)
        if response.status_code == 200:
            flash('Goal updated successfully.', category='success')
        else:
            flash('Failed to update goal.', category='error')
        return redirect(url_for('views.home'))

    return render_template("goal.html", user=current_user, goal=goal)

@views.route('/comments/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def comments(goal_id):
    response = requests.get(f'{url}goal/{goal_id}')
    goal = response.json()
    print(goal)
    if request.method == 'POST':
        user_id = current_user.id
        content = request.form.get('content')
        data ={
            "content": content,
            "user_id": user_id,
            "goal_id": goal_id
        }
        print(data)
        print(f'{url2}comment/')        
        response = requests.post(f'{url2}comment/', data=data)
        if response.status_code == 200:
            flash('Comment added successfully!', category='success')
            response_data = response.json()
        else:
            flash("Failed to add comment.", category='error')

    comments = []
    response = requests.get(f'{url2}comments/{goal_id}')
    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            comments = response_data
    print(comments)
    return render_template("comments.html", user=current_user, goal=goal, comments=comments)

@views.route('/comment/edit/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    response = requests.get(f'{url2}comment/',data={"comment_id":comment_id})
    comment = response.json()
    print(comment)

    if request.method == 'POST':
        content = request.form.get('content')
        data = {
            "comment_id": comment_id,
            "content": content
        }
        print(data)
        print(f'{url2}comment/')        
        response = requests.put(f'{url2}comment/', data=data)
        if response.status_code == 200:
            flash('Comment updated successfully.', category='success')
        else:
            flash('Failed to update comment.', category='error')
        return redirect(url_for('views.home'))

    return render_template("comment.html", user=current_user, comment=comment)

@views.route('/comment/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    response = requests.delete(f'{url2}comment/', data={"comment_id": comment_id})
    if response.status_code == 200:
        flash('Comment deleted succesfully!', category='success')
    else:
        flash('Failed to delete comment.', category='error')
    
    return redirect(url_for('views.home'))
# This is the controller file
from flask import Flask, render_template, redirect, request, flash, session
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.sql import func
from sqlalchemy import update
import json
import model
import os
import requests
import jinja2


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/")
def welcome():
	"""The welcome page"""
	return render_template("welcome.html")

@app.route("/signup", methods=['GET'])
def show_signup():
    return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def signup():
    user_email = request.form.get('email')
    user_password = request.form.get('password') 

    new_user = model.User(email=user_email, password=user_password)
    
    model.session.add(new_user) 

    try:
        model.session.commit()
    except IntegrityError:
        flash("Email already in database. Please try again.")
        return show_signup()

    session.clear()
    flash("Signup successful. Please log in.")
    return show_login()

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")
    if session.get('user_email'):
        flash("You have successfully logged out.")
        session.clear()
   
@app.route("/login", methods=["POST"])
def login():
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    users = model.session.query(model.User)
    try:
        user = users.filter(model.User.email==user_email,
                            model.User.password==user_password
                            ).one()
    except InvalidRequestError:
        flash("That email or password was incorrect.")
        return render_template("login.html")

    session['user_email'] = user.email
    session['user_id'] = user.id
    session['count'] = 0
    
    return render_template("welcome.html")

# @app.route("/changepassword")
# def show_change_password():
#     """Displays the change password page"""
#     return render_template("changepassword.html", email=session['email'])

# @app.route("/changepassword", methods=['POST'])
# def change_password():
#     pass
#     """Change user password"""
    

# @app.route("/bookmarkcourse")
# def bookmark_course():
#     pass
#     # user_id = model.session.query(User).filter_by(email=session_email).first().id
#     # savedcourse = BookmarkedCourse.

#     # model.session.add()
    # model.session.commit()
    

# @app.route("/bookmarkedcourses", methods = ['GET'])
# def show_bookmarked_courses():
#     pass
#     """Show all the bookmarked courses from the database"""
    

# @app.route("/randomize", methods=['GET', 'POST'])
# def randomize():
#     pass
# """The app generates a course based on random course generator"""



@app.route("/Recommend", methods=['GET'])
def get_courses_by_criteria():
    """Queries the database based on user selections, and returns appropriate output"""
    category_chosen = request.args.get("category")
    #This gets the category's id
    get_category = model.session.query(model.Category.id).filter(model.Category.category_name==category_chosen).first()
    #Query the coursecategories table to find all courses which have the category id associated with the category chosen
    get_courses_associated_with_category = model.session.query(model.CourseCategory.course_id).filter(model.CourseCategory.category_id==get_category[0]).all()
    all_courses = []
    for i in get_courses_associated_with_category:
        get_course_name = model.session.query(model.Course.course_name).filter(model.Course.id==i[0]).all()
        all_courses.append(get_course_name)
    print all_courses
    

    #Duration selected 
    duration_chosen = request.args.get("duration")
    # durations = model.session.query(model.Term)
    print duration_chosen
    get_duration = model.session.query(model.Term.duration==duration_chosen).all()
    print get_duration

    workload_chosen = request.args.get("workload")
    workload = model.session.query(model.Course)
    get_course = workload.filter(model.Course.course_workload==workload_chosen).all()

    return render_template("recommended_courses.html", chosencategory=category_chosen, 
                                                       categories=all_courses, 
                                                       durations=duration_chosen,
                                                       workloads=workload_chosen) 


if __name__ == "__main__":
    app.run(debug=True)


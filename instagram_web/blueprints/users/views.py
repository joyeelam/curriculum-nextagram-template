from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.user import User
from instagram_web.util.helpers import upload_file_to_s3, allowed_file

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

# load form to create new user
@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

# records new user in the database
@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(username=username, email=email, password=password)
    if user.save():
        flash("User successfully created!")
        return redirect(url_for('sessions.new'))
    else:
        flash("Oh no, something went wrong. Please try again!", "error")
        return render_template("users/new.html", username=request.form['username'], email=request.form['email'], errors=user.errors)

# load form to edit user profile
@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    if current_user == user:
        return render_template('users/edit.html')
    else:
        flash("Uh oh! That wasn't your profile, we've retrieved your profile instead.", "error")
        return redirect(url_for('users.edit', id=current_user.id))

# makes changes to user's information in database
@users_blueprint.route('/<id>/update', methods=['POST'])
@login_required
def update(id):

    user = User.get_by_id(id)

    new_info = {}
    if request.form['username'] != "":
        new_info['username'] = request.form['username']
    if request.form['email'] != "":
        new_info['email'] = request.form['email']
    if request.form['password'] != "":
        new_info['password'] = request.form['password']

    if current_user == user:
        for key in new_info:
            # print(f"{key}: {new_info[key]}")
            setattr(user, key, new_info[key])
            user.save()
        if user.save():
            flash("Profile successfully updated.")
            return redirect(url_for('users.show', username=current_user.username))
        else:
            flash("Oh no, something went wrong. Please try again!", "error")
            return render_template("users/edit.html", errors=user.errors)
    else:
        flash("Oh no, something went wrong. Please try again", "error")
        return redirect(url_for('users.edit', id=current_user.id))

# upload profile picture via aws s3
@users_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def upload(id):

    user = User.get_by_id(id)
    file = request.files['user_file']

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        image_path = upload_file_to_s3(file, app.config['S3_BUCKET'])
        # print(image_path)
        user.profile_image = image_path
        if user.save():
            flash("Image uploaded successfully")
            return redirect(url_for('users.show', username=current_user.username))
        else:
            print(user.errors)
            flash("Error occurred", "error")
            return redirect(url_for('users.edit', id=current_user.id))

@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    return render_template('users/show.html')

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

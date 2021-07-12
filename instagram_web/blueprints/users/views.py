from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3, allowed_file
from models.user import User
from models.image import Image
from models.donation import Donation
from peewee import prefetch

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

# record changes to user's information in database
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
    if request.form['account_access'] == "private":
        new_info['private_account'] = True
    if request.form['account_access'] == "public":
        new_info['private_account'] = False

    if current_user == user:
        for key in new_info:
            # print(f"{key}: {new_info[key]}")
            setattr(user, key, new_info[key])
            user.save()
        if user.save():
            flash("Profile successfully updated.")
            return redirect(url_for('users.show', username=current_user.username))
        else:
            # print(user.errors)
            flash("Oh no, something went wrong. Please try again!", "error")
            return render_template("users/edit.html", errors=user.errors)
    else:
        flash("Oh no, something went wrong. Please try again!", "error")
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
            flash("Profile picture updated successfully.")
            return redirect(url_for('users.show', username=current_user.username))
        else:
            # print(user.errors)
            flash("Oh no, something went wrong. Please try again!", "error")
            return redirect(url_for('users.edit', id=current_user.id))

# delete user
@users_blueprint.route('/<id>/delete', methods=['POST'])
@login_required
def destroy(id):
    user = User.get_by_id(id)
    if user.id == current_user.id:
        if user.delete_instance():
            flash("We're sorry to see you go. Till the next time.")
            return redirect(url_for('home'))
        else:
            flash("Oops, looks like we're not ready to let you go yet.")
            return redirect(url_for('users.show', username=current_user.username))
    else:
        flash("Sneaky move! That wasn't your profile. Here's yours instead.")
        return redirect(url_for('users.show', username=current_user.username))

# show individual profile
@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    if user:
        images = user.images
        donations_list = []
        for image in images:
            donations = image.donations
            for donation in donations:
                # print(donation.amount)
                donations_list.append(donation.amount)
        # print(sum(donations_list))
        total_donations = sum(donations_list)
        return render_template('users/show.html', user=user, posts=images, donations=total_donations)
    else:
        flash("Couldn't locate that account", "error")
        return redirect(url_for('home'))

# show all public profiles
@users_blueprint.route('/', methods=["GET"])
def index():
    users = User.select().where(User.private_account == False)
    images = Image.select()
    users_with_images = prefetch(users, images)
    return render_template('users/index.html', users=users_with_images)

# search function to pull up specific profile by username
@users_blueprint.route('/search', methods=["POST"])
def search():
    user = User.get_or_none(User.username == request.form['username'].lower())
    if user:
        return redirect(url_for('users.show', username=user.username))
    else:
        flash("Couldn't locate that account", "error")
        return redirect(url_for('home'))

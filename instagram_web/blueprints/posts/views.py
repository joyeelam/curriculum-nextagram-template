from app import app
from peewee import prefetch
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from instagram_web.util.helpers import upload_file_to_s3, allowed_file
from instagram_web.util.payments import gateway
from werkzeug.utils import secure_filename
from models.user import User
from models.image import Image
from models.follow import Follow

posts_blueprint = Blueprint('posts', __name__, template_folder='templates')

# load form to create new post
@posts_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('posts/new.html')

# upload image via aws s3
@posts_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def create(id):
    user = User.get_by_id(id)
    file = request.files['image_file']
    caption = request.form['caption']

    if caption:
        caption = request.form['caption']
    else:
        caption = None

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        image_path = upload_file_to_s3(file, app.config['S3_BUCKET'])
        image = Image(image_url=image_path, image_caption=caption,  user_id=user.id)
        if image.save():
            flash('Post successfully created!')
            return redirect(url_for('users.show', username=user.username))
        else:
            # print(user.errors)
            flash("Error occurred", "error")
            return redirect(url_for('posts.new'))
    else:
        flash("Error occurred", "error")
        return redirect(url_for('posts.new'))

# load form to edit post
@posts_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    image = Image.get_or_none(Image.id == id)
    if image:
        return render_template("posts/edit.html", image=image)
    else:
        flash("Oh no, an error occurred.", "error")
        return redirect(url_for('users.show', username=current_user.username))

# make changes to post
@posts_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    image = Image.get_or_none(Image.id == id)
    caption = request.form['caption']
    if caption:
        image.image_caption = caption
        image.save()
        if image.save():
            return redirect(url_for('users.show', username=current_user.username))
        else:
            flash("Oh no, an error occurred.", "error")
            return redirect(url_for('users.show', username=current_user.username))
    else:
        flash("Oh no, an error occurred.", "error")
        return redirect(url_for('users.show', username=current_user.username))

# delete post
@posts_blueprint.route('/<id>/delete', methods=['POST'])
@login_required
def destroy(id):
    image = Image.get_or_none(Image.id == id)
    if image:
        image.delete_instance()
        flash("Post successfully deleted")
        return redirect(url_for('users.show', username=current_user.username))
    else:
        flash("Oh no, an error occurred.", "error")
        return redirect(url_for('users.show', username=current_user.username))

# view post
@posts_blueprint.route('/<id>', methods=['GET'])
def show(id):
    image = Image.get_or_none(Image.id == id)
    user = User.get_by_id(image.user_id)
    token = gateway.client_token.generate()
    if image:
        return render_template("posts/show.html", image=image, user=user, token=token)
    else:
        flash("Oh no, an error occurred.", "error")
        return redirect(url_for('users.index'))

# view all public posts
@posts_blueprint.route("/", methods=['GET'])
def index():
    users = User.select().where(User.private_account == False)
    images = (
                Image.select()
                    .join(User, on = User.id == Image.user_id)
                    .where(User.private_account == False)
                    .order_by(Image.created_at.desc())
                    .prefetch(users)
            )
    return render_template('posts/index.html', images=images)

# view posts from followed users
@posts_blueprint.route("/feed")
def feed():
    user = User.get_or_none(User.id == current_user.id)
    users = User.select()
    images = (
                Image.select()
                    .join(User, on = User.id == Image.user_id)
                    .join(Follow, on = Follow.creator_id == Image.user_id)
                    .where((Follow.follower == user) & (Follow.approval_status == True))
                    .order_by(Image.created_at.desc())
                    .prefetch(users)
            )
    return render_template('posts/feed.html', images=images)

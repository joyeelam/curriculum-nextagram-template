from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import User
from models.follow import Follow

followers_blueprint = Blueprint('followers', __name__, template_folder='templates')

# show all followers
@followers_blueprint.route('/<id>')
@login_required
def show(id):
    user = User.get_or_none(User.id == id)
    followers = (
                    User.select()
                        .join(Follow, on=Follow.follower_id == User.id)
                        .where(Follow.creator == user)
                )
    return render_template('followers/index.html', user=user, followers=followers)

# follow user
@followers_blueprint.route('/', methods=['POST'])
@login_required
def create():
    creator = User.get_or_none(User.id == request.form['creator'])
    follower = User.get_or_none(User.id == current_user.id)
    if creator and follower:
        follow = Follow(creator=creator, follower=follower)
        if follow.save():
            flash("User successfully followed")
            return redirect(url_for('users.show', username=creator.username))
        else:
            flash("Oh no, an error occurred", "error")
            return redirect(url_for('users.show', username=creator.username))

# unfollow user
@followers_blueprint.route('/<id>/delete', methods=['POST'])
@login_required
def destroy(id):
    creator = User.get_or_none(User.id == id)
    follow = Follow.get_or_none(Follow.creator_id == id)
    if follow.delete_instance():
        flash("Unfollow was successful")
        return redirect(url_for('users.show', username=creator.username))
    else:
        flash("Oh no, an error occurred", "error")
        return redirect(url_for('users.show', username=creator.username))

# create follow request
@followers_blueprint.route('/new')
@login_required
def new():
    creator = User.get_or_none(User.id == request.form['creator'])
    follower = User.get_or_none(User.id == current_user.id)
    follow_requests = []

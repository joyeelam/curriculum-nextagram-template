from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import User
from models.follow import Follow

followers_blueprint = Blueprint('followers', __name__, template_folder='templates')

# show all followers
@followers_blueprint.route('/<id>')
def show(id):
    user = User.get_or_none(User.id == id)
    followers = (
                    User.select()
                        .join(Follow, on = Follow.follower_id == User.id)
                        .where((Follow.creator == user) & (Follow.approval_status == True))
                )
    return render_template('followers/show.html', user=user, followers=followers)

@followers_blueprint.route('/<id>/following')
def index(id):
    user = User.get_or_none(User.id == id)
    following = (
                    User.select()
                        .join(Follow, on = Follow.creator_id == User.id)
                        .where((Follow.follower == user) & (Follow.approval_status == True))
                )
    return render_template('followers/index.html', user=user, following=following)

# follow user
@followers_blueprint.route('/', methods=['POST'])
@login_required
def create():
    creator = User.get_or_none(User.id == request.form['creator'])
    follower = User.get_or_none(User.id == current_user.id)
    if creator and follower:
        if creator.private_account:
            follow = Follow(creator=creator, follower=follower)
            if follow.save():
                flash("Follow request submitted successfully")
                return redirect(url_for('users.show', username=creator.username))
        else:
            follow = Follow(creator=creator, follower=follower, approval_status=True)
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
    follower = User.get_or_none(User.id == current_user.id)
    follow = Follow.get_or_none(Follow.creator_id == creator.id and Follow.follower_id == follower.id)
    if follow.delete_instance():
        flash("Unfollow was successful")
        return redirect(url_for('users.show', username=creator.username))
    else:
        flash("Oh no, an error occurred", "error")
        return redirect(url_for('users.show', username=creator.username))

# load form for follower requests pending approval
@followers_blueprint.route('/<id>/edit')
@login_required
def edit(id):
    user = User.get_or_none(User.id == id)
    followers = (
                    User.select()
                        .join(Follow, on=Follow.follower_id == User.id)
                        .where((Follow.creator == user) & (Follow.approval_status == False))
                )
    return render_template('followers/edit.html', user=user, followers=followers)

# approve follower requests
@followers_blueprint.route('/<id>', methods=['POST'])
@login_required
def approve(id):
    follow_request = Follow.get_or_none(Follow.follower_id == id)
    if follow_request:
        follow_request.approval_status = True
        if follow_request.save():
            flash("Follower request approved")
            return redirect(url_for('followers.edit', id=current_user.id))
    flash("Oh no, an error occurred", "error")
    return redirect(url_for('users.show', username=current_user.username))

# reject follower requests
@followers_blueprint.route('/<id>/reject', methods=['POST'])
@login_required
def reject(id):
    follow_request = Follow.get_or_none(Follow.follower_id == id)
    if follow_request:
        if follow_request.delete_instance():
            flash("Follower request rejected")
            return redirect(url_for('followers.edit', id=current_user.id))
    flash("Oh no, an error occurred", "error")
    return redirect(url_for('users.show', username=current_user.username))

from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User
from flask_login import LoginManager

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")

login_manager = LoginManager()
login_manager.init_app(app)

@app.errorhandler(401)
def unauthorized_access(e):
    return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    users = User.select()
    return render_template('home.html', users=users)
    
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.posts.views import posts_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.followers.views import followers_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(posts_blueprint, url_prefix="/posts")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(followers_blueprint, url_prefix="/followers")

@app.errorhandler(401)
def unauthorized_access(e):
    return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

import os
from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from blog.config import DevConfig, TestConfig, ProdConfig

# Declare flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
mail = Mail()
admin = Admin()


def create_app(config=None):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config: The configuration object to use.
    """
    app = Flask(__name__)

    if config is None or config == "Development":
        app.config.from_object(DevConfig)
    if config == "Testing":
        app.config.from_object(TestConfig)
    if config == "Production":
        app.config.from_object(ProdConfig)

    # Register Bluprints
    from blog.main.routes import main
    from blog.users.routes import users
    from blog.posts.routes import posts
    from blog.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    # Initialize flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    admin.init_app(app, index_view=MyAdminIndexView())

    return app


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.username == "admin"
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        abort(401)
        # redirect to login page if user doesn't have access
        # return redirect(url_for('login', next=request.url))

from flask import render_template, request, Blueprint, abort
from blog.models import Post
from blog.main.decorator import roles_required


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("main/home.html", posts=posts)


@main.route("/about")
@roles_required("admin")
def about():
    return render_template("main/about.html", title="About")

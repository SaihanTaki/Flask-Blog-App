from flask import render_template, redirect, request, url_for, flash, abort, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from blog import db
from blog.models import User, Post, Comment
from blog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__, url_prefix='/user')


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(message="Your account has been created!", category="success")
        return redirect(url_for("users.login"))
    return render_template("users/register.html", title="Sign Up", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            #password = check_password_hash(user.password, form.password.data)
            if user.check_password(form.password.data) or (user.password == form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Login Successful', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for("main.home"))
            else:
                flash(
                    'Login Unsuccessful. Please check your email and password', 'danger')
        else:
            flash('Login Unsuccessful. This email is not registerd', 'danger')

    return render_template("users/login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == "GET":  # showing the current info's in the form
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pictures/' + current_user.image_file)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template("users/account.html", title="Account", image_file=image_file, form=form, user=user)


@users.route("/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('users/user_post.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash(
                'An email has been sent with instructions to reset your password.', 'info')
        else:
            flash('This email is not registerd!', 'danger')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset Password', form=form)


@users.route('/<string:username>/delete', methods=['POST'])
@login_required
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        abort(403)
    if user:

        Post.query.filter_by(author=user).delete()
        Comment.query.filter_by(commenter=user).delete()
        # Comment.query.filter_by(article=user.posts).delete()
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('main.home'))

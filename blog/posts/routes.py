from flask import render_template, redirect, request, url_for, flash, abort, Blueprint
from flask_login import current_user, login_required
from blog.models import Post, Comment
from blog import db
from blog.posts.forms import PostForm, AddCommentForm

posts = Blueprint('posts', __name__, url_prefix='/post')


@posts.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for("main.home"))
    return render_template("posts/create_post.html", title="New Post", form=form, legend='New Post')


@posts.route("/<int:post_id>", methods=["GET", "POST"])
def read_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(article=post).all()
    form = AddCommentForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            comment = Comment(comment=form.comment.data,
                              article=post, commenter=current_user)
            db.session.add(comment)
            db.session.commit()
            flash("Your comment has been added to the post", "success")
            return redirect(url_for("posts.read_post", post_id=post.id))
    return render_template("posts/read_post.html",
                           title=post.title, post=post,
                           comments=comments, form=form)


@posts.route("/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.author = current_user
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.read_post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("posts/create_post.html",
                           title="Update Post",
                           form=form,
                           legend='Update Post')


@posts.post("/<int:post_id>/delete")
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.post("/<int:post_id>/comment/<int:comment_id>/delete")
@login_required
def delete_comment(comment_id, post_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    if comment.article == post:
        if comment.commenter != current_user:
            abort(403)
        db.session.delete(comment)
        db.session.commit()
    else:
        abort(403)
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('posts.read_post', post_id=post.id))

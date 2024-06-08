from flask import url_for
from blog.models import Post,User,Comment

def register(client,username,email,password,confirm_password):
    return client.post(url_for("users.register"), data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password
    ), follow_redirects=True)

def login(client, email, password,remember):
    return client.post(url_for("users.login"), data=dict(
            email=email,
            password=password,
            remember=remember
    ), follow_redirects=True)


def logout(client):
    return client.get(url_for("users.logout"), follow_redirects=True)

def update(client,username,email):
    return client.post(url_for("users.account"), data=dict(
            username=username,
            email=email
    ), follow_redirects=True)


def create_post(client,title,content,author):
    return client.post(url_for("posts.create_post"), data=dict(
            title=title,
            content=content,
            author=author
    ), follow_redirects=True)

def update_post(client,title,content):
    return client.post(url_for('posts.update_post', post_id=1), data=dict(
            title=title,
            content=content
    ), follow_redirects=True)

def delete_post(client):
    return client.post(url_for('posts.delete_post', post_id=1), follow_redirects=True)


def comment(client,comment,commenter,article):
    return client.post(url_for('posts.read_post', post_id=1), data=dict(
            comment=comment,
            commenter=commenter,
            article=article
    ), follow_redirects=True)

def delete_comment(client):
    return client.post(url_for('posts.delete_comment', post_id=1, comment_id=1), follow_redirects=True)



    

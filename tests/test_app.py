from flask import url_for
from flask_login import current_user
from tests.utils import register,login,logout,update,create_post,update_post,delete_post,delete_comment,comment
from blog.models import Post,Comment



def test_new_user(new_user):
    assert new_user.username == "tester"
    assert new_user.email == 'tester@gmail.com'
    assert new_user.check_password("password") == True

def test_new_post(new_post,new_user):
    assert new_post.title == "A Post"
    assert new_post.content == "bla bla bla"
    assert new_post.author == new_user
    assert new_post.user_id == new_user.id

def test_new_comment(new_comment,new_user,new_post):
    assert new_comment.comment == "bla"
    assert new_comment.article == new_post
    assert new_comment.commenter == new_user
    assert new_comment.commenter_id == new_user.id
    assert new_comment.post_id == new_post.id


def test_home_page(client):
    response1 = client.get('/')
    response2 = client.get('/home')
    assert response1.status_code == 200
    assert response2.status_code == 200




def test_login_page(client):
    response = client.get('/user/login')
    assert response.status_code == 200

def test_register_page(client):
    response = client.get('/user/register')
    assert response.status_code == 200




def test_register_user(client,new_user):
    """Make sure registration works."""
    username = new_user.username
    email = new_user.email
    password = new_user.password

    rv = register(client,username,email,password,password)
    assert b'Your account has been created!' in rv.data
    assert rv.status_code == 200

    
    rv = register(client,username,email,password,password)
    assert b'That email is taken. Please choose a different one.' in rv.data
    assert b'That username is taken. Please choose a different one.' in rv.data
    assert rv.status_code == 200



def test_login_logout_user(client,new_user):
    """Make sure login logout works."""
    username = new_user.username
    email = new_user.email
    password = new_user.password

    rv = login(client, email, password, False)
    assert b'Login Successful' in rv.data
    assert rv.status_code == 200

    rv = logout(client)
    assert b'<a class="nav-link" href="/user/logout">Logout</a>' not in rv.data
    assert rv.status_code == 200

    rv = login(client, email, password+"x", False)
    assert b'Login Unsuccessful. Please check your email and password' in rv.data
    assert rv.status_code == 200

    email = "notregisterd@gmail.com"
    rv = login(client, email, password, False)
    assert b'Login Unsuccessful. This email is not registerd' in rv.data
    assert rv.status_code == 200

def test_update_user(client,new_user):

    username = new_user.username
    email = new_user.email
    password = new_user.password

    login(client, email, password, False)

    username = "update"
    email = "update@gmail.com"

    rv = update(client,username,email)
    assert rv.status_code == 200
    assert b'Your account has been updated!' in rv.data
    assert current_user.email == email
    assert current_user.username == username

##################### Test About Page ###########################

def test_about_page_not_logged_in_and_unauthorized(client):
    response = client.get('/about')
    assert response.status_code == 401

def test_about_page_logged_in_and_unauthorized(client,user_reg_log):
    response = client.get('/about')
    assert response.status_code == 401

def test_about_page_authorized(client,admin_reg_log):
    response = client.get('/about')
    assert response.status_code == 200

######################## Test Posts ##############################

def test_create_update_delete_post(client,user_reg_log,new_post):


    rv = create_post(client,new_post.title,new_post.content,author=current_user)
    post = Post.query.get(1)
    assert rv.status_code == 200
    assert b'Your post has been created!' in rv.data
    assert post.title == new_post.title

    rv = update_post(client, title="updated", content="hey bro new")
    post = Post.query.get(1)
    assert rv.status_code == 200
    assert b'Your post has been updated!' in rv.data
    assert post.title == "updated"

    rv = delete_post(client)
    post = Post.query.get(1)
    assert rv.status_code == 200
    assert b'Your post has been deleted!' in rv.data
    assert post == None


def test_create_delete_comment(client,user_reg_log,new_post,new_comment):

    create_post(client,new_post.title,new_post.content,author=current_user)
    post = Post.query.get(1)

    rv = comment(client,comment=new_comment.comment,commenter=current_user,article=post)
    mycomment = Comment.query.get(1)
    assert rv.status_code == 200
    assert b'Your comment has been added to the post' in rv.data
    assert mycomment.comment == new_comment.comment

    rv = delete_comment(client)
    mycomment = Comment.query.get(1)
    assert rv.status_code == 200
    assert b'Your comment has been deleted!' in rv.data
    assert mycomment == None


    

# all the fixtures goes here
import os
import pytest
import factory 
from factory import Factory, Faker, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from blog import create_app,db
from blog.models import User, Post, Comment
from tests.utils import register,login,logout
from flask_login import current_user, login_user, logout_user


app = create_app(config="Testing")


@pytest.fixture(scope='session')
def client():
    app = create_app(config="Testing")

    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client

    try:
        os.remove("blog/test.sqlite")
    except:
        pass



    

@pytest.fixture(scope='module')
def new_user():
    user = User("tester", "tester@gmail.com", "password")
    return user


@pytest.fixture(scope='module')
def new_post(new_user):
    post = Post("A Post", "bla bla bla", author=new_user)
    return post


@pytest.fixture(scope='module')
def new_comment(new_user, new_post):
    comment = Comment("bla", commenter=new_user, article=new_post)
    return comment


@pytest.fixture(scope='module')
def admin_user():
    user = User("admin", "admin@gmail.com", "1234")
    return user

@pytest.fixture(scope='function')
def admin_reg_log(client,admin_user,request):
    if current_user.is_authenticated:
        logout(client)
    username = admin_user.username
    email = admin_user.email
    password = admin_user.password
    register(client,username,email,password,password)
    login(client, email, password, False)
    

@pytest.fixture(scope='function')
def user_reg_log(client,new_user,request):
    if current_user.is_authenticated:
        logout(client)
    username = new_user.username
    email = new_user.email
    password = new_user.password
    register(client,username,email,password,password)
    login(client, email, password, False)

@pytest.fixture(scope='function')
def user_logibz(client,new_user,request):
    if current_user.is_authenticated:
        logout(client)
    username = new_user.username
    email = new_user.email
    password = new_user.password
    register(client,username,email,password,password)
    login(client, email, password, False)


    

# @pytest.fixture
# def logged_in_user(request, new_user):
#     login_user(new_user)
#     request.addfinalizer(logout_user)

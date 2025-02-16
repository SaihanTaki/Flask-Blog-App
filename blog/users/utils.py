import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

    return None


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, extension = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + extension
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pictures', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

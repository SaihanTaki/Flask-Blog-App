from functools import wraps
from flask_login import current_user
from flask import abort


def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated:
                if current_user.username not in roles:
                    # Redirect the user to an unauthorized notice!
                    abort(401)
            else:
                abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
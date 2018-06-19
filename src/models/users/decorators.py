from functools import wraps

from flask import session, url_for, redirect, request


def requires_login(func):
    @wraps(func)  # wrap the func with decorated_function
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))  # after login, go to next
        return func(*args, **kwargs)
    return decorated_function
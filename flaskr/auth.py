import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flaskr.db import get_db
from flaskr.models import User

bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Create a new blog user."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        db = get_db()
        error = None
        if not username:
            error = 'Username is required!'
        elif not password:
            error = 'Password is required!'
        elif User.query.filter_by(username=username).first() is not None:
            error = 'User {} is already registered!'.format(username)
        if error is None:
            user = User(username=username, first_name=first_name, last_name=last_name)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Login user and redirect to main page."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            error = 'Incorrect username or password!'
        if error is None:
            session.clear()
            session['user_id'] = user.id_
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """Check if user is logged in, and if so, add the user to Flask `g` object."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout')
def logout():
    """Logout user and redirect to main page."""
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """A decoratior used to check if user is logged in."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

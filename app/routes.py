from flask import Blueprint, render_template, request, session, redirect, url_for

from . import utils as f

app = Blueprint('main', __name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html', user=session.get('user'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    if f.authenticate_user(username, password):
        f.add_user_to_session(username)
        return redirect(url_for('index'))
    else:
        return render_template('login.html', err=True)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    rf = request.form
    f.new_user(rf['username'], rf['password'], rf['sex'], rf['cooking_level'])
    f.add_user_to_session(rf['username'])
    return redirect(url_for('index'))


@app.route('/user')
@f.login_required
def user():
    return render_template('user.html')


@app.route('/reset-password', methods=['GET', 'POST'])
@f.login_required
def reset_password():
    if request.method == 'GET':
        return render_template('register.html')

    password = request.form['password']
    f.change_password(session['user']['username'], password)
    return redirect(url_for('user'))

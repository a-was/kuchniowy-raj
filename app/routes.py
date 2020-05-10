from flask import Blueprint, render_template, request, session, redirect, url_for

from . import utils as f

app = Blueprint('main', __name__, template_folder='templates')


@app.route('/')
def index():
    name = request.args.get('name', 'World')
    return render_template('index.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')
    if f.authenticate_user(username, password):
        session['user'] = {
            'username': username
        }
        return redirect(url_for('index'))
    else:
        return render_template('login.html', err=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    rf = request.form
    f.new_user(rf['nick'], rf['mail'], rf['cooking_level'], rf['sex'], rf['password'])
    return redirect(url_for('index'))

from flask import Blueprint, render_template, request, session, redirect, url_for

from . import utils as f
from .utils import login_required

app = Blueprint('main', __name__, template_folder='templates')


@app.route('/')
def index():
    print(session.get('user'))
    return render_template('index.html')


@app.route('/logowanie', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('logowanie.html')

    username = request.form.get('username')
    password = request.form.get('password')
    if f.authenticate_user(username, password):
        f.add_user_to_session(username)
        return redirect(url_for('.index'))
    else:
        return render_template('logowanie.html', err=True)


@app.route('/wyloguj')
@login_required
def logout():
    session.clear()
    return redirect(url_for('.index'))


@app.route('/rejestracja', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rejestracja.html', cooking_levels=f.get_cooking_levels_list())
    rf = request.form
    f.new_user(rf['username'], rf['password'], rf['sex'], rf['cooking_level'])
    f.add_user_to_session(rf['username'])
    return redirect(url_for('.index'))


@app.route('/profil')
@login_required
def user_profile():
    return render_template('profil.html')


# @app.route('/reset-password', methods=['GET', 'POST'])
# @f.login_required
# def reset_password():
#     if request.method == 'GET':
#         return render_template('register.html')
#
#     password = request.form['password']
#     f.change_password(session['user']['username'], password)
#     return redirect(url_for('user'))

@app.route('/admin')
@login_required
def admin():
    return render_template('administrator.html')


@app.route('/dodaj-przepis')
def new_recipe():
    return render_template('dodaj_przepis.html')


@app.route('/o-nas')
def about_us():
    return render_template('/o_nas.html')

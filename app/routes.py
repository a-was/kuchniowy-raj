from flask import Blueprint, render_template, request, session, redirect, url_for

from .utils.messages import info_message, success_message, warning_message, error_message
from .utils.sessions import login_required, admin_required, add_user_to_session
from .utils import users as u
from .utils import cooking_levels as cl

app = Blueprint('main', __name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logowanie', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('logowanie.html')

    username = request.form.get('username')
    password = request.form.get('password')
    if u.authenticate_user(username, password):
        add_user_to_session(username)
        return redirect(url_for('.index'))
    else:
        return render_template('logowanie.html', msg=error_message('Podano błędny login i/lub hasło'))


@app.route('/wyloguj')
@login_required
def logout():
    session.clear()
    return redirect(url_for('.index'))


@app.route('/rejestracja', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rejestracja.html', cooking_levels=cl.get_cooking_levels())

    user_login = request.form.get('username')
    user_sex = request.form.get('sex')
    user_cooking_level = request.form.get('cooking_level')
    user_password1 = request.form.get('password1')
    user_password2 = request.form.get('password2')

    if not u.exists(user_login):
        if u.validate_passwords(user_password1, user_password2):
            u.new_user(user_login, user_password1, user_sex, user_cooking_level)
            add_user_to_session(user_login)
            return redirect(url_for('.index'))
        else:
            return render_template('rejestracja.html', msg=error_message('Podane hasła nie są takie same'))
    else:
        return render_template('rejestracja.html', msg=error_message('Ta nazwa użytkownika jest już zajęta'),
                               cooking_levels=cl.get_cooking_levels())


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
@admin_required
def admin():
    return render_template('administrator.html')


@app.route('/dodaj-przepis')
def new_recipe():
    return render_template('dodaj_przepis.html')


@app.route('/o-nas')
def about_us():
    return render_template('/o_nas.html')

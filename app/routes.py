from flask import Blueprint, render_template, request, session, redirect, url_for

from .utils.messages import info_message, success_message, warning_message, error_message
from .utils.sessions import login_required, admin_required, add_user_to_session, get_user_id
from .utils import users as u
from .utils import recipies as r
from .utils import cooking_levels as cl
from .utils import food_categories as fc
from .utils import types_of_food as tof

app = Blueprint('main', __name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html',
                           recipes=r.get_recipes_list(True),
                           daily_recipe=r.get_daily_recipe())


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

    if u.exists(user_login):
        return render_template('rejestracja.html',
                               msg=error_message('Ta nazwa użytkownika jest już zajęta'),
                               cooking_levels=cl.get_cooking_levels())

    if not u.validate_username(user_login):
        return render_template('rejestracja.html',
                               msg=error_message('Nazwa użytkownika może składać się jedynie z liter i cyfr, '
                                                 'od 4 do 12 znaków'),
                               cooking_levels=cl.get_cooking_levels())

    if user_password1 != user_password2:
        return render_template('rejestracja.html',
                               msg=error_message('Podane hasła nie są takie same'),
                               cooking_levels=cl.get_cooking_levels())

    if not u.validate_passwords(user_password1, user_password2):
        return render_template('rejestracja.html',
                               msg=error_message('Podane hasła nie spełniają wymogów bezpieczeństwa'),
                               cooking_levels=cl.get_cooking_levels())

    u.new_user(user_login, user_password1, user_sex, user_cooking_level)
    add_user_to_session(user_login)
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
@admin_required
def admin():
    return render_template('administrator.html')


@app.route('/dodaj-przepis', methods=['GET', 'POST'])
@login_required
def new_recipe():
    food_categories = fc.get_food_categories_list()
    types_of_food = tof.get_types_of_food_list()

    if request.method == 'GET':
        return render_template('dodaj_przepis.html',
                               food_categories=food_categories,
                               types_of_food=types_of_food)

    recipe_name = request.form.get('name')
    recipe_type = request.form.get('type')
    recipe_food_category = request.form.get('category')
    recipe_time_required = request.form.get('time')
    recipe_description = request.form.get('description')
    # recipe_level = request.form.get('cooking_level')

    if r.recipe_exists(recipe_name):
        return render_template('dodaj_przepis.html',
                               msg=error_message('Przepis o takiej nazwie już istnieje'),
                               food_categories=food_categories,
                               types_of_food=types_of_food)

    r.new_recipe(get_user_id(), recipe_name, recipe_type, recipe_food_category, recipe_description,
                 recipe_time_required)
    return render_template('dodaj_przepis.html',
                           msg=success_message('Przepis pomyślnie dodano, '
                                               'czeka on na zatwierdzenie przez administratora'),
                           food_categories=food_categories,
                           types_of_food=types_of_food)


@app.route('/o-nas')
def about_us():
    return render_template('/o_nas.html')

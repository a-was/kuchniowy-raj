from flask import Blueprint, render_template, request, session, redirect, url_for, abort

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
    return render_template('index.html', recipes=r.get_recipes_list(True), daily_recipe=r.get_daily_recipe())


@app.route('/o-nas')
def about_us():
    return render_template('/o_nas.html')


@app.route('/logowanie', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('logowanie.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if any(v is None for v in [username, password]):
        return render_template('logowanie.html', msg=error_message('Nie wypełniono wszystkich pól'))

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
    cooking_levels = cl.get_cooking_levels()
    if request.method == 'GET':
        return render_template('rejestracja.html', cooking_levels=cooking_levels)

    user_login = request.form.get('username')
    user_sex = request.form.get('sex')
    user_cooking_level = request.form.get('cooking_level')
    user_password1 = request.form.get('password1')
    user_password2 = request.form.get('password2')

    if any(v is None for v in [user_login, user_sex, user_cooking_level, user_password1, user_password2]):
        return render_template('rejestracja.html',
                               msg=error_message('Nie wypełniono wszystkich pól'),
                               cooking_levels=cooking_levels)

    if u.exists(user_login):
        return render_template('rejestracja.html',
                               msg=error_message('Ta nazwa użytkownika jest już zajęta'),
                               cooking_levels=cooking_levels)

    if not u.validate_username(user_login):
        msg = 'Nazwa użytkownika może składać się jedynie z liter i cyfr, od 4 do 12 znaków'
        return render_template('rejestracja.html',
                               msg=error_message(msg),
                               cooking_levels=cooking_levels)

    if user_password1 != user_password2:
        return render_template('rejestracja.html',
                               msg=error_message('Podane hasła nie są takie same'),
                               cooking_levels=cooking_levels)

    if not u.validate_passwords(user_password1, user_password2):
        return render_template('rejestracja.html',
                               msg=error_message('Podane hasło nie spełnia wymogów bezpieczeństwa'),
                               cooking_levels=cooking_levels)

    u.new_user(user_login, user_password1, user_sex, user_cooking_level)
    add_user_to_session(user_login)
    # return redirect(url_for('.index', recipes=r.get_recipes_list(True), daily_recipe=r.get_daily_recipe()))
    return redirect(url_for('.index'))


@app.route('/profil', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'GET':
        return render_template('profil.html')

    new_password1 = request.form.get('password1')
    new_password2 = request.form.get('password2')

    if any(v is None for v in [new_password1, new_password2]):
        return render_template('profil.html', msg=error_message('Nie wypełniono wszystkich pól'))

    if new_password1 != new_password2:
        return render_template('profil.html', msg=error_message('Podane hasła nie są takie same'))

    if not u.validate_passwords(new_password1, new_password2):
        return render_template('profil.html', msg=error_message('Podane hasło nie spełnia wymogów bezpieczeństwa'))
    return render_template('profil.html', msg=success_message('Hasło zaktualizowane'))


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
    return render_template('administrator.html',
                           recipes_to_check=r.get_recipes_list(False),
                           users=u.get_all_users())


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

    if any(v is None for v in [recipe_name, recipe_type, recipe_food_category, recipe_time_required,
                               recipe_description]):
        return render_template('dodaj_przepis.html',
                               msg=error_message('Nie wypełniono wszystkich pól'),
                               food_categories=food_categories,
                               types_of_food=types_of_food)

    if r.recipe_exists(recipe_name):
        return render_template('dodaj_przepis.html',
                               msg=error_message('Przepis o takiej nazwie już istnieje'),
                               food_categories=food_categories,
                               types_of_food=types_of_food)

    if len(recipe_description) < 50 or len(recipe_description) > 5000:
        return render_template('dodaj_przepis.html',
                               msg=error_message('Opis powinien mieć od 50 do 5000 znaków'),
                               food_categories=food_categories,
                               types_of_food=types_of_food)

    r.new_recipe(get_user_id(), recipe_name, recipe_type, recipe_food_category, recipe_description,
                 recipe_time_required)
    msg = 'Przepis pomyślnie dodano, czeka on na zatwierdzenie przez administratora'
    return render_template('dodaj_przepis.html',
                           msg=success_message(msg),
                           food_categories=food_categories,
                           types_of_food=types_of_food)


@app.route('/przepis/<int:recipe_id>')
def get_recipe(recipe_id):
    if r.recipe_checked(recipe_id):
        r.add_view(recipe_id)
        return render_template('przepis.html', recipe=r.get_recipe(recipe_id))
    else:
        abort(404)


@app.route('/przepis/<int:recipe_id>/akceptuj')
@login_required
@admin_required
def accept_recipe(recipe_id):
    r.accept_recipe(recipe_id)
    return redirect(url_for('.admin'))


@app.route('/przepis/<int:recipe_id>/odrzuc')
@login_required
@admin_required
def delete_recipe(recipe_id):
    r.delete_recipe(recipe_id)
    return redirect(url_for('.admin'))


@app.route('/szukaj')
def search():
    query = request.args.get('q')
    type_ = request.args.get('typ')
    if type_ not in ['nazwa', 'typ', 'kategoria']:
        abort(406)
    recipes = r.search_recipes(query, type_, True)
    return render_template('szukaj.html', recipes=recipes)

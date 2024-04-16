import utils
from main import Application
from mysql.connector.errors import OperationalError
from flask import request, render_template, session, redirect


def setup_error_handlers(app: Application):
    @app.errorhandler(404)
    def error404(error):
        return render_template('404.html'), error.code

    @app.errorhandler(500)
    def error500(error):
        return render_template('500.html'), error.code

    @app.errorhandler(OperationalError)
    def database_error(error):
        """ Обработка потери соединения с БД """
        app.manager.connection = None
        app.manager.connect()
        if app.manager.connection:
            last_path = f'/{request.url.split("/")[-1]}'
            return redirect(last_path)
        else:
            return render_template('500.html'), error.code


def index():
    if session:
        return redirect('/customers')
    else:
        return redirect('/login')


def reset(app: Application):
    session.clear()
    app.manager.drop_tables()
    app.manager.make_initial_tables()
    return redirect('/login')


def login(app: Application):
    print('hello!', request.method, request.args, request.form)
    print('session:', session)
    if request.method == "POST":
        user = app.manager.authentication(request.form['login'], utils.hash_it(request.form['password']))
        if user:
            session['login'] = user['login']
            session['manager_fio'] = user['manager_fio']
            return redirect('/customers')
        else:
            context = {
                'managers': app.manager.get_managers(),
                'error_message': 'Ой! Был введен неверный логин или пароль',
            }
            return render_template('/login.html', **context)
    else:
        if session:
            return redirect('/customers')
        else:
            context = {
                'managers': app.manager.get_managers()
            }
            return render_template('login.html', **context)


def logout():
    if session:
        session.clear()
    return redirect('/login')


def customers(app: Application):
    print('session:', session)
    if session:
        cur_customers = app.manager.get_customers(manager_fio=session['manager_fio'])
        context = {
            'customers': cur_customers,
            'status_constants': app.manager.status_constants
        }
        return render_template('customers.html', **context)
    else:
        return redirect('/login')


def update_status(app: Application):
    print('request data:', request.args)
    params = dict(request.args)
    result = app.manager.update_status(params['id'], params['status'])
    if result['ok']:
        params.update(result)
        return params
    else:
        params.update({'error': '500', 'back_status': app.manager.status_constants_rus[params['back_status']]})
        return params


def demo_error_page():
    raise Exception


import views
from main import Application


def setup_routes(app: Application):
    """ Привязка маршрутов к представлениям """
    views.setup_error_handlers(app=app)
    #
    app.add_url_rule('/', view_func=views.index)
    app.add_url_rule('/reset', view_func=views.reset, defaults={'app': app})
    app.add_url_rule('/login', view_func=views.login, methods=['GET', 'POST'], defaults={'app': app})
    app.add_url_rule('/logout', view_func=views.logout)
    app.add_url_rule('/customers', view_func=views.customers, defaults={'app': app})
    app.add_url_rule('/api/update_status', view_func=views.update_status, methods=['GET'], defaults={'app': app})
    app.add_url_rule('/demo_error', view_func=views.demo_error_page)
    #
    return app

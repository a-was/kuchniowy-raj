from flask import Flask

from .config import Config

__all__ = ['create_app']


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    init_regex_converter(app)
    init_main_routes(app)
    init_extensions(app)
    init_blueprints(app)

    return app


def init_blueprints(application):
    from app.routes import app as main
    for blueprint in [main, ]:
        application.register_blueprint(blueprint)


def init_extensions(application):
    from . import db
    db.init_app(application)


def init_main_routes(application):
    import time
    import traceback

    from flask import g, request

    from .extensions import log

    def get_ip(req):
        ip = req.headers.getlist('X-Forwarded-For')
        return ip[0].split(',')[0] if ip else req.remote_addr

    @application.before_request
    def before_request():
        g.start = time.time()

    @application.after_request
    def after_request(response):
        time_diff = time.time() - g.start
        log.info('request, {ip:>39}, {code}, {time:2.3f}s, {path}'.format(
                ip=get_ip(request), code=response.status, time=time_diff, path=request.full_path
        ))
        return response

    @application.errorhandler(500)
    def internal_error(error):
        time_diff = time.time() - g.start
        log.error('{ip}, {time:2.3f}s, {code}, {path}, {formatted_error}'.format(
                ip=get_ip(request), time=time_diff, code=error.get_response().status, path=request.full_path,
                formatted_error=' | '.join(traceback.format_exc().split('\n'))
        ))
        return error


def init_regex_converter(application):
    from werkzeug.routing import BaseConverter

    class RegexConverter(BaseConverter):
        def __init__(self, url_map, *items):
            super(RegexConverter, self).__init__(url_map)
            self.regex = items[0]

    application.url_map.converters['regex'] = RegexConverter

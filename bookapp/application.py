from flask import Flask
from .boilerplate import Response
from .views import v
from sqlbag.flask import FS, session_setup


class FlaskApp(Flask):
    response_class = Response


def get_app(db):
    app = FlaskApp('bookapp')
    app.config['DB'] = db
    app.s = FS(db, echo=False)
    session_setup(app)
    app.register_blueprint(v)
    return app

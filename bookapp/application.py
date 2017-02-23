

from sqlbag.flask import FS, session_setup


from flask import Flask
from .boilerplate import Response


class FlaskApp(Flask):
    response_class = Response


app = FlaskApp('bookapp')
from . import views # noqa


def get_app(db):
    app.config['DB'] = db
    app.s = FS(db, echo=False)
    session_setup(app)
    return app

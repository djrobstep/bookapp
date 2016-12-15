from flask import jsonify, Blueprint
from flask import current_app as app

from .boilerplate import selectables


v = Blueprint('v', __name__)


@v.route('/')
def home():
    selectable_names = sorted(selectables(app.s))

    if selectable_names:
        links = ['<a href="/{}">{}</a>'.format(n, n) for n in selectable_names]
        contents = '<br>'.join(links)
    else:
        contents = 'No tables yet'
    return '<h1 style="font-family: sans-serif;">{}</h1>'.format(contents)


@v.route('/<string:thing>')
def things(thing):
    selectable_names = set(selectables(app.s))
    if thing in selectable_names:
        query = 'select * from {}'.format(thing)
        results = app.s.execute(query)
        return jsonify([dict(x) for x in results])
    else:
        return 'Not found', 404

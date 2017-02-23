from flask import jsonify

from .boilerplate import selectables
from .application import app
from sqlbag.flask import proxies

s = proxies.s


@app.route('/')
def home():
    selectable_names = sorted(selectables(s))

    if selectable_names:
        links = ['<a href="/{}">{}</a>'.format(n, n) for n in selectable_names]
        contents = '<br>'.join(links)
    else:
        contents = 'No tables yet'
    return '<h1 style="font-family: sans-serif;">{}</h1>'.format(contents)


@app.route('/<string:thing>')
def things(thing):
    selectable_names = set(selectables(s))
    if thing in selectable_names:
        query = 'select * from {}'.format(thing)
        results = s.execute(query)
        return jsonify([dict(x) for x in results])
    else:
        return 'Not found', 404

from flask import render_template, redirect
from flask_babel import _
from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title=_('Home'))


@bp.route('/favicon.ico')
def favicon():
    return redirect('https://s.gravatar.com/avatar/f9eca48d6c9afa6dbeeefc3484b4985d?s=80')
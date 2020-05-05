from flask import render_template, redirect, jsonify
from flask_babel import _
from app.main import bp
from app.models import CarSpend, CarSpendType


@bp.route('/')
@bp.route('/index')
def index():
    data = CarSpend.get_fuel_prices()
    return render_template('index.html', title=_('Home'), data=data)


@bp.route('/favicon.ico')
def favicon():
    return redirect('https://s.gravatar.com/avatar/f9eca48d6c9afa6dbeeefc3484b4985d?s=80')
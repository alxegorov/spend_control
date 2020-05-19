from flask import render_template, redirect, request, g
from flask_babel import _, get_locale
from app.main import bp
from app.models import CarSpend, CarSpendType


@bp.before_app_request
def before_request():
    g.locale = str(get_locale())


@bp.route('/')
@bp.route('/index')
def index():
    f_fuel_type = request.args.get('ftype', type=int)
    data = CarSpend.get_fuel_prices(f_fuel_type)

    fuel_type_id = CarSpendType.get_fuel_types()
    fuel_type = []
    for t in fuel_type_id:
        fuel_type.append({
            'id': t,
            'title': CarSpendType.query.get(t).type
        })

    return render_template('index.html', title=_('Home'), data=data, fuel_type=fuel_type)


@bp.route('/favicon.ico')
def favicon():
    return redirect('https://s.gravatar.com/avatar/f9eca48d6c9afa6dbeeefc3484b4985d?s=80')
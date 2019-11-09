from flask import render_template, redirect, url_for, flash, request, current_app
from flask_babel import _
from flask_login import login_required
from app import db
from app.spends import bp
from app.spends.forms import AddNewCarForm
from app.models import CarModel


@bp.route('/')
def index():
    return render_template('start.html')


@bp.route('/addcar', methods=['GET', 'POST'])
def addcar():
    page = request.args.get('page', 1, type=int)
    cars = CarModel.query.order_by(CarModel.manufacturer.asc(),
                                   CarModel.model.asc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('spends.addcar', page=cars.next_num) if cars.has_next else None
    prev_url = url_for('spends.addcar', page=cars.prev_num) if cars.has_prev else None
    return render_template('addcar.html', cars=cars.items, next_url=next_url, prev_url=prev_url)


@bp.route('/addnewcar', methods=['GET', 'POST'])
@login_required
def addnewcar():
    form = AddNewCarForm()
    if form.validate_on_submit():
        car = CarModel(manufacturer=form.manufacturer.data, model=form.model.data, fuel_type=form.fueltype.data,
                       engine_volume=form.enginevolume.data, engine_power=form.enginepower.data)
        db.session.add(car)
        db.session.commit()
        flash(_('New car added'))
        return redirect(url_for('main.index'))
    return render_template('addnewcar.html', form=form)

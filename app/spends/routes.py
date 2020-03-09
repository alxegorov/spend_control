from flask import render_template, redirect, url_for, flash, request, current_app
from flask_babel import _
from flask_login import login_required, current_user
from app import db
from app.spends import bp
from app.spends.forms import AddNewCarForm, AddCarSpendForm, AddCarSpendTypeForm
from app.models import Car, CarModel, CarSpend, CarSpendType


@bp.route('/')
def index():
    return render_template('start.html', title=_('Spends'))


@bp.route('/moving')
def moving():
    return render_template('moving.html', title=_('Moving'))


@bp.route('/car')
@login_required
def car():
    page = request.args.get('page', 1, type=int)
    cars = Car.query.filter(Car.user_id == current_user.id).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('spends.addcar', page=cars.next_num) if cars.has_next else None
    prev_url = url_for('spends.addcar', page=cars.prev_num) if cars.has_prev else None
    return render_template('car.html', cars=cars.items, next_url=next_url, prev_url=prev_url, title=_('Cars'))


@bp.route('/addcar', methods=['GET', 'POST'])
def addcar():
    page = request.args.get('page', 1, type=int)
    cars = CarModel.query.order_by(CarModel.manufacturer.asc(),
                                   CarModel.model.asc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('spends.addcar', page=cars.next_num) if cars.has_next else None
    prev_url = url_for('spends.addcar', page=cars.prev_num) if cars.has_prev else None
    return render_template('addcar.html', cars=cars.items, next_url=next_url, prev_url=prev_url, title=_('Add Car'))


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
        return redirect(url_for('spends.addcar'))
    return render_template('addnewcar.html', form=form, title=_('Add New Car'))


@bp.route('/addcar/add')
@login_required
def addingcar():
    user_id = request.args.get('user_id', type=int)
    car_model_id = request.args.get('car_model_id', type=int)
    car = Car(car_model_id=car_model_id, user_id=user_id)
    db.session.add(car)
    db.session.commit()
    flash(_('Car was added'))
    return redirect(url_for('spends.car'))


@bp.route('/car/addspend/<car_id>', methods=['GET', 'POST'])
@login_required
def addcarspend(car_id):
    form = AddCarSpendForm()
    form.spend_type.choices = [(t.id, t.type) for t in CarSpendType.query.all()]
    if form.validate_on_submit():
        spend = CarSpend(timestamp=form.timestamp.data, trip=form.trip.data, price=form.price.data,
                         amount=form.amount.data, car_id=car_id, car_spend_type_id=form.spend_type.data)
        db.session.add(spend)
        db.session.commit()
        flash(_('Spend added'))
        return redirect(url_for('spends.car'))
    page = request.args.get('page', 1, type=int)
    spends = CarSpend.query.filter(CarSpend.car_id == car_id).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('spends.addcarspend[car_id]', page=spends.next_num) if spends.has_next else None
    prev_url = url_for('spends.addcarspend[car_id]', page=spends.prev_num) if spends.has_prev else None
    return render_template('addcarspend.html', form=form, spends=spends.items, next_url=next_url, prev_url=prev_url,
                           title=_('Add Car Spend'))


@bp.route('/car/dellspend/<id>')
@login_required
def dellcarspend(id):
    spend = CarSpend.query.get(id)
    db.session.delete(spend)
    db.session.commit()
    return redirect(url_for('spends.car'))


@bp.route('car/addspendtype', methods=['GET', 'POST'])
@login_required
def addcarspendtype():
    form = AddCarSpendTypeForm()
    if form.validate_on_submit():
        type = CarSpendType(type=form.type.data)
        db.session.add(type)
        db.session.commit()
        flash(_('New type car spend was added'))
        return redirect(url_for('spends.car'))
    return render_template('addcarspendtype.html', form=form, title=_('Add Car Spend Type'))

from flask import render_template, redirect, url_for, flash, request, current_app, g
from flask_babel import _
from flask_login import login_required, current_user
from app import db
from app.spends import bp
from app.spends.forms import AddNewCarForm, AddCarSpendForm, AddCarSpendTypeForm, AddCarForm
from app.models import Car, CarModel, CarSpend, CarSpendType


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index(): 
    add_spend_form = AddCarSpendForm()
    add_spend_form.car.choices = [(c.id, c.model.manufacturer + ' ' + c.model.model) for c in Car.query.filter(Car.user_id == current_user.id)]
    add_spend_form.spend_type.choices = [(t.id, t.type) for t in CarSpendType.query.all()]
    if add_spend_form.validate_on_submit():
        spend = CarSpend(timestamp=add_spend_form.timestamp.data, trip=add_spend_form.trip.data, 
                         price=add_spend_form.price.data, amount=add_spend_form.amount.data, 
                         car_id=add_spend_form.car.data, car_spend_type_id=add_spend_form.spend_type.data)
        db.session.add(spend)
        db.session.commit()
        flash(_('Spend added'))
        return redirect(url_for('spends.index'))

    add_spend_type_form = AddCarSpendTypeForm()
    if add_spend_type_form.validate_on_submit():
        type = CarSpendType(type=add_spend_type_form.type.data)
        db.session.add(type)
        db.session.commit()
        flash(_('New type car spend was added'))
        return redirect(url_for('spends.index'))

    add_new_car_form = AddNewCarForm()
    if add_new_car_form.validate_on_submit():
        car = CarModel(manufacturer=add_new_car_form.manufacturer.data, model=add_new_car_form.model.data, 
                       fuel_type=add_new_car_form.fueltype.data, engine_volume=add_new_car_form.enginevolume.data, 
                       engine_power=add_new_car_form.enginepower.data)
        db.session.add(car)
        db.session.commit()
        flash(_('New model added'))
        return redirect(url_for('spends.index'))

    add_car_form = AddCarForm()
    add_car_form.car.choices = [(m.id, m.manufacturer + ' ' + m.model + ', ' + str(m.engine_volume)) for m in CarModel.query.all()]
    if add_car_form.validate_on_submit():
        car = Car(car_model_id=add_car_form.car.data, user_id=current_user.id)
        db.session.add(car)
        db.session.commit()
        flash(_('New car added'))
        return redirect(url_for('spends.index'))


    cars = Car.query.filter(Car.user_id == current_user.id).all()
    car_id = [c.id for c in cars]
    page = request.args.get('page', 1, type=int)
    spends = CarSpend.query.filter(CarSpend.car_id.in_(car_id)).order_by(CarSpend.timestamp.desc()).paginate(page, 
        current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('spends.index', car_id=car_id, page=spends.next_num) if spends.has_next else None
    prev_url = url_for('spends.index', car_id=car_id, page=spends.prev_num) if spends.has_prev else None
    return render_template('spends.html', title=_('Spends'), spends=spends.items, next_url=next_url, 
        prev_url=prev_url, add_spend_form=add_spend_form, add_spend_type_form=add_spend_type_form, cars=cars,
        add_new_car_form=add_new_car_form, add_car_form=add_car_form)

@bp.route('/addcar', methods=['GET', 'POST'])
def addcar():
    page = request.args.get('page', 1, type=int)
    cars = CarModel.query.order_by(CarModel.manufacturer.asc(),
                                   CarModel.model.asc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('spends.addcar', page=cars.next_num) if cars.has_next else None
    prev_url = url_for('spends.addcar', page=cars.prev_num) if cars.has_prev else None
    return render_template('addcar.html', cars=cars.items, next_url=next_url, prev_url=prev_url, title=_('Add Car'))

@bp.route('/dellcar/<id>', methods=['GET', 'POST'])
@login_required
def dellcar(id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('spends.car'))


@bp.route('/car/dellspend/<id>')
@login_required
def dellcarspend(id):
    spend = CarSpend.query.get(id)
    db.session.delete(spend)
    db.session.commit()
    return redirect(url_for('spends.car'))
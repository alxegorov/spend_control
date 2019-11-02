from flask import render_template, redirect, url_for, flash
from flask_babel import _
from flask_login import login_required
from app import db
from app.spends import bp
from app.spends.forms import AddCarForm, AddNewCarForm
from app.models import CarModel


@bp.route('/addcar', methods=['GET', 'POST'])
def addcar():
    form = AddCarForm()
    return render_template('addcar.html', form=form)


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

from flask import render_template
from flask_login import login_required
from app.spends import bp
from app.spends.forms import AddCarForm, AddNewCarForm


@bp.route('/addcar', methods=['GET', 'POST'])
def addcar():
    form = AddCarForm()
    return render_template('addcar.html', form=form)


@bp.route('/addnewcar', methods=['GET', 'POST'])
@login_required
def addnewcar():
    form = AddNewCarForm()
    return render_template('addnewcar.html', form=form)

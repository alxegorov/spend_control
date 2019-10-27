from flask import render_template
from app.spends import bp
from app.spends.forms import AddCarForm


@bp.route('/addcar', methods=['GET', 'POST'])
def addcar():
    form = AddCarForm()
    return render_template('addcar.html', form=form)

from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import SelectField, StringField, SubmitField, IntegerField, FloatField, DateTimeField
from wtforms.validators import InputRequired, DataRequired


class AddNewCarForm(FlaskForm):
    manufacturer = StringField(_l('Manufacturer'), validators=[DataRequired()])
    model = StringField(_l('Model'), validators=[DataRequired()])
    fueltype = SelectField(_l('Fuel type'),
                           choices=[('gasoline', _l('gasoline')), ('diesel', _l('diesel')), ('gas', _l('gas')),
                                    ('electricity', _l('electricity'))],
                           validators=[InputRequired()])
    enginevolume = StringField(_l('Engine volume (сс)'), validators=[DataRequired()])
    enginepower = StringField(_l('Engine power'), validators=[DataRequired()])
    submit = SubmitField(_l('Add'))


class AddCarSpendForm(FlaskForm):
    timestamp = DateTimeField(_l('Date'))
    trip = IntegerField(_l('Trip'), validators=[DataRequired()])
    spend_type = SelectField(_l('Spend type'), coerce=int)
    price = FloatField(_l('Price'), validators=[DataRequired()])
    amount = IntegerField(_l('Amount'), validators=[DataRequired()])
    submit = SubmitField(_l('Add'))


class AddCarSpendTypeForm(FlaskForm):
    type = StringField(_l('Spend type'), validators=[DataRequired()])
    submit = SubmitField(_l('Add'))

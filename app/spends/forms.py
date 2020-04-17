from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import SelectField, StringField, SubmitField, IntegerField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, DataRequired, NumberRange


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


class AddCarTripForm(FlaskForm):
    trip = IntegerField(_l('Trip'), validators=[DataRequired(), NumberRange()])
    submit = SubmitField(_l('Add'))

class AddCarSpendForm(FlaskForm):
    timestamp = DateField(_l('Date'))
    trip = IntegerField(_l('Trip'), validators=[DataRequired(), NumberRange()])
    spend_type = SelectField(_l('Spend type'), coerce=int)
    price = FloatField(_l('Price'))
    amount = FloatField(_l('Amount'), validators=[DataRequired()])
    submit = SubmitField(_l('Add'))


class AddCarSpendTypeForm(FlaskForm):
    type = StringField(_l('Spend type'), validators=[DataRequired()])
    submit = SubmitField(_l('Add'))

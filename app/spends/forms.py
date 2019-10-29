from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, DataRequired


class AddCarForm(FlaskForm):
    manufacturer = SelectField(_l('Manufacturer'), coerce=int, validators=[InputRequired])
    model = SelectField(_l('Manufacturer'), coerce=int, validators=[InputRequired])
    fueltype = SelectField(_l('Fuel type'), coerce=int, validators=[InputRequired])
    enginevolume = SelectField(_l('Engine volume'), coerce=int, validators=[InputRequired])
    enginepower = SelectField(_l('Engine power'), coerce=int, validators=[InputRequired])


class AddNewCarForm(FlaskForm):
    manufacturer = StringField(_l('Manufacturer'), validators=[DataRequired])
    model = StringField(_l('Model'), validators=[DataRequired])
    fueltype = StringField(_l('Fuel type'), validators=[DataRequired])
    enginevolume = StringField(_l('Engine volume'), validators=[DataRequired])
    enginepower = StringField(_l('Engine power'), validators=[DataRequired])
    submit = SubmitField(_l('Add'))
    cancel = SubmitField(_l('Cancel'))

from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import SelectField
from wtforms.validators import InputRequired


class AddCarForm(FlaskForm):
    manufacturer = SelectField(_l('Manufacturer'), coerce=int, validators=[InputRequired])
    model = SelectField(_l('Manufacturer'), coerce=int, validators=[InputRequired])
    fueltype = SelectField(_l('Fuel type'), coerce=int, validators=[InputRequired])
    enginevolume = SelectField(_l('Engine volume'), coerce=int, validators=[InputRequired])
    enginepower = SelectField(_l('Engine power'), coerce=int, validators=[InputRequired])

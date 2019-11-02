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
    manufacturer = StringField(_l('Manufacturer'), validators=[DataRequired()])
    model = StringField(_l('Model'), validators=[DataRequired()])
    fueltype = SelectField(_l('Fuel type'),
                           choices=[('gasoline', _l('gasoline')), ('diesel', _l('diesel')), ('gas', _l('gas')),
                                    ('electricity', _l('electricity'))],
                           validators=[InputRequired()])
    enginevolume = StringField(_l('Engine volume (сс)'), validators=[DataRequired()])
    enginepower = StringField(_l('Engine power'), validators=[DataRequired()])
    submit = SubmitField(_l('Add'))

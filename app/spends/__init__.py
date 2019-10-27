from flask import Blueprint

bp = Blueprint('spends', __name__, template_folder='templates')

from app.spends import routes
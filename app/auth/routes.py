from flask import render_template
from app.auth import bp


@bp.route('/login')
def login():
    return render_template('login.html')

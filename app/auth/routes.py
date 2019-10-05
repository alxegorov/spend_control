from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from app import db
from app.auth import bp
from app.models import User
from app.auth.forms import RegistrationForm


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

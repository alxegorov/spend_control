from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm
from app.email import send_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        if user.active is False:
            flash('Your account not active. Please, confirm your email.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash('{}, welcome to Spend Control!'.format(user.username))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@bp.route('/logout')
def logout():
    flash('Goodbye, {}!'.format(current_user.username))
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Add user to database
        user = User(username=form.username.data, email=form.email.data, active=False)
        user.set_password(form.password.data)
        token = user.get_activate_token()
        db.session.add(user)
        db.session.commit()

        # Send activate email
        token = user.get_activate_token()
        send_email(subject='[Spend_control] User activation',
                   sender=current_app.config['ADMINS'][0],
                   recipients=[user.email],
                   text_body=render_template('email/register_apply.txt', user=user, token=token),
                   html_body=render_template('email/register_apply.html', user=user, token=token))
        flash('Please, check email to activate your account.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@bp.route('/activate/<token>')
def activate(token):
    user = User.activate_user(token)
    db.session.commit()
    if not user:
        flash('Activation error')
        return redirect(url_for('main.index'))
    flash('Your account is activated. Please, sign in.')
    return redirect(url_for('auth.login'))

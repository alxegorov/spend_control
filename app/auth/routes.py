from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.email import send_user_activate_email, send_password_reset_email
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        if user.active is False:
            flash(_('Your account not active. Please, confirm your email.'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash(_('%(username)s, welcome to Spend Control!', username=user.username))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', form=form, title=_('Sign In'))


@bp.route('/logout')
def logout():
    flash(_('Goodbye, %(username)s!', username=current_user.username))
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, active=False)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            send_user_activate_email(user)
            flash(_('Please, check email to activate your account.'))
        except:
            db.session.rollback()
            flash('Registration error. Please try again later')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, title=_('Sign Up'))


@bp.route('/activate/<token>')
def activate(token):
    user = User.activate_user(token)
    db.session.commit()
    if not user:
        flash(_('Activation error'))
        return redirect(url_for('main.index'))
    flash(_('Your account is activated. Please, sign in.'))
    return redirect(url_for('auth.login'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password.'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form, title=_('Reset password'))


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash(_('Reset password error.'))
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form, title=_('Reset password'))

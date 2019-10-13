from flask import render_template, current_app
from app.email import send_email


def send_user_activate_email(user):
    token = user.get_activate_token()
    send_email(subject='[Spend_control] User activation',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/register_apply.txt', user=user, token=token),
               html_body=render_template('email/register_apply.html', user=user, token=token))


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(subject='[Spend_control] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db
from app.email import send_email
from app.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are now a registered user')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/test_email', methods=['POST', 'GET'])
@login_required
def test_email():
    if request.method == "POST":
        send_email('Flask boilerplate test email',
                   sender=app.config['ADMINS'][0], recipients=[request.form['recipient']], text_body=render_template('email/test_email.txt', user=current_user), html_body=render_template('email/test_email.html', user=current_user))
    return render_template('send_email.html')

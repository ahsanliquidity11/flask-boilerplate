from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.username.data))
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)

# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = user.posts.all()
    calls = [
    {
        'number':'+7 969 234 09 09',
        'site':'apple-mobile',
    },
    {
        'number':'+7 969 234 09 01',
        'site':'dobro-phone',
    }]
    return render_template("index.html",
    title = 'Dashboard',
    user = user,
    posts = posts,
    calls = calls)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    print g.user.is_authenticated
    if g.user is not None and g.user.is_authenticated:
        flash('Is Authenticated User')
        return redirect(url_for('index'))
    else:
        flash('Is None Authenticated User')
    form = LoginForm()

    if form.validate_on_submit():

        flash('Login requested for OpenID="' 
            + form.openid.data 
            + '", remember_me=' 
            + str(form.remember_me.data))
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
        # return redirect('/index')

    return render_template(
        'login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    flash('after_login')
    print 'after_login'
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        print 'add user to db'
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    
    print user
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
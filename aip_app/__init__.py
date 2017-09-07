from flask import Flask, render_template,  flash, redirect, session, send_from_directory, request
from flask.ext.bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
# Create the app with the root as the path from where static files are served
app = Flask(__name__, static_url_path='')
bcrypt = Bcrypt(app)
import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'birds.db')
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'd675d572-58e9-4667-b988-4ab1de50a24c'
db = SQLAlchemy(app)

########################################
# TODO - things left to do
#
# Localization


########################################
# Views
#
@app.route('/api/pagecount')
def page_count():
    if(session['target'] != ""):
        pageCount = Bird.query.order_by(Bird.english_name).filter(Bird.english_name.like("%" + session['target'] + "%")).count()
    else:        
        pageCount = Bird.query.count()
    return json.dumps({"pagecount": int(pageCount / 10)})

@app.route('/api/bird')
def bird():
    bird = Bird.query.filter_by(id=request.args.get('id')).first()
    wb = WrappedBird(bird.id, bird.category, bird.english_name, bird.scientific_name, bird.flight_range, bird.bio_order, bird.family).__dict__
    return json.dumps(wb)

@app.route('/api/birds')
def birds():
    pg =  int(request.args.get('pg')) if 'pg' in request.args else 0
    if(session['target'] != ""):
        print("Target: " + session['target'])
        birds = Bird.query.order_by(Bird.english_name).filter(Bird.english_name.like("%" + session['target'] + "%")).limit(10).offset(pg * 10)
    else:
        print("Empty Target")
        birds = Bird.query.order_by(Bird.english_name).limit(10).offset(pg * 10)
    birds = map(lambda bird : WrappedBird(bird.id, bird.category, bird.english_name, bird.scientific_name, bird.flight_range, bird.bio_order, bird.family).__dict__, birds)
    return json.dumps(birds)

@app.route('/api/gettarget')
def get_target():
    if(session['target']):
        return json.dumps(session['target'])
    return json.dumps("{}")

@app.route('/api/searchbirds')
def search_birds():
    session['target'] =  request.args.get('target')
    birds = Bird.query.order_by(Bird.english_name).filter(Bird.english_name.like("%" + session['target'] + "%")).limit(10)
    birds = map(lambda bird : WrappedBird(bird.id, bird.category, bird.english_name, bird.scientific_name, bird.flight_range, bird.bio_order, bird.family).__dict__, birds)
    return json.dumps(birds)

@app.route('/api/addbird', methods=['POST'])
def add_bird():
    bird = request.json
    birdy = Bird(bird['category'], bird['english_name'], bird['scientific_name'], bird['flight_range'], bird['bio_order'], bird['family'])
    db.session.add(birdy)
    db.session.commit()
    return json.dumps({"status": "OK"})

@app.route('/api/deletebird', methods=['DELETE'])
def delete_bird():
    bird = Bird.query.filter_by(id=request.args.get('id')).first()
    db.session.delete(bird)
    db.session.commit()
    return json.dumps({"status": "OK"})

@app.route('/api/updatebird', methods=['POST'])
def update_bird():
    in_bird = request.json
    bird = db.session.query(Bird).get(in_bird['id'])
    bird.category = in_bird['category']
    bird.english_name = in_bird['english_name']
    bird.scientific_name = in_bird['scientific_name']
    bird.flight_range = in_bird['flight_range']
    bird.bio_order = in_bird['bio_order']
    bird.family = in_bird['family']
    db.session.commit()
    return json.dumps({"status": "OK"})

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/ng_templates/<path:path>')
def send_ng_templates(path):
    return send_from_directory('ng_templates', path)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', **session)

@app.route('/init')
def init():
    msg = init_db()
    return render_template('init.html', msg=msg)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('index.html', **session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    session['target'] = ""
    login_msg = ''
    form = LoginForm()
    if form.validate_on_submit():
        dbg_flash('Login requested for user_name="%s", remember_me=%s' % (form.user_name.data, str(form.remember_me.data)))
        user = User.query.filter_by(username=form.user_name.data).first()
        if(user):
            pwd_match = bcrypt.check_password_hash(user.password, form.password.data)
            print(pwd_match)
        else:
            pwd_match = False
        if(pwd_match):
            session['logged_in'] = True
            session['user_nickname'] = user.nickname
            return redirect('/index')
        else:
            login_msg = 'User name or password is incorrect'
    return render_template('login.html', login_msg=login_msg, form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        dbg_flash('Sign-up requested for user_name="%s"' % (form.user_name.data))
        user = User(form.user_name.data, bcrypt.generate_password_hash(form.password.data), form.user_nickname.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('signup.html', title='Sign up', form=form)

debug_flash = False
def dbg_flash(msg):
    if debug_flash:
        flash(msg)
    return
########################################
# Forms
#
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(Form):
    user_name = StringField('user_name', validators=[DataRequired(message="User Name is required.")])
    password = PasswordField('password', validators=[DataRequired(message="Password is required.")])
    remember_me = BooleanField('remember_me', default=False)

class SignUpForm(Form):
    user_name = StringField('user_name', validators=[DataRequired(message="User Name is required.")])
    password =  PasswordField('password', validators=[DataRequired(message="Password is required."), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    user_nickname = StringField('user_nickname', validators=[DataRequired(message="Aw c'mon. Give us your nickname." )])

########################################
# Models
#
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=False)
    nickname = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(120), unique=False)

    def __init__(self, username, password, nickname, email=''):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Bird(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120), unique=False)
    english_name	 = db.Column(db.String(120), unique=False)
    scientific_name	 = db.Column(db.String(120), unique=False)
    flight_range = db.Column(db.String(120), unique=False)
    bio_order = db.Column(db.String(120), unique=False)
    family = db.Column(db.String(120), unique=False)
    def __init__(self, category, english_name, scientific_name, flight_range, bio_order, family):
        self.category = category
        self.english_name = english_name
        self.scientific_name = scientific_name
        self.flight_range = flight_range
        self.bio_order = bio_order
        self.family = family

class WrappedBird:
    def __init__(self, id, category, english_name, scientific_name, flight_range, bio_order, family):
        self.id = id
        self.category = category
        self.english_name = english_name
        self.scientific_name = scientific_name
        self.flight_range = flight_range
        self.bio_order = bio_order
        self.family = family

########################################
# Database
#
def init_db():
    db.drop_all()
    db.session.commit()
    db.create_all()
    user = User('admin', bcrypt.generate_password_hash('password'), 'Administrator')
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username='admin').first()
    if(user):
        msg = 'Database initialized'
    else:
        msg = 'Error initializing database'
    return msg

########################################
# Unit Tests - "Anything that is untested is broken.""
#
import tempfile
import unittest

class BirdTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        init_db()

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'Pythonic' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            user_name=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def signup(self):
        rv = self.logout()
        return self.app.get('/signup')

    def test_login_logout(self):
        rv = self.login('admin', 'password')
        assert b'Hi' in rv.data
        rv = self.logout()
        assert b'Login' in rv.data
        assert b'Sign up' in rv.data
        assert b'Welcome to the' in rv.data
        rv = self.login('adminx', 'default')
        assert b'Password:' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'Password:' in rv.data

    def test_sign_up(self):
        rv = self.signup()
        assert b'Nick name:' in rv.data
        rv = self.app.post('/signup', data=dict(
            user_name='testuser',
            password='testuserpwd',
            confirm='testuserpwdnotconfirmed',
            user_nickname='testusernickname'
        ), follow_redirects=True)
        assert b'Passwords must match' in rv.data
        rv = self.signup()
        assert b'Nick name:' in rv.data
        rv = self.app.post('/signup', data=dict(
            user_name='testuser',
            password='testuserpwd',
            confirm='testuserpwd',
            user_nickname=''
        ), follow_redirects=True)
        assert b'Give us your nickname' in rv.data
        rv = self.signup()
        assert b'Nick name:' in rv.data
        rv = self.app.post('/signup', data=dict(
            user_name='testuser',
            password='testuserpwd',
            confirm='testuserpwd',
            user_nickname='testusernickname'
        ), follow_redirects=True)
        assert b"Log In" in rv.data

if __name__ == '__main__':
    unittest.main()

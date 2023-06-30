"""Blogly application."""

from flask import Flask,render_template,request,redirect
from models import db, connect_db,User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:graygirl@localhost:5433/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'f724'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.debug = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    '''Homepage defaults to list of users'''
    return redirect('/users')

@app.route('/users')
def users():
    '''Page of list of users'''
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/user_page.html',users = users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    '''Show form for adding new user'''
    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    '''Handle form submission to add new user'''
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''Show individual user page'''
    user = User.query.get_or_404(user_id)
    print(user)
    return render_template('users/show.html',user = user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''Show form for editing specific user'''
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html',user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def update_user(user_id):
    '''Handle form submission of edit info for user'''
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Remove user from list'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
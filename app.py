from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
import git
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c29bcfa698752666def85f68880d22d8'
proxied = FlaskBehindProxy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
  db.create_all()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/update_server", methods=['POST'])
def webhook():
    repo = git.Repo('/home/codetomato/flask-hosting-template/')
    repo.remotes.origin.pull()
    return 'Updated PythonAnywhere successfully', 200

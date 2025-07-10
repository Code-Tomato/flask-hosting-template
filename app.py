from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
import git
from flask_behind_proxy import FlaskBehindProxy
proxied = FlaskBehindProxy(app)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c29bcfa698752666def85f68880d22d8'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/update_server", methods=['POST'])
def webhook():
    repo = git.Repo('/home/codetomato/flask-hosting-template/')
    repo.remotes.origin.pull()
    return 'Updated PythonAnywhere successfully', 200
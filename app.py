from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecoactions.db'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer, default=0)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False)

# Routes
@app.route('/')
def home():
    if 'user' in session:
        user = User.query.filter_by(username=session['user']).first()
        challenges = Challenge.query.all()
        return render_template('index.html', user=user, challenges=challenges)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return 'User already exists!'
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = username
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/complete_challenge/<int:challenge_id>')
def complete_challenge(challenge_id):
    if 'user' in session:
        user = User.query.filter_by(username=session['user']).first()
        challenge = Challenge.query.get(challenge_id)
        user.points += challenge.points
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html', users=users)

if _name_ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
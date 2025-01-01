import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from config import Config
import pyodbc

# Opret forbindelse til databasen ved at bruge miljøvariabler
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=' + os.getenv('DB_SERVER') + ';'
        'DATABASE=' + os.getenv('DB_NAME') + ';'
        'UID=' + os.getenv('DB_USER') + ';'
        'PWD=' + os.getenv('DB_PASSWORD') + ';'
        'TrustServerCertificate=yes'
    )
    return conn

# Initialisering af Flask app
app = Flask(__name__)

# Brug miljøvariabler til at indlæse config.py
app.config.from_object(Config)

# Angiv din SECRET_KEY for at beskytte sessionen
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')  # Brug miljøvariabel eller default værdi

# Database setup
db = SQLAlchemy(app)

# Definér User model
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Navn på brugeren
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Forespørgsel for at hente hold
def get_teams():
    """Hent liste over hold baseret på årgang fra databasen."""
    try:
        query = text("SELECT DISTINCT hold FROM dbo.spillere WHERE hold IS NOT NULL AND hold != ''")
        result = db.session.execute(query).fetchall()

        teams = [{"label": hold[0], "value": hold[0]} for hold in result if hold[0]]
        return teams
    except Exception as e:
        print(f"Fejl ved hentning af hold: {e}")
        return []

# Route for login
@app.route('/')
def home():
    return redirect('/login')  # Redirect til login-siden som standard

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.clear()  # Ryd sessionen for at fjerne gamle koder eller data
            session['user_id'] = user.user_id  # Gem kun brugerens ID i sessionen
            flash("Login successful!", "success")
            return redirect('/dashboard')
        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html', username=None)  # Sæt username til None eller en tom værdi

# Route for dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You need to log in to access the dashboard.", "info")
        return redirect('/login')

    user = User.query.get(session['user_id'])
    teams = get_teams()  # Hent holdene fra databasen
    selected_team = request.args.get('team', None)  # Hent valgt hold fra URL

    return render_template('dashboard.html', user=user, teams=teams, selected_team=selected_team)

# Route for player stats page
@app.route('/player_stats')
def player_stats():
    if 'user_id' not in session:
        flash("You need to log in to access player statistics.", "info")
        return redirect('/login')

    user = User.query.get(session['user_id'])
    return render_template('view.html', user=user)

# Route for team stats page
@app.route('/team_stats')
def team_stats():
    if 'user_id' not in session:
        flash("You need to log in to access team statistics.", "info")
        return redirect('/login')

    user = User.query.get(session['user_id'])
    return render_template('hold.html', user=user)

# Route for other sections if needed
@app.route('/other_section')
def other_section():
    if 'user_id' not in session:
        flash("You need to log in to access other sections.", "info")
        return redirect('/login')

    user = User.query.get(session['user_id'])
    return render_template('andet.html', user=user)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('name', None)  # Fjern brugerens navn fra sessionen
    flash("You have been logged out.", "info")
    return redirect('/login')

# Start Flask app
if __name__ == '__main__':
    app.run(debug=False)  # Deaktiver debug-mode i produktion


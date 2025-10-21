from flask import Flask, request, render_template, redirect, url_for, session, g
from jinja2 import Template
import re
import html
import os
import requests
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(64)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row 
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        db.commit()
    

with app.app_context():
    init_db()

def decode_html_entities(text):
    return html.unescape(text)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('fetch_url_info'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        db = get_db()
        cursor = db.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?",
                            (username, hashed_password))
        user = cursor.fetchone()

        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            return redirect(url_for('fetch_url_info'))
        else:
            error = "Invalid username or password."
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('logged_in'):
        return redirect(url_for('fetch_url_info'))

    error = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            error = "Username and password are required."
        else:
            db = get_db()
            cursor = db.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            if cursor.fetchone()[0] > 0:
                error = "Username already exists. Please choose a different one."
            else:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                try:
                    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                               (username, hashed_password))
                    db.commit()
                    success = "Registration successful! You can now login."
                    return render_template('register.html', success=success)
                except sqlite3.IntegrityError:
                    error = "An error occurred during registration. Please try again."

    return render_template('register.html', error=error, success=success)

@app.route('/fetch_url_info', methods=['GET', 'POST'])
def fetch_url_info():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    current_user = session.get('username', 'Guest')

    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "URL is required", 400

        title = ""
        description = ""
        error_message = None

        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            response.raise_for_status()
            html_content = response.text

            title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = decode_html_entities(title_match.group(1).strip())

            og_description_match = re.search(r'<meta property="og:description" content="([^"]+)"', html_content, re.IGNORECASE)
            if og_description_match:
                description = decode_html_entities(og_description_match.group(1))
            else:
                meta_description_match = re.search(r'<meta name="description" content="([^"]+)"', html_content, re.IGNORECASE)
                if meta_description_match:
                    description = decode_html_entities(meta_description_match.group(1))
                else:
                    twitter_description_match = re.search(r'<meta property="twitter:description" content="([^"]+)"', html_content, re.IGNORECASE)
                    if twitter_description_match:
                        description = decode_html_entities(twitter_description_match.group(1))

        except requests.exceptions.Timeout:
            error_message = "Request to URL timed out."
        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred while fetching the URL: {str(e)}"
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"

        escaped_description = html.escape(description) # Escape HTML entities in description
        escaped_description = Template(description).render()
        escaped_url = html.escape(url)
        escaped_title = html.escape(title)

        try:
            return render_template(
                'fetch_info.html',
                url_display=escaped_url,
                title_display=escaped_title,
                description_content=escaped_description, 
                username=current_user
            )
        except Exception as e:
            error_message = f"Error rendering template: {str(e)}"
            return f"<h1>Error</h1><p>{error_message}</p>", 500

    return render_template('fetch_url_form.html', username=current_user)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5003)

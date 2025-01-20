from flask import Flask, request, render_template, g, redirect, url_for
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)
app.secret_key = 'REPLACE_ME_WITH_A_RANDOM_SECRET_KEY'  # Important for session security

def get_db():
    """
    Gets a SQLite database connection for each request.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        db.commit()
    return db

@app.teardown_appcontext
def close_connection(exception):
    """
    Closes the database connection when the request finishes.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Basic validation check for empty email
        if not email:
            return render_template('index.html', message="Please provide a valid email.")
        
        # Insert email into database
        try:
            db = get_db()
            db.execute('INSERT INTO subscribers (email) VALUES (?)', (email,))
            db.commit()
            
            return render_template('index.html', message="Thank you for subscribing!")
        
        except sqlite3.IntegrityError:
            # Email already exists in the database or other constraint violation
            return render_template('index.html', message="You've already subscribed or invalid email.")
    
    # For GET requests, just show the page with the form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

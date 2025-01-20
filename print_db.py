# list_subscribers.py

import sqlite3

DATABASE = 'database.db'  # Path to your SQLite database

def list_emails():
    """
    Connects to the local SQLite database, fetches all email records,
    and prints them line by line.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Assuming your table is named 'subscribers' and the email column is 'email'
    cursor.execute("SELECT email FROM subscribers")
    
    rows = cursor.fetchall()
    
    if rows:
        print("Subscribers' Emails:")
        for row in rows:
            email = row[0]
            print(email)
    else:
        print("No emails found in the database.")
    
    conn.close()

if __name__ == "__main__":
    list_emails()

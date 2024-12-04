from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime

# Flask app initialization
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database connection details
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'ClothingStore'
}

def db_connect():
    return mysql.connector.connect(**db_config)

# --- Route to Display Records ---
@app.route('/')
def index():
    conn = db_connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Store;")
    store_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', store_items=store_items)

# --- Route to Add New Clothing Item ---
@app.route('/add', methods=['POST'])
def add_item():
    clothing_id = request.form['clothing_id']
    price = request.form['price']
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Store (ClothingID, Price) VALUES (%s, %s)", (clothing_id, price))
        conn.commit()
        flash('Item added successfully!')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

# --- Route to Delete Clothing Item (Soft Delete) ---
@app.route('/delete/<int:clothing_id>', methods=['POST'])
def delete_item(clothing_id):
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Store WHERE ClothingID = %s", (clothing_id,))
        conn.commit()
        flash('Item deleted successfully!')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

# --- Route to Update Gold Customer Status ---
@app.route('/update_gold/<int:customer_id>', methods=['POST'])
def update_gold_customer(customer_id):
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Customer SET GoldCustomer = TRUE WHERE CustomerID = %s AND (SELECT COUNT(*) FROM CustomerTransactions WHERE CustomerID = %s) > 5", (customer_id, customer_id))
        conn.commit()
        flash('Customer updated to Gold Customer status!')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

# --- Main function to run the application ---
if __name__ == '__main__':
    app.run(debug=True)

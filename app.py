from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from db_operations import db_operations
from datetime import datetime

# Flask app initialization
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# global variable for MySQL password
db_ops = None

def db_initialize(password):
    db_ops = db_operations('localhost', 'root', password)  # Use the provided password
    db_ops.create_database()
    db_ops.create_tables()

# --- Route to Display Records ---
@app.route('/')
def index():
    store_items  = db_ops.get_store_items()
    return render_template('index.html', store_items=store_items)

# --- Route to Add New Clothing Item ---
@app.route('/add', methods=['POST'])
def add_item():
    clothing_id = request.form['clothing_id']
    price = request.form['price']
    try:
        message = db_ops.add_store_item(clothing_id, price)
        flash(message)
    except Exception as e:
        flash(f"Unexpected error: {str(e)}")
    return redirect(url_for('index'))


# --- Route to Delete Clothing Item (Soft Delete) ---
@app.route('/delete/<int:clothing_id>', methods=['POST'])
def delete_item(clothing_id):
    try:
        message = db_ops.delete_store_item(clothing_id)
        flash(message)
    except Exception as e:
        flash(f"Unexpected error: {str(e)}")
    return redirect(url_for('index'))

# --- Route to Update Gold Customer Status ---
@app.route('/update_gold/<int:customer_id>', methods=['POST'])
def update_gold_customer(customer_id):
    try:
        message = db_ops.update_gold_customer_status(customer_id)
        flash(message)
    except Exception as e:
        flash(f"Unexpected error: {str(e)}")
    return redirect(url_for('index'))


def main():
    global db_ops
    password = input("Please enter your MySQL password: ")
    try:
        db_ops = db_operations('localhost', 'root', password)
        db_ops.create_database()
        db_ops.create_tables()
        db_ops.insert_data()
        print("Starting the Flask app...")
        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# --- Main function to run the application ---
if __name__ == '__main__':
    main()

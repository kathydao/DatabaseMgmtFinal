import mysql.connector
import random
from datetime import datetime, timedelta
import csv 

class db_operations:
    # initilize and connect with sql database
    def __init__(self, host, user, password):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()
        print("connection established")
    
    def __del__(self):
        self.connection.close()
        print("Database connection closed.")


    # create rideshare database
    def create_database(self):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS ClothingStore;")
        self.connection.database = 'ClothingStore'
        print("Database created successfully.")
    
    def create_tables(self):
        # create store table
        store_table_query = '''
        CREATE TABLE IF NOT EXISTS Store(
            ClothingID INT PRIMARY KEY,
            Price INT NOT NULL
        );
        '''
        # create the customers table
        customers_table_query = '''
        CREATE TABLE IF NOT EXISTS Customer(
            CustomerID INT PRIMARY KEY,
            State VARCHAR(50) NOT NULL,
            Age INT NOT NULL,
            GoldCustomer BOOLEAN DEFAULT FALSE
        );
        '''
        # create the customer table
        customer_transactions_table_query = '''
        CREATE TABLE IF NOT EXISTS CustomerTransactions(
            CustomerTransactionID INT PRIMARY KEY,
            CustomerID INT,
            ClothingID INT,
            Amount INT NOT NULL,
            TotalCost INT NOT NULL,
            Date DATETIME NOT NULL,
            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (ClothingID) REFERENCES Store(ClothingID) ON DELETE CASCADE
        );
        '''
        #create the store transactions table
        store_transactions_table_query = '''
        CREATE TABLE IF NOT EXISTS StoreTransactions(
            StoreTransactionID INT PRIMARY KEY,
            ClothingID INT,
            Amount INT NOT NULL,
            TotalCost INT NOT NULL,
            Date DATETIME NOT NULL,
            FOREIGN KEY (ClothingID) REFERENCES Store(ClothingID) ON DELETE CASCADE
        );
        '''
        #create the warehouse table
        warehouse_table_query = '''
        CREATE TABLE IF NOT EXISTS Warehouse(
            ClothingID INT PRIMARY KEY,
            Cost INT NOT NULL,
            FOREIGN KEY (ClothingID) REFERENCES Store(ClothingID)
        );
        '''
        #create the clothes table
        clothes_table_query = '''
        CREATE TABLE IF NOT EXISTS Clothes(
            ClothingID INT PRIMARY KEY,
            Color VARCHAR(30) NOT NULL,
            Brand VARCHAR(50) NOT NULL,
            Style VARCHAR(50) NOT NULL,
            FOREIGN KEY (ClothingID) REFERENCES Store(ClothingID)
        );
        '''
        # execute queries
        self.cursor.execute(store_table_query)
        print("store table created successfully.")
        self.cursor.execute(customers_table_query)
        print("customers table created successfully.")
        self.cursor.execute(customer_transactions_table_query)
        print("customer transactions table created successfully.")
        self.cursor.execute(store_transactions_table_query)
        print("store transactions table created successfully.")
        self.cursor.execute(warehouse_table_query)
        print("warehouse table created successfully.")
        self.cursor.execute(clothes_table_query)
        print("clothes table created successfully.")


    # get store items
    def get_store_items(self):
        self.cursor.execute("SELECT * FROM Store")
        store_items = self.cursor.fetchall()
        return store_items
    
    # Add a new store item
    def add_store_item(self, clothing_id, price):
        try:
            query = "INSERT INTO Store (ClothingID, Price) VALUES (%s, %s)"
            self.cursor.execute(query, (clothing_id, price))
            self.connection.commit()
            return "Item added successfully!"
        except Exception as e:
            self.connection.rollback()
            return f"Error: {str(e)}"
    
    # Delete a store item (Soft Delete)
    def delete_store_item(self, clothing_id):
        try:
            query = "DELETE FROM Store WHERE ClothingID = %s"
            self.cursor.execute(query, (clothing_id,))
            self.connection.commit()
            return "Item deleted successfully!"
        except Exception as e:
            self.connection.rollback()
            return f"Error: {str(e)}"

    # Update Gold Customer Status
    def update_gold_customer_status(self, customer_id):
        try:
            query = """
            UPDATE Customers
            SET GoldCustomer = TRUE
            WHERE CustomerID = %s AND (
            SELECT COUNT(*) FROM CustomerTransactions WHERE CustomerID = Customers.CustomerID
            ) > 5
            """
            self.cursor.execute(query, (customer_id, customer_id))
            self.connection.commit()
            return "Customer updated to Gold Customer status!"
        except Exception as e:
            self.connection.rollback()
            return f"Error: {str(e)}"
    
    #insert data into tables
    def insert_data(self):
        try:
            # Insert data into Store table
            for i in range(1, 6):
                clothing_id = i
                price = random.randint(20, 100)
                self.cursor.execute("INSERT INTO Store (ClothingID, Price) VALUES (%s, %s)", (clothing_id, price))

            # Insert data into Customer table
            states = ['California', 'Texas', 'New York', 'Florida', 'Illinois']
            for i in range(1, 6):
                customer_id = i
                state = random.choice(states)
                age = random.randint(18, 65)
                self.cursor.execute("INSERT INTO Customer (CustomerID, State, Age) VALUES (%s, %s, %s)", (customer_id, state, age))

            # Insert data into CustomerTransactions table
            for i in range(1, 6):
                transaction_id = i
                customer_id = random.randint(1, 5)
                clothing_id = random.randint(1, 5)
                amount = random.randint(1, 3)
                total_cost = amount * random.randint(20, 100)
                transaction_date = datetime.now() - timedelta(days=random.randint(1, 365))
                self.cursor.execute("INSERT INTO CustomerTransactions (CustomerTransactionID, CustomerID, ClothingID, Amount, TotalCost, Date) VALUES (%s, %s, %s, %s, %s, %s)",
                                    (transaction_id, customer_id, clothing_id, amount, total_cost, transaction_date))

            # Insert data into StoreTransactions table
            for i in range(1, 6):
                transaction_id = i
                clothing_id = random.randint(1, 5)
                amount = random.randint(1, 3)
                total_cost = amount * random.randint(20, 100)
                transaction_date = datetime.now() - timedelta(days=random.randint(1, 365))
                self.cursor.execute("INSERT INTO StoreTransactions (StoreTransactionID, ClothingID, Amount, TotalCost, Date) VALUES (%s, %s, %s, %s, %s)",
                                    (transaction_id, clothing_id, amount, total_cost, transaction_date))

            # Insert data into Warehouse table
            for i in range(1, 6):
                clothing_id = i
                cost = random.randint(10, 50)
                self.cursor.execute("INSERT INTO Warehouse (ClothingID, Cost) VALUES (%s, %s)", (clothing_id, cost))

            # Insert data into Clothes table
            colors = ['Red', 'Blue', 'Green', 'Black', 'White']
            brands = ['Nike', 'Adidas', 'Puma', 'Reebok', 'Under Armour']
            styles = ['Casual', 'Formal', 'Sporty', 'Elegant', 'Comfortable']
            for i in range(1, 6):
                clothing_id = i
                color = random.choice(colors)
                brand = random.choice(brands)
                style = random.choice(styles)
                self.cursor.execute("INSERT INTO Clothes (ClothingID, Color, Brand, Style) VALUES (%s, %s, %s, %s)", (clothing_id, color, brand, style))

            self.connection.commit()
            print("Sample data inserted successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error while inserting sample data: {str(e)}")
from db_operations import db_operations

# Global variable for database operations
# Assuming the database file is called 'clothing_store.db'
db_ops = db_operations('clothing_store.db')

def start_app():
    print("Welcome to the Clothing Store Management System!")
    main_menu()

def main_menu():
    while True:
        user_choice = input('''
        SELECT FROM THE FOLLOWING MENU:
        1. Show all clothing items
        2. Add a new clothing item
        3. Delete a clothing item
        4. Update clothing item details
        5. Find customers by state
        6. Mark customer as Gold Customer
        7. Show all Gold Customers
        8. Exit
        Choice: ''')

        if user_choice == '1':
            db_ops.show_clothing_items()
        elif user_choice == '2':
            add_clothing_item()
        elif user_choice == '3':
            delete_clothing_item()
        elif user_choice == '4':
            update_clothing_item()
        elif user_choice == '5':
            state = input("Enter the state to search customers: ")
            db_ops.find_customers_by_state(state)
        elif user_choice == '6':
            customer_id = input("Enter customer ID to mark as Gold Customer: ")
            db_ops.mark_gold_customer(customer_id)
        elif user_choice == '7':
            db_ops.show_gold_customers()
        elif user_choice == '8':
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please choose again.")

def add_clothing_item():
    clothing_id = input("Enter Clothing ID: ")
    price = input("Enter Price: ")
    db_ops.add_clothing_item(clothing_id, price)

def delete_clothing_item():
    clothing_id = input("Enter Clothing ID to delete: ")
    db_ops.delete_clothing_item(clothing_id)

def update_clothing_item():
    clothing_id = input("Enter Clothing ID to update: ")
    new_price = input("Enter new Price: ")
    db_ops.update_clothing_item(clothing_id, new_price)

if __name__ == '__main__':
    start_app()

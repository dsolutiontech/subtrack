import csv
import logging
from datetime import datetime, timedelta
import re
import os

# Define a function to print the script's logo
def print_logo():
    print(r"""
 _____            _       _   _          _______        _
|  __ \          | |     | | (_)        |__   __|      | |
| |  | |___  ___ | |_   _| |_ _  ___  _ __ | | ___  ___| |__
| |  | / __|/ _ \| | | | | __| |/ _ \| '_ \| |/ _ \/ __| '_ '\
| |__| \__ \ (_) | | |_| | |_| | (_) | | | | |  __/ (__| | | |
|_____/|___/\___/|_|\__,_|\__|_|\___/|_| |_|_|\___|\___|_| |_|
                    +-+-+-+-+-+-+-+-+-+
                    |S|u|b|_|T|r|a|c|k|
                    +-+-+-+-+-+-+-+-+-+
""")

print_logo()

# Set up logging
LOGFILE = '/workspaces/python-development/python/Subscription_Tracker/subscriptions_log.log'
logging.basicConfig(filename=LOGFILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the filename where subscription data will be stored
FILENAME = '/workspaces/python-development/python/Subscription_Tracker/subscriptions.csv'

def is_valid_email(email):
    """Validate email format."""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def load_subscriptions():
    """Load subscriptions from a CSV file."""
    subscriptions = []
    try:
        with open(FILENAME, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            subscriptions = list(reader)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        pass
    return subscriptions

def save_subscription(customer_name, purchase_date, duration_months, expiration_date, email):
    """Save a new subscription to the CSV file."""
    file_exists = os.path.isfile(FILENAME)
    with open(FILENAME, mode='a', newline='') as file:
        fieldnames = ['Customer Name', 'Purchase Date', 'Months', 'Renewal Date', 'Email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if file did not exist
        if not file_exists:
            writer.writeheader()
        
        # Write the subscription data
        writer.writerow({
            'Customer Name': customer_name,
            'Purchase Date': purchase_date,
            'Months': duration_months,
            'Renewal Date': expiration_date,
            'Email': email
        })

def calculate_expiration_date(purchase_date, duration_months):
    """Calculate the expiration date based on the purchase date and duration."""
    purchase_date_obj = datetime.strptime(purchase_date, '%Y-%m-%d')
    expiration_date = purchase_date_obj + timedelta(days=30 * duration_months)  # approximate days in a month
    return expiration_date.strftime('%Y-%m-%d')

def input_duration():
    """Get a valid subscription duration in months from the user."""
    while True:
        try:
            duration_months = int(input("Enter duration (in months): "))
            if duration_months <= 0:
                raise ValueError("Duration must be a positive integer.")
            return duration_months
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a positive integer.")

def input_date(prompt):
    """Get a valid date input from the user."""
    while True:
        date_str = input(prompt)
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def input_email():
    """Get a valid email input from the user."""
    while True:
        email = input("Enter account owner email: ")
        if is_valid_email(email):
            return email
        print("Invalid email format. Please try again.")

def add_subscription():
    """Add a new subscription entry."""
    customer_name = input("Enter customer name: ")
    email = input_email()
    purchase_date = input_date("Enter purchase date (YYYY-MM-DD): ")
    duration_months = input_duration()
    
    expiration_date = calculate_expiration_date(purchase_date, duration_months)
    
    save_subscription(customer_name, purchase_date, duration_months, expiration_date, email)
    print(f"Subscription for {customer_name} added. Expires on {expiration_date}.")
    logging.info(f"Added subscription for {customer_name} with duration {duration_months} months.")

def save_all_subscriptions(subscriptions):
    """Save all subscriptions back to the CSV file."""
    with open(FILENAME, mode='w', newline='') as file:
        fieldnames = ['Customer Name', 'Purchase Date', 'Months', 'Renewal Date', 'Email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for sub in subscriptions:
            writer.writerow(sub)

def renew_subscription():
    """Renew an existing subscription."""
    customer_name = input("Enter customer name to renew subscription: ")
    subscriptions = load_subscriptions()
    found = False

    for index, sub in enumerate(subscriptions):
        if sub['Customer Name'] == customer_name:
            found = True
            duration_months = input_duration()
            new_purchase_date = datetime.now().strftime('%Y-%m-%d')
            new_expiration_date = calculate_expiration_date(new_purchase_date, duration_months)

            # Update subscription data
            subscriptions[index]['Purchase Date'] = new_purchase_date
            subscriptions[index]['Months'] = str(duration_months)
            subscriptions[index]['Renewal Date'] = new_expiration_date
            
            save_all_subscriptions(subscriptions)  # Save all updates
            print(f"Subscription for {customer_name} renewed. New expiration date is {new_expiration_date}.")
            logging.info(f"Renewed subscription for {customer_name} with new duration {duration_months} months.")
            break

    if not found:
        print("Customer not found or unable to renew.")

def delete_subscription():
    """Cancel a subscription."""
    customer_name = input("Enter customer name to cancel subscription: ")
    subscriptions = load_subscriptions()
    found = False

    for index, sub in enumerate(subscriptions):
        if sub['Customer Name'] == customer_name:
            found = True
            
            # Ask for a reason for cancellation
            cancellation_reason = input("Enter reason for cancellation: ")
            # Log the cancellation reason
            logging.info(f"Canceled subscription for {customer_name}. Reason: {cancellation_reason}")

            # Remove the subscription
            subscriptions.pop(index)
            save_all_subscriptions(subscriptions)  # Save all updates
            print(f"Subscription for {customer_name} has been canceled.")
            break

    if not found:
        print("Customer not found or unable to cancel.")

def check_expiring_within_two_weeks():
    """Check for subscriptions expiring within two weeks."""
    subscriptions = load_subscriptions()
    today = datetime.now()
    two_weeks_from_now = today + timedelta(weeks=2)
    expiring_subscriptions = []

    for sub in subscriptions:
        expiration_date = datetime.strptime(sub['Renewal Date'], '%Y-%m-%d')
        if today <= expiration_date <= two_weeks_from_now:
            expiring_subscriptions.append(sub)

    if expiring_subscriptions:
        print("\nSubscriptions Expiring Within Two Weeks:")
        print(f"{'Customer Name':<20} {'Renewal Date':<15} {'Months':<10} {'Email'}")
        for sub in expiring_subscriptions:
            print(f"{sub['Customer Name']:<20} {sub['Renewal Date']:<15} {sub['Months']:<10} {sub['Email']}")
    else:
        print("No subscriptions are expiring within the next two weeks.")

def view_expired_subscriptions():
    """View expired subscriptions."""
    subscriptions = load_subscriptions()
    today = datetime.now()
    expired_subscriptions = []

    for sub in subscriptions:
        expiration_date = datetime.strptime(sub['Renewal Date'], '%Y-%m-%d')
        if expiration_date < today:
            expired_subscriptions.append(sub)

    if expired_subscriptions:
        print("\nExpired Subscriptions:")
        print(f"{'Customer Name':<20} {'Renewal Date':<15} {'Months':<10} {'Email'}")
        for sub in expired_subscriptions:
            print(f"{sub['Customer Name']:<20} {sub['Renewal Date']:<15} {sub['Months']:<10} {sub['Email']}")
    else:
        print("No expired subscriptions found.")

def display_subscriptions():
    """Display all current subscriptions sorted by email."""
    subscriptions = load_subscriptions()
    
    if not subscriptions:
        print("No subscriptions found.")
        return

    # Sort subscriptions by email
    subscriptions.sort(key=lambda x: x['Email'])

    print("\nCurrent Subscriptions (Sorted by Email):")
    print(f"{'Customer Name':<20} {'Purchase Date':<15} {'Months':<10} {'Renewal Date':<15} {'Email'}")
    for sub in subscriptions:
        print(f"{sub['Customer Name']:<20} {sub['Purchase Date']:<15} {sub['Months']:<10} {sub['Renewal Date']:<15} {sub['Email']}")

def main():
    """Main function to run the subscription tracker."""
    while True:
        print("\nNetflix Subscription Tracker")
        print("1. Add Subscription")
        print("2. Renew Subscription")
        print("3. Cancel Subscription")
        print("4. View Subscriptions")
        print("5. Check Expiring Subscriptions (Next 2 Weeks)")
        print("6. View Expired Subscriptions")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_subscription()
        elif choice == '2':
            renew_subscription()
        elif choice == '3':
            delete_subscription()
        elif choice == '4':
            display_subscriptions()
        elif choice == '5':
            check_expiring_within_two_weeks()
        elif choice == '6':
            view_expired_subscriptions()
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# subtrack
![image](https://github.com/user-attachments/assets/68c9e202-bb5b-428d-9a97-782e46d681ce)
The provided code is a subscription tracker written in Python that allows users to manage subscriptions for a service (like Netflix).
### Overview of the Code

1. **Imports and Logging Configuration**:
   - The script imports necessary modules, including `csv`, `logging`, `datetime`, `re`, and `os`.
   - It sets up logging to keep track of actions performed on subscriptions, storing logs in a specified log file (`subscriptions_log.log`).

2. **File Management**:
   - Subscriptions are stored in a CSV file (`subscriptions.csv`), with functions to load and save subscription data.

3. **Validation Functions**:
   - `is_valid_email(email)`: Validates the format of an email address.
   - `input_date(prompt)`: Prompts for a valid date input from the user.
   - `input_email()`: Prompts for a valid email address until a correct format is provided.

4. **Subscription Management Functions**:
   - `add_subscription()`: Collects user input and saves a new subscription, including customer name, email, purchase date, and duration in months.
   - `renew_subscription()`: Allows renewal of an existing subscription by updating the purchase date and expiration date.
   - `delete_subscription()`: Cancels a subscription based on the customer's name and logs the cancellation reason.

5. **Expiration Checks**:
   - `check_expiring_within_two_weeks()`: Checks and displays subscriptions that will expire within the next two weeks.
   - `view_expired_subscriptions()`: Displays subscriptions that have already expired.

6. **Display Functions**:
   - `display_subscriptions()`: Displays all current subscriptions, sorted by email address.

7. **Main Loop**:
   - `main()`: The entry point of the script, providing a menu for users to interact with the subscription tracker. Users can add, renew, cancel subscriptions, and view relevant information.

### Usage Steps

1. Run the script, which prompts the user with several options.
2. Enter the corresponding choice to:
   - Add a new subscription.
   - Renew an existing subscription.
   - Cancel an existing subscription.
   - View all subscriptions.
   - Check subscriptions expiring within the next two weeks.
   - View expired subscriptions.
   - Exit the program.

### Validation and Error Handling
- The script includes various input validations (for email and dates) and error handling (for file operations), ensuring robustness in user interaction.

### Example of a Menu Interaction
When the program is running, the user will see:
```
Netflix Subscription Tracker
1. Add Subscription
2. Renew Subscription
3. Cancel Subscription
4. View Subscriptions
5. Check Expiring Subscriptions (Next 2 Weeks)
6. View Expired Subscriptions
7. Exit
Choose an option: 
```

Depending on the user's input, different functionalities can be executed, making it a comprehensive tool for managing subscriptions.

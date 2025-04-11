#Name: Pratham Radhakrishna 
#ID:s3997064
# Attempted all the  parts

# Initializing customer data

customers = {'Kate': 20, 'Tom': 32}
# Initializing an empty dictionary to store order history for each customer
orders = {}


# Initializing product data with their prices and doctor's prescription requirements
products = {
    'vitaminC': {'price': 12.0, 'prescription_mandatory': False},
    'vitaminE': {'price': 14.5, 'prescription_mandatory': False},
    'coldTablet': {'price': 6.4, 'prescription_mandatory': False},
    'vaccine': {'price': 32.6, 'prescription_mandatory': True},
    'fragrance': {'price': 25.0, 'prescription_mandatory': False}
}

#######################################################################################################

def purchase():
    # Inputing customer details
    while True:
        cust_name = input("Enter the customer name: ")
        if cust_name.isalpha():
            break
        else:
            print("Error! Customer name should only contain alphabet characters.")

    # Inputing product details
    while True:
        prod_name = input("Enter the names of the products separated by commas(,): ").split(',')
        prod_name = [p.strip() for p in prod_name]
        if all(product in products for product in prod_name):
            break
        else:
            print("Error! Invalid product entered.")

    # Inputing quantity
    while True:
        qty = input("Enter the quantity separated by commas(,): ").split(',')
        try:
            qty = [int(q.strip()) for q in qty]
            if any(q <= 0 for q in qty):
                raise ValueError
            break 
        except ValueError:
            print("Error! quantity must be positive integers.")

    # Checking prescription requirements
    for product_name in prod_name:
        if products[product_name]['prescription_mandatory']:
            prescription = input(f"Do you have a doctor  prescription for {product_name}? (y/n): ")
            if prescription.lower() != 'y':
                print(f"{product_name} needs a doctor's prescription. Purchase of this product cannot be completed.")
                return

    # Calculating purchase details
    total_amt = sum(products[p]['price'] * q for p, q in zip(prod_name, qty))
    reward_pts = round(total_amt)

    # Deducting reward points
    if customers.get(cust_name, 0) >= 100:
        discount = (customers[cust_name] // 100) * 10
        total_amt -= discount
        customers[cust_name] -= discount

    # Updating customer data
    if cust_name in customers:
        customers[cust_name] += reward_pts
    else:
        customers[cust_name] = reward_pts
    
    # Updating order history
    add_order(cust_name, {p: q for p, q in zip(prod_name, qty)}, total_amt, reward_pts)

    # Displaying receipt
    display_bill(cust_name, prod_name, qty, total_amt, reward_pts)
    
#######################################################################################################    
    
def add_order(cust_name, products, total_amt, earned_rewards):
    if cust_name not in orders:
        orders[cust_name] = []
    orders[cust_name].append({ 
        'products': products,
        'total_amt': total_amt,
        'earned_rewards': earned_rewards
    })
   
#######################################################################################################

def display_bill(cust_name, prod_name, qty, total_amt, reward_pts):
    print("---------------------------------------------------------")
    print("Receipt")
    print("---------------------------------------------------------")
    print(f"Name: {cust_name}")
    
    for product_name, quantity in zip(prod_name, qty):
        print(f"Product: {product_name}")
        print(f"Unit Price: {products[product_name]['price']:.2f} (AUD)")
        print(f"Quantity: {quantity}")
        
    print("---------------------------------------------------------")
    print(f"Total cost: {total_amt:.2f} (AUD)")
    print(f"Earned reward: {reward_pts}")
    print("---------------------------------------------------------")
    
#######################################################################################################

def update_prod():
    products_info = input("Enter product information separated by commas (name price dr_prescription): ").split(',')
    products_info = [info.strip() for info in products_info]
    products_info = [info.split() for info in products_info]
    
    for info in products_info:
        product_name, price, dr_prescription = info[0], float(info[1]), info[2]
        prescription_mandatory = True if dr_prescription.lower() == 'y' else False

        products[product_name] = {'price': price, 'prescription_mandatory': prescription_mandatory}
        
#######################################################################################################

def display_cust():
    print("Existing Customers:")
    for customer, reward_pts in customers.items():
        print(f"{customer}: {reward_pts} reward points")

#######################################################################################################

def display_prod():
    print("Existing Products:")
    for product, details in products.items():
        prescription = "Yes" if details['prescription_mandatory'] else "No"
        print(f"{product}: Price - {details['price']} (AUD), Prescription Required - {prescription}")

#######################################################################################################

def order_history():
    cust_name = input("Enter the name of the customer: ")
    if cust_name in orders:
        print(f"This is the order history of {cust_name}:")
        print("Order    Products                        Total Cost    Earned Rewards")
        for i, order in enumerate(orders[cust_name], start=1):
            product_info = ", ".join(f"{p}: {q}" for p, q in order['products'].items())
            print(f"Order {i:<3} {product_info:<30} {order['total_amt']:<12} {order['earned_rewards']}")
    else:
        print("This customer hasn't made any purchases")

#######################################################################################################

# Main program
while True:
    print("\nMenu:")
    print("1. Make a purchase")
    print("2. Add/update information of products")
    print("3. Display existing customers")
    print("4. Display existing products")
    print("5. Display a customer order history")
    print("6. Exit the program")

    choice = input("Enter your choice (1-6): ")

    if choice == '1':
        purchase()
    elif choice == '2':
        update_prod()
    elif choice == '3':
        display_cust()
    elif choice == '4':
        display_prod()
    elif choice == '5':
        order_history()
    elif choice == '6':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
        
#######################################################################################################

#Data Structures::
# customers: A dictionary is created storing customer names and reward points
# orders: An empty dictionary is created to store order history for each customer.
# products: A dictionary is created having product details like price and whether a prescription is required or not

# Functions:
# purchase(): manages the purchasing process. It will ask the user to input  the customer details, product names, qty, and checks if any prescription is required or not. It calculates the total cost, deducts reward points and updates customer data and adds the order to the history.
# add_order: Adds the order to the order history for that particular customer.
# display_bill: Displays a receipt for the purchase of the customer.
# update_prod(): Allows the  adding or updating product information .
# display_cust(): Displays the existing customers  with the reward points.
# display_prod(): Displays the products with their prices and prescription  if needed or not .
# order_history(): Displays the order history for a specific customer.


# User Interface:
# The main program runs in a loop displaying a menu of options.
# Users can choose to make a purchase (1), update product information (2), display customers (3), display products (4), display customer order history (5), or exit the program (6).
# Input validation is employed in various parts of the code to ensure correct data entry (e.g., customer name, product names, qty).

#REFERENCE
#https://github.com/topics/python-application - reseached and explored the operation of various functions and parameters
#https://www.w3schools.com/python/python_examples.asp - for understanding how functions works and its purpose .
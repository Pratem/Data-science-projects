#Name: Pratham Radhakrishna
# ID : s3997064
# i have attempted till DI level , my program seems to crash after that and im not able to resolve the errors

# Custom exception classes for specific error conditions
class InvalidNameError(Exception):
    pass

class InvalidProductError(Exception):
    pass

class InvalidQuantityError(Exception):
    pass

class InvalidPrescriptionAnswerError(Exception):
    pass
class InvalidPrescriptionError(Exception):
    pass

class InsufficientStockError(Exception):
    pass

##############################################################################
# function to take bundle info
class Bundle:
    def __init__(self, ID, name, components):
        self.ID = ID
        self.name = name
        self.components = components

#function to calculate price 
    def calculate_price(self):
        total_price = sum(component.price for component in self.components)
        return 0.8 * total_price

# display  customer info function
    def display_info(self):
        prescription_required = any(component.requires_prescription for component in self.components)
        prescription = "Yes" if prescription_required else "No"
        component_ids = ', '.join(component.ID for component in self.components)
        print(f"ID: {self.ID}, Name: {self.name}, Component IDs: {component_ids}, Price: {self.calculate_price()}, Prescription Required: {prescription}")

##############################################################################
#customer info class

class Customer:
    def __init__(self, ID, name, reward):
        self.ID = ID
        self.name = name
        self.reward = reward 

    def get_reward(self):
        pass

    def get_discount(self):
        pass

    def update_reward(self, value):
        pass

    def display_info(self):
        pass

##############################################################################
class BasicCustomer(Customer):
    def __init__(self, ID, name, reward, reward_rate=1.0):
        super().__init__(ID, name, reward)
        self.reward_rate = reward_rate

    def get_reward(self, total_cost):
        return round(total_cost * self.reward_rate)

    def update_reward(self, value):
        self.reward += value

    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Reward Rate: {self.reward_rate}")

##############################################################################
# functiom for VIP customer
class VIPCustomer(Customer):
    def __init__(self, ID, name, reward, reward_rate=1.0, discount_rate=0.08):
        super().__init__(ID, name, reward)
        self.reward_rate = reward_rate
        self.discount_rate = discount_rate

    def get_discount(self, total_cost):
        return total_cost * self.discount_rate

    def get_reward(self, total_cost):
        return round((total_cost - self.get_discount(total_cost)) * self.reward_rate)

    def update_reward(self, value):
        self.reward += value

    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Reward Rate: {self.reward_rate}, Discount Rate: {self.discount_rate}")

##############################################################################
class Product:
    def __init__(self, product_id, product_name, price, requires_prescription, components=None):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.requires_prescription = requires_prescription
        self.components = components if components is not None else []

    def display_info(self):
        if self.product_id.startswith('B'):  # Check if it's a bundle
            print(f"{self.product_id}, {self.product_name}, {', '.join(self.components)}")
            
        else:
            
            print(f"ID: {self.product_id}, Name: {self.product_name}, Price: {self.price}, Prescription: {'Yes' if self.requires_prescription else 'No'}")


##############################################################################
class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []

    def add_item(self, product, quantity):
        self.items.append((product, quantity))

    def compute_cost(self):
        total_cost = 0
        for product, quantity in self.items:
            total_cost += product.price * quantity
        discount = self.customer.get_discount(total_cost) if isinstance(self.customer, VIPCustomer) else 0
        final_cost = total_cost - discount
        reward_points = self.customer.get_reward(final_cost)
        return total_cost, discount, final_cost, reward_points

    def display_receipt(self):
        total_cost, discount, final_cost, reward_points = self.compute_cost()
        print("Receipt:")
        print(f"Customer: {self.customer.name}")
        for product, quantity in self.items:
            print(f"Product: {product.product_name}, Quantity: {quantity}")
        print(f"Total cost: {total_cost} (AUD)")
        print(f"Discount: {discount} (AUD)")
        print(f"Final cost: {final_cost} (AUD)")
        print(f"Earned reward points: {reward_points}")



##############################################################################
class Records: 
    def __init__(self):
        self.customers = []
        self.products = []
        self.bundles = [] 
        
    def add_or_update_product(self, product_id, product_name, price, requires_prescription):
        product = self.find_product(product_id)
        if product:
            # Updating existing product
            product.product_name = product_name
            product.price = price
            product.requires_prescription = requires_prescription
            print(f"Product '{product_id}' updated successfully.")
        else:
            # Adding new product
            self.products.append(Product(product_id, product_name, price, requires_prescription))
            print(f"New product '{product_id}' added successfully.")
    
    def adjust_reward_rate(self, new_rate):
        try:
            new_rate = float(new_rate)
            if new_rate <= 0:
                raise ValueError("Reward rate must be a positive number.")
            for customer in self.customers:
                if isinstance(customer, BasicCustomer):
                    customer.reward_rate = new_rate
            print("Reward rate adjusted for all Basic customers.")
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid positive number for the reward rate.")

    def adjust_discount_rate(self):
        try:
            # Prompting user for customer's name or ID
            customer_input = input("Enter the name or ID of the VIP customer: ")
            customer = self.find_customer(customer_input)
            if customer is None or not isinstance(customer, VIPCustomer):
                print("Invalid VIP customer. Please enter a valid VIP customer.")
                return

            # Prompting user for the new discount rate
            new_rate = input("Enter the new discount rate (as a percentage, e.g., 20 for 20%): ")
            new_rate = float(new_rate)
            if new_rate <= 0:
                raise ValueError("Discount rate must be a positive number.")
        
            # Updating the discount rate of the VIP customer
            customer.discount_rate = new_rate / 100  # Convert percentage to decimal

            print(f"Discount rate adjusted for {customer.name} to {new_rate}%.")
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid positive number for the discount rate.")
        except InvalidNameError:
            print("Invalid VIP customer. Please enter a valid VIP customer.")
            

    def read_customers(self, filename):
     with open(filename, 'r') as file:
        for line in file:
            data = [item.strip() for item in line.strip().split(',')]
            if len(data) >= 4:
                if data[0].startswith('B'):
                    reward = float(data[3])
                    self.customers.append(BasicCustomer(data[0], data[1], reward))
                elif data[0].startswith('V') and len(data) >= 5:
                    reward = float(data[4])
                    discount_rate = float(data[3])
                    self.customers.append(VIPCustomer(data[0], data[1], reward, discount_rate=discount_rate))
                else:
                    print("Invalid data format:", data)
            else:
                print("Invalid data format:", data)  

    def read_products(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                data = [item.strip() for item in line.strip().split(',')]
                if len(data) >= 4:  # Ensure all required data is present
                    product_id = data[0]
                    product_name = data[1]
                    price = data[2]
                    requires_prescription = data[3].lower() == 'y'  # Checking if prescription is required
                    if product_id.startswith('B'):
                        components = [component.strip() for component in data[2:]]  # Bundle components
                        self.bundles.append(Product(product_id, product_name, price, requires_prescription, components))
                    else:
                        self.products.append(Product(product_id, product_name, price, requires_prescription))
                else:
                    print("Invalid data format:", data)
                
    def find_bundle(self, search_value):
    # First, try searching by ID
     for bundle in self.bundles:
        if bundle.ID == search_value:
            return bundle

    # If not found by ID, try searching by name
     for bundle in self.bundles:
        if bundle.name.lower() == search_value.lower():
            return bundle

    # If not found by ID or name, return None
     return None
   
    def find_customer(self, search_value):
    # First, try searching by ID
     for customer in self.customers:
        if customer.ID == search_value:
            return customer

    # If not found by ID, try searching by name
     for customer in self.customers:
        if customer.name.lower() == search_value.lower():
            return customer

    # If not found by ID or name, return None
     return None

    def find_product(self, search_value):
    # First, try searching by ID
     for product in self.products:
        if product.product_id == search_value:
            return product

    # If not found by ID, try searching by name
     for product in self.products:
        if product.product_name.lower() == search_value.lower():
            return product

    # If not found by ID or name, return None
     return None    

    def list_customers(self):
        for customer in self.customers:
            customer.display_info()

    def list_products(self):
     print("Existing Products:")
     for product in self.products:
        product.display_info()

     
     for bundle in self.bundles:
        bundle.display_info()


##############################################################################
class Operations:
    def __init__(self):
        self.records = Records()
        self.records.read_customers("customers.txt")
        self.records.read_products("products.txt")

# Inside the Operations class
    def make_purchase(self):
    # Prompt user to enter customer details
        customer_input = input("Enter customer ID or name: ")
        
        customer = self.records.find_customer(customer_input)
        if customer is None:
         print("Customer not found.")
         return

    # Prompt user to enter product/bundle details
        product_input = input("Enter product/bundle ID or name: ")
        product_or_bundle = self.records.find_product(product_input) or self.records.find_bundle(product_input)
       
        if product_or_bundle is None:
         print("Product or bundle not found.")
         return

    # Prompt user to enter quantity
        quantity_input = input("Enter quantity: ")
        try:
           quantity = int(quantity_input) 
           if quantity <= 0:
            raise InvalidQuantityError
        except ValueError:
         print("Invalid quantity. Quantity must be a positive integer.")
         return
        except InvalidQuantityError:
         print("Invalid quantity. Quantity must be greater than zero.")
        return
         
       

       
  
    # Process purchase
        try:
        # Create an order instance
         order = Order(customer)
         print("Order object created with customer:", order.customer.name)

        # Add the purchased item to the order
         order.add_item(product_or_bundle, quantity)
         print("Item added to the order:", product_or_bundle.name, "Quantity:", quantity)

        # Compute and display the receipt
         total_cost, discount, final_cost, reward = order.compute_cost()
         print("Purchase successful.")
         order.display_receipt()
         
         print("Purchase successful.")
         print("Receipt:") 
         print(f"Customer: {customer.name}")
         print(f"Product/Bundle: {product_or_bundle.name}")
         print(f"Quantity: {quantity}")
         print(f"Total cost: {final_cost} (AUD)")
         print(f"Earned reward: {reward}")

        except InvalidPrescriptionError:
         print("Cannot purchase this product. A doctor's prescription is required.")
        except InsufficientStockError:
         print("Insufficient stock available.")
        except Exception as e:
         print(f"An error occurred: {e}")
         
        
       
    def display_existing_customers(self):
        self.records.list_customers()

    def display_existing_products(self):
        self.records.list_products()
    
    def add_or_update_product(self):
        
        
        product_id = input("Enter product ID: ")
        product_name = input("Enter product name: ")
        price = float(input("Enter price: "))
        requires_prescription = input("Requires prescription? (y/n): ").lower() == 'y'

        self.records.add_or_update_product(product_id, product_name, price, requires_prescription)

    def adjust_reward_rate(self):
        # Implementation for adjusting the reward rate of all Basic customers
        new_rate = float(input("Enter the new reward rate: "))
        if new_rate <= 0:
            print("Invalid reward rate. Please enter a positive number.")
            return

        self.records.adjust_reward_rate(new_rate)

    def adjust_discount_rate(self): 
        self.records.adjust_discount_rate()


    def run(self):
        while True:
            print("1. Make a purchase")
            print("2. Display existing customers")
            print("3. Display existing products")
            print("4. Add/update information of products")
            print("5. Adjust the reward rate")
            print("6. Adjust the discount rate")
            print("7. Exit the program")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.make_purchase()
            elif choice == '2':
                self.display_existing_customers()
            elif choice == '3':
                self.display_existing_products()
            elif choice == '4':
                self.add_or_update_product()
            elif choice == '5':
                self.adjust_reward_rate()
            elif choice == '6':
                self.adjust_discount_rate()
            elif choice == '7':
                print("Exiting the program...")
                break
            else:
                print("Invalid choice. Please try again.")


# Main program
if __name__ == "__main__":
    app = Operations()
    app.run()    

##############################################################################
# Bundle Class:

# The Bundle class represents a collection of products sold together at a discounted price. It contains methods to calculate the total price of the bundle (with a discount) and to display the bundle's information, including whether a prescription is required for any component.
# Customer and Subclasses:

# The Customer class is a base class with methods for managing rewards and discounts. The BasicCustomer and VIPCustomer subclasses inherit from it, implementing specific behaviors:
# BasicCustomer can accumulate rewards based on purchase totals.
# VIPCustomer can receive discounts on purchases and accumulate rewards on the discounted total.
# Product Class:

# The Product class represents individual products, each with an ID, name, price, and a flag indicating if a prescription is required. It also includes a method to display product details.
# Order Class:

# The Order class manages the items purchased by a customer, calculates the total cost, applies discounts if applicable, and calculates reward points. It also generates and displays a receipt for the purchase.
# Records Class:

# The Records class is responsible for managing the lists of customers, products, and bundles. It includes methods to read customer and product data from files, find specific customers/products, and adjust reward/discount rates.
# Operations Class:

# The Operations class handles the main operations of the program, such as making purchases, displaying customers/products, adding/updating products, and adjusting reward/discount rates. It uses a loop to present a menu to the user and perform actions based on user input.

# Initialization:

# The Operations class initializes by reading customer and product data from files.
# User Interaction:

# A menu-driven interface is presented to the user, allowing them to choose actions such as making a purchase, displaying customers/products, and adjusting rates.
# Making a Purchase:

# When making a purchase, the program prompts for customer and product details, validates the input, calculates the total cost, applies any discounts, and updates the customer's rewards. It then displays a receipt.
# Managing Products and Customers:

# The program includes functionalities to add or update product information and adjust reward or discount rates for customers, demonstrating extensibility and flexibility in handling retail operations.
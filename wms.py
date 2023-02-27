"""
This program forms part of a warehouse management system for a fashion and lifestyle brand.
Focusing on footwear, the program supports store managers based internationally who would
like to be able to:
~ search for products by code,
~ determine which products have the highest and lowest quantities,
~ calculate the total value of each stock item.

The program makes use of OOP and SQLite.
For the sake of example, each product code and quantity is assumed to refer to every size of a particular model.
"""

# To begin, import sqlite3
import sqlite3

# Create a file to store the database, and a cursor item to interact with the same.
db = sqlite3.connect("wms_footwear_db")
cursor = db.cursor()

# Create the table and assign a primary key.
cursor.execute('''CREATE TABLE IF NOT EXISTS footwear(
                    Country VARCHAR(225),
                    Code VARCHAR(225) NOT NULL PRIMARY KEY, 
                    Product VARCHAR(225), 
                    Cost INT, 
                    Qty INT)
                ''')
db.commit()

# Populate the table with the first data set.
data = [
        ("South Africa", "SKU44386", "Gaia Sandal Dove", 365, 20),
        ("China", "SKU90000", "Gaia Sandal Soft Rose", 365, 50),
        ("United States", "SKU63221", "Gaia Wedge Black", 395, 25),
        ("United States", "SKU29077", "Gaia Wedge Black Dye", 395, 60),
        ("Russia", "SKU89999", "June Boot Candle", 595, 43),
        ("Australia", "SKU71827", "Lola Loafer Shearling Black", 320, 15),
        ("South Korea", "SKU66734", "Dash Ballerina Black", 390, 7),
        ("Russia", "SKU93222", "Marine Ankle Boot Black", 475, 10),
        ("UK", "SKU79084", "Marine Ankle Boot Terrazzo", 475, 4),
        ("Japan", "SKU95000", "Isa Boot Shiny Black", 575, 2),
        ("India", "SKU38773", "Julio Sandal Root Mix", 395, 29),
        ("Colombia", "SKU87500", "Isa Sandal Black", 375, 8),
        ("Brazil", "SKU44600", "Isa Sandal Silver Mix", 395, 24),
        ("France", "SKU77999", "Isa Sandal Eternal", 395, 67),
        ("Morocco", "SKU33000", "Isa Sandal White Satin", 395, 9),
        ("UK", "SKU29888", "June Strappy Platform Emporium", 595, 5),
        ("Morocco", "SKU77744", "June Platform Black", 475, 11),
        ("Russia", "SKU20207", "June Platform Zebra", 495, 7),
        ("France", "SKU84500", "June Platform Tan", 475, 28),
        ("UK", "SKU76000", "June Sandal Diamante Silver", 495, 32),
        ("Egypt", "SKU19888", "Julio Anklet Sandal Silver Mix", 550, 26),
        ("Canada", "SKU68677", "Julio Anklet Sandal Black", 495, 13),
        ("Australia", "SKU57443", "June Boot Zebra", 595, 4),
        ("France", "SKU20394", "June Sandal Diamante Tan", 495, 17),
    ]

cursor.executemany('''INSERT OR IGNORE INTO footwear VALUES(?,?,?,?,?)''', data)
db.commit()


# Create a class with data attributes for each shoe object to be stored in the program.
# Create methods relevant to this class.
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.code}\n{self.product}\n" \
               f"Cost: GBP{self.cost:,.2f}\nIn Stock: {self.quantity}\n" \
               f"Country: {self.country}\n"


# Create a list to store every instance of the Shoe class.
shoes = []


# Define the functions that will make up the menu items of the program.
def read_shoes_data():
    try:
        cursor.execute('''SELECT * FROM footwear''')
        entry = cursor.fetchall()
        if entry:
            for row in entry:
                country = row[0]
                code = row[1]
                product = row[2]
                cost = int(row[3])
                quantity = int(row[4])

                new_shoe = Shoe(country, code, product, cost, quantity)
                shoes.append(new_shoe)
            print("Shoe data import successful.\n")
    except (ValueError, sqlite3.ProgrammingError):
        print("Unable to locate inventory file.\n")
    finally:
        db.close()


def capture_shoe():
    while True:
        try:
            code = input("Code: ").upper()
            product = input("Product: ")
            cost = float(input("Cost: "))
            quantity = int(input("Quantity: "))
            country = input("Country: ")

            new_shoe = Shoe(country, code, product, cost, quantity)
            shoes.append(new_shoe)
            print("Shoe data added successfully.\n")
            break
        except ValueError:
            print("Verify product details")


def view_all():
    for item in shoes:
        print(item)


def search_shoe():
    code = input("Search by product code: ").upper()
    print(next((item for item in shoes if item.code == code), "Product not found.\n"))


def value_per_item():
    for item in shoes:
        value = f"Value: GBP{item.cost * item.quantity:,.2f}"
        print(f"{item}{value}\n")


def re_stock():
    lowest = min(shoes, key=lambda x: x.quantity)
    print(f"{lowest.code} {lowest.product} has only {lowest.quantity} units available for sale.\n")


def highest_qty():
    highest = max(shoes, key=lambda x: x.quantity)
    print(f"{highest.code} {highest.product} has {highest.quantity} units available for sale.\n")


def check_inventory():
    if not shoes:
        print("Shoe inventory empty. Import or manual enter shoe data to continue.\n")


# Create the program menu within a while loop.
# Call previously defined functions with the corresponding user input.
print("""Main Menu
Enter your selection (0 - 7) from the menu options below:""")
while True:
    try:
        menu = int(input("""1. Import Shoe Data
2. Enter Shoe Data
3. View All
4. View Value Per Item
5. View High Stock
6. View Low Stock
7. Product Search
0. Exit
"""))
        if menu == 1:
            read_shoes_data()
        elif menu == 2:
            capture_shoe()
        elif menu == 3:
            print("View All\n")
            check_inventory()
            view_all()
        elif menu == 4:
            print("View Value Per Item\n")
            check_inventory()
            value_per_item()
        elif menu == 5:
            print("View High Stock\n")
            check_inventory()
            if shoes:
                highest_qty()
        elif menu == 6:
            print("View Low Stock\n")
            check_inventory()
            if shoes:
                re_stock()
        elif menu == 7:
            print("Product Search\n")
            check_inventory()
            if shoes:
                search_shoe()
        elif menu == 0:
            print("You have been logged out.")
            break
    except ValueError:
        print("Invalid menu selection.\n")

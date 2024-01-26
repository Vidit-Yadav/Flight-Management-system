#__Mysql connector package
import mysql.connector        

class FlightManagementSystem:
    def __init__(self):
        # Establishing a connection to MySQL
        self.db_connection = mysql.connector.connect(host="localhost", user="root", passwd="admin")
        self.cursor = self.db_connection.cursor()
        self.setup_database()

    def setup_database(self):
        # Creating and using the 'airlines' database
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS airlines")
        self.cursor.execute("USE airlines")

        # Create table for food items
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_items (
                sl_no INT(4) AUTO_INCREMENT PRIMARY KEY,
                food_name VARCHAR(40) NOT NULL,
                price INT(4) NOT NULL
            )
        """)
        self.populate_food_items()

        # Create table for luggage entry
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS luggage (
                luggage_id INT(4) AUTO_INCREMENT PRIMARY KEY,
                weight INT(3) NOT NULL,
                price INT(4) NOT NULL
            )
        """)

        # Create table for customer details
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cust_details (
                cust_id INT(4) AUTO_INCREMENT PRIMARY KEY,
                cust_name VARCHAR(40) NOT NULL,
                cont_no BIGINT(10) NOT NULL
            )
        """)

        # Create table for customer's flight details
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS flight_details (
                cus_id INT(4),
                cus_name VARCHAR(40) NOT NULL,
                flight_id INT(4)
            )
        """)

        self.db_connection.commit()

    def populate_food_items(self):
        # Data for populating the food_items table
        food_items_data = [
            ('pepsi', 150),
            ('coffee', 70),
            ('tea', 50),
            ('water', 60),
            ('milk shake', 80),
            ('chicken burger', 160),
            ('cheese pizza', 70),
            ('chicken biryani', 300),
            ('plane rice', 80),
            ('aloo paratha', 120),
            ('roti sabji', 100),
            ('omelette', 50)
        ]

        # Inserting data into the food_items table
        self.cursor.executemany("INSERT INTO food_items (food_name, price) VALUES (%s, %s)", food_items_data)

    def close_connection(self):
        # Closing the MySQL connection
        self.db_connection.close()


# Function to handle luggage operations
def luggage(fms):
    print("What do you want to do?")
    print("1. Add luggage")
    print("2. Delete luggage")
    choice = input("Enter your choice: ")

    if choice == '1':
        lname = input("Enter luggage type: ")
        fms.cursor.execute("INSERT INTO luggage (weight, price) VALUES (%s, %s)", ('null', lname))
    elif choice == '2':
        lid = int(input("Enter your luggage id: "))
        fms.cursor.execute("DELETE FROM luggage WHERE luggage_id = %s", (lid,))
    else:
        print("**************** PLEASE ENTER A VALID OPTION *********************")

    fms.db_connection.commit()


# Function to handle food operations
def food(fms):
    print("What do you want to do?")
    print("1. Add new items")
    print("2. Update price")
    print("3. Delete items")
    choice = input("Enter your choice: ")

    if choice == '1':
        fname = input("Enter food name: ")
        fprice = int(input("Enter food price: "))
        fms.cursor.execute("INSERT INTO food_items (food_name, price) VALUES (%s, %s)", (fname, fprice))
    elif choice == '2':
        fid = int(input("Enter food id: "))
        fprice = int(input("Enter new price: "))
        fms.cursor.execute("UPDATE food_items SET price = %s WHERE food_id = %s", (fprice, fid))
    elif choice == '3':
        fid = int(input("Enter food id: "))
        fms.cursor.execute("DELETE FROM food_items WHERE food_id = %s", (fid,))
    else:
        print("**************** PLEASE ENTER A VALID OPTION ********************")

    fms.db_connection.commit()

def main():
    # Creating an instance of the FlightManagementSystem
    fms = FlightManagementSystem()

    while True:
        print("**************** YOUR DESIGNATION? *******************")
        print("1. Admin")
        print("2. User")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            admin(fms)
        elif choice == '2':
            user(fms)
        elif choice == '3':
            break
        else:
            print("************ PLEASE CHOOSE A CORRECT OPTION ******************")

    fms.close_connection()


#Admin Interface
def admin(fms):
    while True:
        sec = input("Enter the password: ")
        if sec == "admin":
            admin_actions(fms)
        else:
            print("************ YOUR PASSWORD IS INCORRECT *********")
            print("*********** PLEASE TRY AGAIN *****************")

def admin_actions(fms):
    print("************ WHAT'S YOUR TODAYS GOAL? ****************")
    print("1. Update details")
    print("2. Show details")
    print("3. Job approval")
    choice = input("Select your choice: ")

    if choice == '1':
        print("1. Classtype")
        print("2. Food")
        print("3. Luggage")
        x1 = input("Enter your choice: ")
        if x1 == '1':
            classtype(fms)
        elif x1 == '2':
            food(fms)
        elif x1 == '3':
            luggage(fms)
        else:
            print(" ********************** PLEASE ENTER A VALID OPTION ******************************** ")
    elif choice == '2':
        print("1. Classtype")
        print("2. Food")
        print("3. Luggage")
        print("4. Records")
        y = input("From which table: ")
        if y == '1':
            fms.cursor.execute("SELECT * FROM classtype")
        else:
            fms.cursor.execute("SELECT * FROM customer_details")
            z = fms.cursor.fetchall()
            for i in z:
                print(i)
                print("**************** THESE ABOVE PEOPLE HAVE BOOKED TICKET *****************************")

def classtype(fms):
    print("What do you want to do? ")
    print("1. Change the classtype name")
    print("2. Change the price of classtype")
    x = input("Enter your choice: ")
    if x == '1':
        oname = input("Enter old name: ")
        nname = input("Enter new name: ")
        fms.cursor.execute("UPDATE classtype SET %s = %s", (oname, nname))

def fooditems(fms):
    print("THE AVAILABLE FOODS ARE: ")
    fms.cursor.execute("SELECT * FROM food_items")
    x = fms.cursor.fetchall()
    for i in x:
        print("FOOD ID: ", i[0])
        print("FOOD Name: ", i[1])
        print("PRICE: ", i[2])
        print("__________________________________________________________________    ________________________")

def user(fms):
    while True:
        print("************** MAY I HELP YOU? *****************")
        print("1. Flight details")
        print("2. Food details")
        print("3. Book ticket")
        print("4. My details")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            flightavailable(fms)
        elif choice == '2':
            fooditems(fms)
        elif choice == '3':
            ticketbooking(fms)
        elif choice == '4':
            records(fms)
        elif choice == '5':
            break
        else:
            print("************ PLEASE CHOOSE A CORRECT OPTION ******************")


#TO SEE THE RECORDS OF THE CUSTOMER
def records(fms):
    cid = int(input("Enter your customer id: "))
    fms.cursor.execute("SELECT * FROM customer_details WHERE cus_id = %s", (cid,))
    d = fms.cursor.fetchall()
    print("YOUR DETAILS ARE HERE...........")
    print("Customer id: ", d[0])
    print("Name: ", d[1])
    print("Mobile number: ", d[2])
    print("Flight id: ", d[3])
    print("Flight name", d[4])
    print("Classtype: ", d[5])
    print("Departure place", d[6])
    print("Destination", d[7])
    print("Flight day: ", d[8])
    print("Flight time: ", d[9])
    print("Price of ticket: ", d[10])
    print("Date of booking ticket: ", d[11])


#TO BOOK THE TICKETS
def ticketbooking(fms):
    cname = input("Enter your name: ")
    cmob = int(input("Enter your mobile number: "))
    if cmob == 0000000000:
        print("MOBILE NUMBER CAN'T BE NULL")
        ticketbooking(fms)
    fid = int(input("Enter flight id: "))
    fcl = input("Enter your class: ")
    fname = input("Enter your flight name")
    dept = input("Enter departure place: ")
    dest = input("Enter destination: ")
    fday = input("Enter flight day: ")
    ftime = input("Enter flight time: ")
    fprice = input("Enter ticket rate: ")

    fms.cursor.execute("""
        INSERT INTO customer_details 
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE())
    """, (cname, cmob, fid, fname, fcl, dept, dest, fday, ftime, fprice))

    fms.db_connection.commit()


#TO SEE THE AVAILABLE FLIGHTS
def flightavailable(fms):
    print("THE AVAILABLE FLIGHTS ARE: ")
    fms.cursor.execute("SELECT * FROM flight_details")
    x = fms.cursor.fetchall()
    for i in x:
        print("Flight ID: ", i[0])
        print("Flight Name: ", i[1])
        print("Departure: ", i[2])
        print("Destination: ", i[3])
        print("Take Off Day: ", i[4])
        print("Take Off Time: ", i[5])
        print("Bussiness: ", i[6])
        print("Middle: ", i[7])
        print("Economic: ", i[8])
        print("__________________________________________________________________    ________________________")


# USER INTERFACE
def user():
    while True:
        print("************** MAY I HELP YOU? *****************")
        print("1. Flight details")
        print("2. Food details")
        print("3. Book ticket")
        print("4. My details")
        print("5. Exit")
        x = int(input("Enter your choice: "))
        if x == 1:
            flightavailable()
        elif x == 2:
            fooditems()
        elif x == 3:
            ticketbooking()
        elif x == 4:
            records()
        else:
            print("************ PLEASE CHOOSE A CORRECT OPTION ************")
            user()
        break

print("****************** WELCOME TO VAIBHAVI AIRLINES **********************")
print("************ MAKE YOUR JOURNEY SUCCESS WITH US! *****************")
print("\n\n\n\n\n")

# Main Interface
def menu1():
    print("**************** YOUR DESIGNATION? *******************")
    print("1. Admin")
    print("2. User")
    print("3. Exit")
    x = int(input("Choose an option: "))
    while True:
        if x == 1:
            admin()
        elif x == 2:
            user()
        else:
            print("************ PLEASE CHOOSE A CORRECT OPTION ******************")
            menu1()
        break

menu1()

if __name__ == "__main__":
    main()

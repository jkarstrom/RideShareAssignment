from helper import helper
from db_operations import db_operations
# python app.py

db_ops = db_operations()

#start screen
def startScreen():
    print("Welcome to the ride share app!")

#If user is new or returning
def options():
    print('''Are you a new user or returning user?: 
    1. New User
    2. Returning User''')
    return helper.get_choice([1,2])

#creates new user
def createNewUser():
    print('''What kind of user are you?
    1. Rider
    2. Driver
    ''')
    user_choice = helper.get_choice([1,2])
    # User is a driver
    if user_choice == 1:
        count_query = '''
        SELECT COUNT(DISTINCT driverID)
        FROM Drivers
        '''
        driver_count = db_ops.single_record(count_query)
        userID = "d"+str(driver_count + 1)
        # Ask user whether they are currently accepting rides or not
        print('''Are you currently able to drive and are accepting ride requests?
        1 - Yes
        0 - No
        ''')
        availability = helper.get_choice([1,0])
        insert_query = "INSERT INTO Drivers VALUES(?,?,?)"
        if availability == 1:
            driver_data = [userID, "0.0", "Active"]
        else:
            driver_data = [userID, "0.0", "Inactive"]
        # Add driver to the database
        db_ops.update_table(insert_query, driver_data)
        print("Your driverID is: ", userID, ". Make sure to remember this!")

    # User is a rider
    else:
        count_query = '''
        SELECT COUNT(DISTINCT riderID)
        FROM Riders
        '''
        rider_count = db_ops.single_record(count_query)
        userID = "r"+str(rider_count + 1)
        insert_query = "INSERT INTO Riders VALUES(?)"
        rider_data = [userID]
        # Add rider to the database
        db_ops.update_table(insert_query, rider_data)
        print("Your riderID is: ", userID, ". Make sure to remember this!")
    # Return to the main menu

# Finds if the returning user is a rider or driver
def returningUser():
    user_type = -1
    while user_type == -1:
        curUser = input("What is your userID?")
        if len(curUser) > 22:
                print("User ID is longer than any currently existing ID. Try again.")
                continue
        # Using userID find if user is rider or driver then call either userDriver() or userRider()
        # Query to check if inputted ID exists in Drivers table
        driver_check_query = '''
            SELECT COUNT(*)
            FROM Drivers
            WHERE riderID := '%s'
        '''
        driver_result = db_ops.single_record(driver_check_query % curUser)
        if driver_result != 0:
            user_type = 0
            break

        # Query to check if inputted ID exists in Riders table
        rider_check_query = '''
            SELECT COUNT(*)
            FROM Drivers
            WHERE riderID := '%s'
        '''
        rider_result = db_ops.single_record(rider_check_query % curUser)
        if rider_result != 0:
            user_type = 1
            break

        if driver_result == 0 and rider_result == 0:
            print("User ID could not be found from Driver and Rider tables. Try again.")
            continue

    # Once user type has been found, bring the user to their appropriate menu.
    if user_type == 0:
        userDriver(curUser)
    if user_type == 1:
        userRider(curUser)



#options for driver users
def userDriver(userID):
    while True:
        print('''What would you like to do?: 
        1. View Rating
        2. View Rides
        3. Activate/Deactivate Driver Mode
        4. Quit''')
        user_choice = helper.get_choice([1,2,3,4])
        # User views their rating
        if user_choice == 1: #viewing rating
            query = "SELECT "
        if user_choice == 2:#view rides
            query = "SELECT "
        if user_choice == 3: #activate or deactivate Driver Mode
            query = " " #updates the record if they are receving rides or not
        if user_choice == 4:
            break

#options for rider users 
def userRider(userID):
    while True:
        print('''What would you like to do?: 
        1. View Rides
        2. Find a Driver
        3. Rate my driver
        4. Quit''')
        user_choice = helper.get_choice([1,2,3,4])
        if user_choice == 1: #viewing rides
            query = "SELECT " #prints out rider's rides
        if user_choice == 2: #finds a driver
            pickUp = input("What is the pickup location?")
            dropOff = input("What is the dropoff location?")
            query = " " #Creates a new ride and prints the riderID
            #send back to menu
        if user_choice == 3: #rating the last driver
            query = "SELECT " #looking up riders last ride and return their Driver's ID
            #print ride information and ask if it is correct
                #if not correct ask them to enter the rideID of the ride
            #calculate driver's new rating
        if user_choice == 4:
            break
        
#main program
startScreen()

#main program loop
while True:
    user_choice = options()
    if user_choice == 1: #new user
        createNewUser()
    if user_choice == 2: #returning user
        returningUser()
    if user_choice == 3:
        print("Goodbye!")
        break

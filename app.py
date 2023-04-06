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
            rating_query = '''
            SELECT driverRating
            FROM Drivers
            WHERE driverID = '%s'
            '''
            rating = db_ops.single_record(rating_query % userID)
            print("Your current driver rating is: ", rating)
        if user_choice == 2:#view rides
            ride_query = '''
            SELECT *
            FROM Rides
            WHERE driverID :=driver
            '''
            dictionary = {"driver":userID}
            results = db_ops.name_placeholder_query(ride_query, dictionary)
            helper.pretty_print(results)
        if user_choice == 3: #activate or deactivate Driver Mode
            print('''Are you currently accepting rides?
            1 - Yes
            0 - No
            ''')
            user_choice = helper.get_choice([1,0])
            if user_choice == 1:
                status = "Active"
            else:
                status = "Inactive"
            
            update_query = '''
            UPDATE Drivers
            SET driverMode = ?
            WHERE driverID = ?
            ''' #updates the record if they are receving rides or not

            new_data = [(status, userID)]
            db_ops.update_table(update_query, new_data)
            
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
            ride_query = '''
            SELECT *
            FROM Rides
            WHERE riderID := rider
            ''' #prints out rider's rides
            dictionary = {"rider":userID}
            results = db_ops.name_placeholder_query(ride_query, dictionary)
            helper.pretty_print(results)

        if user_choice == 2: #finds a driver
            pickUp = input("What is the pickup location?")
            dropOff = input("What is the dropoff location?")
            # Randomly select an available driver
            driver_query = '''
            SELECT driverID
            FROM Drivers
            WHERE driverMode = "Active"
            ORDER BY RANDOM()
            '''
            driver_id = db_ops.single_record(driver_query)
            print("Your driver's ID is: ", driver_id)

            # Generate an ID for the ride itself
            count_query = '''
            SELECT COUNT(DISTINCT driveID)
            FROM Rides
            '''
            ride_count = db_ops.single_record(count_query)
            rideID = "rd"+str(ride_count + 1)
            print("Your ride's ID is: ", rideID)

            # Add new ride instance to Ride Table
            insert_query = "INSERT INTO Drivers VALUES(?,?,?,?,?)"
            ride_data = [rideID, driver_id, userID, pickUp, dropOff]
            db_ops.update_table(insert_query, ride_data)

        if user_choice == 3: #rating the last driver
            ride_driver_query = '''
            SELECT driverID
            FROM Rides
            WHERE riderID = '%s'
            ORDER BY rideID DESC
            ''' #looking up riders last ride and return their Driver's ID
            driver_id = db_ops.single_record(ride_driver_query % userID)
            # Obtain the ride information for printing and verifying with user
            ride_query = '''
            SELECT *
            FROM Rides
            WHERE riderID = '%s'
            ORDER BY rideID DESC
            '''
            ride_info = db_ops.single_tuple(ride_query % userID)
            #print ride information and ask if it is correct
            helper.pretty_print(ride_info)
            print('''Is the information about your last ride correct?
            1 - Yes
            0 - No
            ''')
            ride_accuracy = helper.get_choice([1,0])
            #if not correct ask them to enter the rideID of the ride
            if ride_accuracy == 0:
                correction = False
                while correction == False:
                    corrected_ride_id = input("Please input the correct ID of your last ride: ")
                    if len(corrected_ride_id) > 22:
                        print("Provided ride ID is longer than any currently existing ID. Try again.")
                        continue

                    # Check if ride actually exists
                    ride_check_query = '''
                    SELECT COUNT(*)
                    FROM Rides
                    WHERE rideID := '%s'
                    '''
                    driver_result = db_ops.single_record(ride_check_query % corrected_ride_id)
                    if driver_result == 0:
                        print("The ride with the provided ride ID could not be found. Please try again.")
                        continue
                    
                    # Ride exists
                    corrected_ride_driver_query = '''
                    SELECT driverID
                    FROM Rides
                    WHERE rideID = '%s'
                    ORDER BY rideID DESC
                    ''' #looking up riders last ride and return their Driver's ID
                    driver_id = db_ops.single_record(corrected_ride_driver_query % corrected_ride_id)
                    # Obtain the ride information for printing and verifying with user
                    corrected_ride_query = '''
                    SELECT *
                    FROM Rides
                    WHERE rideID = '%s'
                    ORDER BY rideID DESC
                    '''
                    corrected_ride_info = db_ops.single_tuple(corrected_ride_query % corrected_ride_id)
                    #print ride information and ask if it is correct
                    helper.pretty_print(corrected_ride_info)
                    print('''Is the information about your last ride correct?
                    1 - Yes
                    0 - No
                    ''')
                    new_ride_accuracy = helper.get_choice([1,0])
                    # Information is correct, proceed
                    if new_ride_accuracy == 1:
                        correction = True
                        break
                    # Information is incorrect, go back
                    else:
                        print("Returning to asking for ride ID...")
                        continue
            
            rating_set = False
            while rating_set == False:
                rating = input("Please insert a number between 0.0 and 5.0: ")
                # Attempt to convert the user's input into a float
                try:
                    float(rating)
                except ValueError:
                    print("A non-float number was provided. Please try again.")
                    continue
                
                # Check if user's input is between 0 and 5
                if float(rating) <= 5.0 and float(rating) >= 0.0:
                    rating_set = True
                    break
                else:
                    print("Error. Rating exceeds limit. Please try again.")
                    continue
            #calculate driver's new rating
            # Obtain initial rating from driver
            rating_query = '''
            SELECT driverRating
            FROM Drivers
            WHERE driverID = '%s'
            '''
            currRating = db_ops.single_record(rating_query % driver_id)
            update_query = '''
            UPDATE Drivers
            SET driverRating = ?
            WHERE driverID = ?
            '''
            # If the driver currently has no ratings (0.0 by default)
            if (float(currRating) == 0.0):
                update_data = [rating, driver_id]

            # Driver currently has a rating
            else:
                new_rating = float((float(currRating) + float(rating)) / float(2.0))
                update_data = [new_rating, driver_id]
            
            # Update driver's rating
            db_ops.update_table(update_query, update_data)
                
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

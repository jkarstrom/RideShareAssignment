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
    if user_choice == 1:
        id_set = False
        while id_set == False:
            userID = input("Please input a unique ID: ")
            check_query = '''
            SELECT COUNT(*)
            FROM Drivers
            WHERE riderID := '%s'
            '''
            result = db_ops.single_record(check_query % userID)
            if result == 0:
                id_set = True
                break
            if result != 0:
                print("Id already exists within driver database. Try again.")
    query = "" #creates a new instance of a user
    #return to the main menu

#finds if the returning user is a rider or driver
def returningUser():
    curUser = input("What is your userID?")
    #using userID find if user is rider or driver then call either userDriver() or userRider()
    id_query = '''
    '''

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

from helper import helper
from db_operations import db_operations
#python app.py


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
    query = "" #creates a new instance of a user
    #return to the main menu

#finds if the returning user is a rider or driver
def returningUser():
    curUser = input("What is your userID?")
    query = "" #using userID find if user is rider or driver then call either userDriver() or userRider()

#options for driver users
def userDriver():
    print('''What would you like to do?: 
    1. View Rating
    2. View Rides
    3. Activate/Deactivate Driver Mode''')
    if helper.get_choice([1,2,3]) == 1: #viewing rating
        query = "SELECT "
    elif helper.get_choice([1,2,3]) == 2:#view rides
        query = "SELECT "
    else: #activate or deactivate Driver Mode
        query = " " #updates the record if they are receving rides or not

#options for rider users 
def userRider():
    print('''What would you like to do?: 
    1. View Rides
    2. Find a Driver
    3. Rate my driver''')
    if helper.get_choice([1,2,3]) == 1: #viewing rides
        query = "SELECT " #prints out rider's rides
    elif helper.get_choice([1,2,3]) == 2: #finds a driver
        pickUp = input("What is the pickup location?")
        dropOff = input("What is the dropoff location?")
        query = " " #Creates a new ride and prints the riderID
        #send back to menu
    else: #rating the last driver
        query = "SELECT " #looking up riders last ride and return their Driver's ID
        #print ride information and ask if it is correct
            #if not correct ask them to enter the rideID of the ride
        #calculate driver's new rating
        
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

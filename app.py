from helper import helper
from db_operations import db_operations
#python app.py


#start screen
def startScreen():
    print("Welcome to the ride share app!")

#creates new user
def createNewUser():
    query = ""

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

#options for rider users 
def userDriver():
    print('''What would you like to do?: 
    1. View Rating
    2. View Rides
    3. Activate/Deactivate Driver Mode''')
    if helper.get_choice([1,2,3]) == 1: #viewing rating
        query = "SELECT "
    elif helper.get_choice([1,2,3]) == 2: #view rides
        query = "SELECT "
    else: #changes driver mode to opposite mode
        query = "SELECT "

#If user is new or returning
def options():
    print('''Are you a new user or returning user?: 
    1. New User
    2. Returning User''')
    return helper.get_choice([1,2])
    

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

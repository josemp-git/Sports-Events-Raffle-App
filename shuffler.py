from csv import writer, reader
from random import shuffle, choices
from itertools import cycle
from sys import stdout
from time import sleep
from termcolor import colored
from argparse import ArgumentParser
from os import path
from string import ascii_letters, digits
import datetime

# Length of the pause in seconds, when the pause feature is enabled. For example, if pause_time = 3, there will be a 3-second pause between the pairing of each team and player when results are being displayed.
pause_time = 3

# Max retries for the enable pause feature
max_pause_retries = 5

# Max retries to open the data file
max_open_file_retries = 5

# Necessary headers for the data file. It is not case sensitive
headers = ['TEAMS', 'PLAYERS']

# The headers for the results file
results_headers = ['NUMBER', 'TEAMS', 'PLAYERS']

# Creates two empty lists out of the data file
teams = []
players = []

# This function is executed when a data file is not passed as an argument
def inputfile():        
    open_file_retries = 0
    global manualdatafile
    while True:
        # Prompts the user to enter the name of the data file
        manualdatafile = input("\nEnter the name of the file to open: ")
        # Validates again if this new file exists
        if not path.exists(manualdatafile) and open_file_retries < max_open_file_retries:
            open_file_retries = open_file_retries + 1
            # If you fail 'max_open_file_retries' times trying to enter the data file name, the app will close
            if open_file_retries == max_open_file_retries:
                print(colored("\n\033[1mFile not found.\033[0m",color="red"),"You have reached the maximum number of attempts ("+str(max_open_file_retries)+"). The application will now close.\n")
                quit()
            else:
                print(colored("\n\033[1mFile not found.\033[0m",color="red"), "Try again.")
        else:
            break

# The command-line arguments that the app accepts
parser = ArgumentParser()
parser.add_argument("--file", help="Name of the CSV file that contains the names of TEAMS and PLAYERS.")
parser.add_argument("--event", help="Name of the event. If provided, it will be used to name the output file with the results.")
parser.add_argument("--pause", help="Inserts some pauses during the execution. Valid values: 'yes' or 'no' (y,n)")

# Parses the command-line arguments
args = parser.parse_args()

# Accesses the arguments using the attribute names specified in add_argument()
datafile = args.file
event = args.event
pause_enabled = args.pause

# Name of your CSV file that contains the names of teams and players. If you do not specify a file name or if the file name is incorrect, the app will ask you to provide the name of the file.
# Make sure that your CSV file has the header TEAMS,PLAYERS in the first row.
# If the file name is not provided, it executes the inputfile() function
if datafile == None:
    inputfile()
    datafile = manualdatafile
# If the file name is provided, it validates that file exists. If it does not exist, it executes the inputfile() function
elif datafile != None and not path.exists(datafile):
    print(colored("\n\033[1mThe file specified in the argument was not found.\033[0m",color="red"))
    inputfile()
    datafile = manualdatafile
else:
    pass

# Opens the data file in read mode
with open(datafile, 'r', encoding="utf-8-sig") as file:
    # Reads the first row (the headers), headers are removed to not count these as part of the raffle
    found_headers = file.readline().strip().split(',')
    # Compares the found header with the the expected headers are part of the file. If the correct headers are not there, the app will show an error message and close
    if [x.lower() for x in found_headers] == [x.lower() for x in headers]:
        pass
    else:
        # If headers are wrong the app will close 
        print("\nThe CSV file does not have the expected headers:\n")
        print(*headers, sep = ',')
        print("\nFix this and try again.\n")
        quit()
    # Read the file as a CSV reader
    filereader = reader(file)
    # Iterate over the rows in the CSV file
    for row in filereader:
        # The first value in the row goes to the first list (teams)
        teams.append(row[0])
        # The second value in the row goes to the second list (players)
        players.append(row[1])

### PAUSE FEATURE ### - This feature inserts pauses during the execution, specially when teams and players are paired as the results are displayed, adding more excitement and suspense to the game.
# Valid values to enable the PAUSE feature (not case sensitive)
pause_answers = ["yes","y","no","n"]
if pause_enabled != None and pause_enabled.lower() in pause_answers:
    pause_enabled = pause_enabled.lower()
else:
    pause_retries = 0
    while True:
    # If no value or an invalid value is provided, it will prompot the user to enable or disable the PAUSE feature
        pause_retries = pause_retries +1
        ask_for_pause = input("\nDo you want to enable the pause feature for the display of the results?\nPlease enter 'yes' or 'no' (y/n): ")
        if ask_for_pause.lower() == "yes" or ask_for_pause.lower() == "y":
            pause_enabled = "yes"
            print("\nPause feature has been \033[1mENABLED\033[0m.\n")
            sleep(0.666)
            break
        elif ask_for_pause.lower() == "no" or ask_for_pause.lower() == "n":
            pause_enabled = "no"
            print("\nPause feature has been \033[1mDISABLED\033[0m.\n")
            sleep(0.666)
            break         
        if pause_retries == max_pause_retries:
            # If you fail 'max_retries_pause' times to enter the right answer, the app will close.
            print(colored("\n\033[1mInvalid answer.\033[0m",color="red"),"You have reached the maximum number of attempts ("+str(max_pause_retries)+"). The application will now close.\n")
            quit()
        else:
            print(colored("\n\033[1mInvalid answer.\033[0m",color="red"),"Try again.")

# Gets the current date and time - these are added to the results file
now = datetime.datetime.now()

# Generates two random characters that are added as a suffix of the results file
random_chars = ''.join(choices(ascii_letters + digits, k=2))

# If the event parameter is not provided, the results file will have the 'results' prefix in its name
if event == None:
    # Creates the file name by combining the word 'results', date, time, and random characters
    resultsfile = "{}_{}_{}_{}_{}_{}_{}.csv".format("results", now.year, now.month, now.day, now.hour, now.minute, random_chars)
#if the event parameter is provided, it will be used as a prefix for the results file name
else:
    # Creates the file name by combining the event attribute, date, time, and random characters
    resultsfile = "{}_{}_{}_{}_{}_{}_{}.csv".format(event, now.year, now.month, now.day, now.hour, now.minute, random_chars)

# Uses the filter() function to filter out any empty values in the lists
teams = list(filter(None, teams))
players = list(filter(None, players))

# Calculates the length of the lists once these have been filtered out of empyt values
lengthteams = len(teams)
lengthplayers = len(players)

# Validates the number of teams and players. If the number of players is larger than the number of teams, the program displays an error message and is closed.
if lengthteams < lengthplayers:
    print(colored("\n\033[1mINVALID DATA SET\033[0m",color="red"),"\nThe number of players must not exceed the number of teams.\nFix this and try again.\n")
    quit()
else:
    # Sorts lists in alphabetical order to display them next
    teams.sort()
    players.sort()

    # Welcome message
    print("\n\033[1mWelcome to the Sports Events Raffle Application!\033[0m\n")
    print("This application enables you to run raffles for sports events and randomly pair teams with players.\n")
    print("\033[1mGood luck and have fun!\n\033[0m")
    if pause_enabled == "yes" or pause_enabled == "y":
        user_input = input("Press ENTER to continue.\n")
    else:
        pass
    # Prints the two lists (TEAMS on the left side, and PLAYERS on the right side, in alphabetical order)
    print("These are the teams and players found in the CSV file:\n")
    print("|▔▔▔▔▔▔|▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔|▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔|")
    print("|\033[1m{:^6}\033[0m|\033[1m{:^30}\033[0m|\033[1m{:^30}\033[0m|".format("#","TEAMS","PLAYERS"))
    print("|______|______________________________|______________________________|")
    print("|{:^6}|{:^30}|{:^30}|".format("","",""))
    teamnumber = 1
    for i in range(lengthteams):
        item1 = teams[i] if i < lengthteams else ""
        item2 = players[i] if i < lengthplayers else ""
        print("|{:^6}|{:^30}|{:^30}|".format(teamnumber,item1, item2))
        # An identification number is added to every TEAM on the left side
        teamnumber = teamnumber + 1
    print("|______|______________________________|______________________________|")

# Calculates how many teams per player
teamsperplayer=lengthteams//lengthplayers

# Validates if the number of players and teams is the same. Displays number of TEAMS and PLAYERS
if lengthteams == lengthplayers:
    print("\nThere are", lengthteams, "teams and", lengthplayers, "players.\nEach player will have", teamsperplayer, "team(s).\n")
else:
    # If there are less players than teams, the players lists is shuffled and iterated to repeate players in the players lists, until both lists are the same length

    # It shuffles the players for the first time. This is useful in case that the teams cannof be divided equally among the players. This is explained ahead
    shuffle(players)

    # Uses the itertools.cycle() function to repeat the values in the PLAYERS list
    list2_iterator = cycle(players)

    # Creates a new PLAYERS list by repeating the values from the PLAYERS list until it has the same length as the TEAMS list
    players = [next(list2_iterator) for i in range(lengthteams)]
    
    # The number of players can be divided equally among the number of teams. Each player will receive the same number of teams
    if lengthteams % lengthplayers == 0:
        print("\n")
        print("There are", lengthteams, "teams and", lengthplayers, "players.\nEach player will have", teamsperplayer, "team(s).\n")
    # If the number of teams cannot be divided equally among the number of players, the following will do the necessary calculations and randomly will provide one extra team to a determined number of lucky players.
    elif lengthteams % lengthplayers != 0:
        playerdiff=(lengthteams % lengthplayers)
        teamdiff=(teamsperplayer+1)
        regularplayers=(lengthplayers-playerdiff)
        print("\n")
        print("There are", lengthteams, "teams and", lengthplayers, "players.")
        print(regularplayers, "player(s) will have", teamsperplayer, "team(s), and", playerdiff, "lucky player(s) will have", teamdiff, "teams.\n")

# This is only executed if the pause feature is enabled
if pause_enabled == "yes" or pause_enabled == "y":
    user_input = input("\033[1mPress ENTER to start the raffle!\033[0m\n")
    print_time = 0.25
    def delay_print(s):
        for c in s:
            stdout.write(c)
            stdout.flush()
            sleep(print_time)

    delay_print("3... 2... 1... ")
    print("\033[1mGO!\n\033[0m")
    sleep(1)
else:
    pass

# It shuffles the lists of TEAMS and PLAYERS
shuffle(teams)
shuffle(players)

# Uses the zip() function to combine the now shuffled lists into a dictionary
dictionary = dict(zip(teams, players))

# Opens the CSV file in write mode
with open(resultsfile, "w", encoding="utf-8-sig") as file:
    # Createw a CSV writer object
    writer = writer(file)
    writer.writerow(results_headers)
    print("|▔▔▔▔▔▔|▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔|▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔|")
    print("|\033[1m{:^6}\033[0m|\033[1m{:^30}\033[0m|\033[1m{:^30}\033[0m|".format("#","TEAMS","PLAYERS"))
    print("|______|______________________________|______________________________|")
    print("|{:^6}|{:^30}|{:^30}|".format("","",""))
    sleep(0.666)
    teamnumber = 1
    # The time it will take to print each one of the characters when the name of the player is revealed
    print_time = 0.008
    for key, value in dictionary.items():
        if pause_enabled == "yes" or pause_enabled == "y":
            print("|{:^6}|{:^30}= ".format(teamnumber,key), end="",flush=True)
            sleep(pause_time)
            delay_print("{:^29}|\n".format(value))
        else:
            print("|{:^6}|{:^30}={:^30}|".format(teamnumber,key,value))
        # Results are written to a CSV file
        writer.writerow([teamnumber, key, value])
        teamnumber = teamnumber + 1
print("|______|______________________________|______________________________|\n")
print ("Results were written to file: \033[1m\033[4m"+resultsfile+"\033[0m\n")
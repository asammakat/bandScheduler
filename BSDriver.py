import csv
import datetime
from BSClasses import Player, Band
from BSFunctions import (
    update_csv,
    load_availability,
    print_band_members,
    format_date_text,
    display_availability,
    display_band_availability,
    delete_availability,
    add_availability,
    deal_with_zeros
    )

def main():
    band_member_list = [] #List of Player oblects
    band_member = None

    print("Welcome to band scheduler!\n")

    band_from_file = open("KTLRoster.txt") #TODO switch to with
    for i in band_from_file:
        name = ""
        for char in i:
            if char != "\n":
                name += char
        band_member_list.append(Player(name))
    band_from_file.close()

    band = Band(band_member_list)

    #Display band for user
    print_band_members(band)

    print("\nWho are you? (choose a number)")
    
    band_member = band_member_list[int(input()) -1]
    
    #loads each band member with their current availability
    load_availability(band_member_list)

    #remove davailability dates that have passed
    band.remove_old_dates()

    #load group availability
    group_availability = [band.find_dates_in_common()]#TODOseems odd dbl check
    
    #display availability
    print("\n")
    print("\nCurrent band availability is: \n" )
    display_band_availability(band)
    print("\n")#newline after displaying band_availability

    #display group availability
    if len(group_availability) == 0:
        print("There are currently no dates where everyone is available")
    else:
        print("Current group availability is: ")
        for date in group_availability:
            display_availability(date)

    user_input = 0
    while(True):
        #menu options
        print("What you like to do? \n\n"
               "    Press 1 to add availability.\n"
               "    Press 2 to delete availability\n"
               "    Press 3 to see all availability\n"
               "    Press 4 to see your availability\n"
               "    Press 5 to see availability in common\n"              
               "    Enter -1 to exit")
        user_input = int(input())

        if user_input == 1:
            availability = add_availability(band_member)
            display_availability(band_member.get_availability())
        elif user_input == 2: 
            delete_availability(band_member)
        elif user_input == 3:
            display_band_availability(band)
        elif user_input == 4:            
            display_availability(band_member.get_availability())
        elif user_input == 5:
            print("Current group availability is: ")
            display_availability(band.find_dates_in_common())
        elif user_input == -1:
            update_csv(band.get_roster())
            print("goodbye")
            break
        else:
            print("I'm sorry I didn't understand you")

main()

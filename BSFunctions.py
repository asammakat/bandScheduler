import csv
import datetime
  
            
def update_csv(band_member_list):
    
    #store all dates for all band members
    availability = []
    
    #get all availability dates and add them to availability
    for member in band_member_list:
        for date in member.get_availability():
            availability.append(date)
    
    #update csv        
    with open("KTLschedule.txt", mode='w') as schedule:
        schedule_writer = csv.writer(schedule, delimiter=',')
        schedule_writer.writerow(["name", "year", "month", "day",
                          "startHour", "startMinute", "endHour",
                          "endMinute"])
        for date in availability:
            schedule_writer.writerow(date)
####################################################################################

def load_availability(band_member_list):
    #Store availability from csv
    availability = []

    #read from csv file into availability
    with open("KTLschedule.txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                availability.append(row)
            line_count = line_count + 1

    availability = deal_with_zeros(availability)

    #add availability to player objects
    for player in band_member_list:
        name = player.get_name().lower()
        for date in availability:
            if name == date[0]:# means date corresponds to player
                player.add_availability(date)
#################################################################################
###################### Text and display helper functions ########################
           
def print_band_members(band):
    for member in enumerate(band.get_roster()):
        print(member[0]+1, ": ", member[1].get_name(), sep = "")
#--------------------------------------------------------------------------------
            
def format_date_text(date):
    #return "mm/dd/yy from <start time> to <endtime>"
    formatted_string = "{}/{}/{} from {}:{} to {}:{}".format(date[2],date[3],
                                                              date[1],date[4],
                                                              date[5], date[6],
                                                              date[7])
    return formatted_string
#--------------------------------------------------------------------------------

def display_availability(dates):
    for date in dates:
        print("\t", format_date_text(date))
    print("\n")
#--------------------------------------------------------------------------------

def display_band_availability(band):
    for member in band.get_roster():
        print(member.get_name(), "-"*40)
        for date in member.get_availability():
            print("\t", format_date_text(date))

def deal_with_zeros(dates):
    #deal with 0, convert to 00
    for date in range(len(dates)):
        for item in range(len(dates[date])):
            if dates[date][item] == '0':
                dates[date][item] = "00"
    return dates

            
#################################################################################

#Menu option 2
def delete_availability(band_member):
    while(True):
        band_member.enumerate_availability()
        print("Which date would you like to delete?(enter a number)")
        user_input = int(input()) - 1
        band_member.delete_availability(user_input)
        print("Deleting item...")
        print("Would you like to delete another? y/n")
        add_another = input()
        if add_another != "y":
            break
#################################################################################

#Menu option 1
def add_availability(band_member):
    #name, year, month, day, startHour, startMinute, endHour, endMinute
    while(True):
        new_entry = []
        new_entry.append(band_member.get_name().lower())
        
        #Get day
        print("On what day are you available? (mm/dd/yyyy)")
        date = input()
        date = date.split("/")
        new_entry.append(date[2])
        new_entry.append(date[0])
        new_entry.append(date[1])
        
        #get start time
        print("What time does your availability start? (hh:mm)", end = " ")
        print("followed by 'a' for am or 'p' for pm") #TODO impliment 'a' or 'p feature'
        start_time = input()
        start_time = start_time.split(":")
        new_entry.append(start_time[0])
        new_entry.append(start_time[1])
        
        #get end time
        print("What time does your availability end: (hh:mm)")
        end_time = input()
        end_time = end_time.split(":")
        new_entry.append(end_time[0])
        new_entry.append(end_time[1])
        
        #TODO Error check user input
        #TODO Impliment user inputing a or p for am / pm

        print("You are available on %s/%s/%s from %s:%s to %s:%s\n"
                                        %(new_entry[2], new_entry[3],
                                         new_entry[1], new_entry[4],
                                         new_entry[5], new_entry[6],
                                         new_entry[7]))
        #confirm date is correct
        print("Is this correct?")
        confirm = input()
        if confirm == "y":
            band_member.add_availability(new_entry)
            
        #Check if user is done        
        print("Would you like to add another time? y/n")
        add_another = input()
        if add_another != "y":
            break
#################################################################################

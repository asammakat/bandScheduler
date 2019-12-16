import datetime
import csv

#################################################################################

class Band:
    def __init__(self, roster):
        self.roster = roster
        self.band_availability = [] #Dates available for all players in band

    #getters
    def get_roster(self):
        return self.roster
    def get_avaliability(self):
        return self.availability

    #setters
    def add_to_roster(self, name):
        self.roster.append(name)
    def add_availability(self, date):
        self.availability.append(date)

    def remove_old_dates(self):
        #csv: name, year, month, day, startHour, startMinute, endHour, endMinute
        #for datetime: year, month, day[,hour,minute,second,mocrosecond,tzinfo]
        for member in self.roster:
            for date in enumerate(member.get_availability()):
                member_date = date[1]
                endtime = datetime.datetime(int(member_date[1]),
                                            int(member_date[2]),
                                            int(member_date[3]),
                                            int(member_date[6]),
                                            int(member_date[7]))
                if endtime < datetime.datetime.now():
                    #delete_availability uses index so use date[0]
                    member.delete_availability(date[0])

    def find_dates_in_common(self):
        #csv: name, year, month, day, startHour, startMinute, endHour, endMinute
        #for datetime: year, month, day[,hour,minute,second,mocrosecond,tzinfo]
        dates_in_common = [];

        #go through dates for first member in band.roster
        for date in self.roster[0].get_availability():
            #flag used to determine if a start/endtime sholud be appended to dates_in_common
            green_light = True 

            #start time for first member as dt obj, gets adjusted
            #according to availability of other members
            start_time = datetime.datetime( 
                int(date[1]),int(date[2]),
                int(date[3]),int(date[4]),
                int(date[5])
                )
            
            #end for first member as dt obj, gets adjusted
            #according to availability of other members
            end_time = datetime.datetime(
                int(date[1]),int(date[2]),
                int(date[3]),int(date[6]),
                int(date[7])
                )
                     
            for member in self.roster[1:]: #go through the rest of band.roster
                #flag to determine if a change has been made to start_time or end_time
                change_made = False
                #go through member's availability
                for member_date in member.get_availability():

                    #start time for member as dt obj
                    member_start_time = datetime.datetime(
                        int(member_date[1]),int(member_date[2]),
                        int(member_date[3]),int(member_date[4]),
                        int(member_date[5])
                        )

                    #end time for member as dt obj
                    member_end_time = datetime.datetime(
                        int(member_date[1]),int(member_date[2]),
                        int(member_date[3]),int(member_date[6]),
                        int(member_date[7])
                        )

                    # If member start time is in the desired window
                    #change start time outside of this loop
                    if (member_start_time >= start_time) and (member_start_time < end_time):
                        start_time = member_start_time
                        change_made = True 

                    #If member end time is in the desired window
                    #change end time outside of this loop
                    if(member_end_time > start_time) and (member_end_time <= end_time):
                        end_time = member_end_time                           
                        change_made = True

                #if no change made we know the date in incompatable
                if change_made == False:  
                    green_light = False
                    break #Current date is incompatable so move on to the next

            if green_light == True: #current date is compatable
                dates_in_common.append(["Everybody", str(start_time.year),
                                        str(start_time.month), str(start_time.day),
                                        str(start_time.hour), str(start_time.minute),
                                        str(end_time.hour), str(end_time.minute)])

        return dates_in_common #[[st1,et1],[st2,et2], ... ]
            
                
#################################################################################

class Player:
    def __init__(self, name):
        self.name = name 
        self.availability = [] #Dates available for player         

    #getters     
    def get_name(self):
        return self.name   
    def get_availability(self):
        return self.availability

    #setters
    def set_name(self, name):
        self.name = name
        
    #adds availability one entry at a time
    def add_availability(self, date):
        self.availability.append(date)
        
    #delete an item from self.availability according to its index
    def delete_availability(self, index):
        del self.availability[index]
        
    #enumerate availability
    def enumerate_availability(self):
        for i in range(len(self.availability)):
            print(i+1, ": ", format_date_text(self.availability[i]), sep = "")
#################################################################################

def remove_old_dates(band):
    #in csv: name, year, month, day, startHour, startMinute, endHour, endMinute
    #for datetime: year, month, day[,hour,minute,second,mocrosecond,tzinfo]
    for member in band.get_roster():
        for date in enumerate(member.get_availability()):
            member_date = date[1]
            endtime = datetime.datetime(int(member_date[1]),
                                        int(member_date[2]),
                                        int(member_date[3]),
                                        int(member_date[6]),
                                        int(member_date[7]))
            if endtime < datetime.datetime.now():
                #delete_availability uses index so use date[0]
                member.delete_availability(date[0])
#################################################################################    
            
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

##        #deal with 0, convert to 00
##        for date in range(len(availability)):
##            for item in range(len(availability[date])):
##                if availability[date][item] == '0':
##                    availability[date][item] = "00"

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
                print("HIT!")
                dates[date][item] = "00"
    print(dates)
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
    group_availability = [band.find_dates_in_common()]
    group_availability = deal_with_zeros(group_availability)
    
    #display availability
    print("\n")
    print("Your availability is: \n" )
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

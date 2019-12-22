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
           
def print_band_members(band):#TODO Make band member function?
    for member in enumerate(band.get_roster()):
        print(member[0]+1, ": ", member[1].get_name(), sep = "")
#--------------------------------------------------------------------------------
            
def format_date_text(date):
    #return "mm/dd/yy from <start time> to <endtime>"
    #name, year, month, day, startHour, startMinute, stpm, endHour, endMinute, etpm
    
    start_time = rev_am_pm_conversion(date[4],date[5])
    end_time = rev_am_pm_conversion(date[6],date[7])
    
    formatted_string = "{}/{}/{} from {} to {}".format(date[2],date[3],date[1],
                                                       start_time,end_time)
    return formatted_string
#--------------------------------------------------------------------------------

def display_availability(dates):
    for date in dates:
        print("\t", format_date_text(date))
    print("\n")
#--------------------------------------------------------------------------------

def display_band_availability(band):#TODO Make band member funcion?
    for member in band.get_roster():
        print(member.get_name(), "-"*40)
        for date in member.get_availability():
            print("\t", format_date_text(date))
#--------------------------------------------------------------------------------

def deal_with_zeros(dates):
    #deal with 0, convert to 00
    for date in range(len(dates)):
        for item in range(len(dates[date])):
            if dates[date][item] == '0':
                dates[date][item] = "00"
    return dates
#--------------------------------------------------------------------------------

def am_pm_conversion(time):
    #time is [hh:mmp] or [hh:mma]
    if time[1][-1] == "p":
        time[1] = time[1][:-1] #get rid of a/p char
        #only make adjustment from 1:00 pm - 11:59pm
        if time[0] != "12":           
            time[0] = str(int(time[0]) + 12) 
            
    else:
        time[1] = time[1][:-1]
        #make adjustment from 12:00am - 12:59am
        if time[0] == "12":
            time[0] = "00"  
    return time
#--------------------------------------------------------------------------------

def rev_am_pm_conversion(hour, minute):
    #take a start or end time with am/pm informaton 
    #and conver to formatted string in "hh:mm am/pm" format.

    if int(hour) >= 12:
        if hour != "12":
            result = "{}:{}pm".format(str(int(hour) - 12), minute)
        else:
            result = "{}:{}pm".format(hour, minute)

    else:
        if hour == "00":
            result = "{}:{}am".format(str(int(hour) + 12), minute)
        else:
            result =  "{}:{}am".format(hour, minute)

    return result
    
                   
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
        #Check that entry is valid format
        try:
            new_entry.append(date[2])
            new_entry.append(date[0])
            new_entry.append(date[1])
        except:
            print("Invalid entry for year please try again.")
            continue
            
        #get start time from user
        print("What time does your availability start? (hh:mm)", end = " ")
        print("followed by 'a' for am or 'p' for pm") 
        start_time = input()
        start_time = start_time.split(":")
        #check that entry is valid format
        try:
            start_time = am_pm_conversion(start_time)
        except:
            print("Invalid entry for start time. Please try again")
            continue

        #append start time             
        for i in start_time:
            new_entry.append(i)
        
        #get end time from user
        print("What time does your availability end: (hh:mm)")
        print("followed by 'a' for am or 'p' for pm") 
        end_time = input()
        end_time = end_time.split(":")
        #check that entry is valid format
        try:
            end_time = am_pm_conversion(end_time)
        except:
            print("Invalid entry for end time. Please try again")
            continue            

        #append end time
        for i in end_time:
            new_entry.append(i)
        
        #Error check user input by testing that datetime objects can be made with them
        try:
            st_as_dt = datetime.datetime(
                        int(new_entry[1]),int(new_entry[2]),
                        int(new_entry[3]),int(new_entry[4]),
                        int(new_entry[5])
                        )
                        
            et_as_dt = datetime.datetime(
                        int(new_entry[1]),int(new_entry[2]),
                        int(new_entry[3]),int(new_entry[6]),
                        int(new_entry[7])
                        )
        except:
            print("Oops! There was an issue with your input. Please try again.")
            continue

        #make sure end time is after start time
        if st_as_dt > et_as_dt:
            print("Start time must be before end time. Please try again.")
            continue

        #make sure start time is in the future
        if st_as_dt < datetime.datetime.now():
            print("Start time must be in the future. Please try again" )
            continue

        #display selected date and confirm correct
        print("You are availabile on", format_date_text(new_entry))
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

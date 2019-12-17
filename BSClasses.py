import csv
import datetime
from BSFunctions import (
    update_csv,
    load_availability,
    print_band_members,
    format_date_text,
    display_availability,
    display_band_availability,
    delete_availability,
    add_availability
    )

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

                #if no change made we know the date is incompatable
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

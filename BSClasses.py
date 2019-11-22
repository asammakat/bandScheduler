import datetime
import csv


class Player:
    def __init__(self, name):
        self.name = name 
        self.availability = [] #Dates available

        # ##Get availability from csv file
        # with open("KTLschedule.txt") as csv_file:
        #     csv_reader = csv.reader(csv_file, delimiter = ",")
        #     line_count = 0
        #     for row in csv_reader:
        #         if line_count != 0:
        #             if row[0].upper() == self.name.upper():
        #                 self.availability.append(row)
        #         line_count = line_count + 1  
            
        #     #Deal with zeros
        #     for date in range(len(self.availability)):
        #         for item in range(len(self.availability[date])):
        #             if self.availability[date][item] == '0':
        #                 self.availability[date][item] = "00"                  
     
    def get_name(self):
        return self.name
    
    def get_availability(self):
        return self.availability

    def set_name(self, name):
        self.name = name

    def add_availability(self, date):
        self.availability.append(date)

def update_csv(band_member_list):
    
    availability = []
    for member in band_member_list:
        for date in member.get_availability():
            availability.append(date)
            
    with open("KTLschedule.txt", mode='w') as schedule:
        schedule_writer = csv.writer(schedule, delimiter=',')
        schedule_writer.writerow(["name", "year", "month", "day",
                          "startHour", "startMinute", "endHour",
                          "endMinute"])
        for date in availability:
            schedule_writer.writerow(date)

def add_availability(band_member):
    #name, year, month, day, startHour, startMinute, endHour, endMinute
    while(True):
        new_entry = []
        new_entry.append(band_member.get_name().lower())

        print("On what day are you available? (mm/dd/yyyy)")
        date = input()
        date = date.split("/")
        new_entry.append(date[2])
        new_entry.append(date[0])
        new_entry.append(date[1])

        print("What time does your availability start? (hh:mm)")
        start_time = input()
        start_time = start_time.split(":")
        new_entry.append(start_time[0])
        new_entry.append(start_time[1])

        print("What time does your availability end: (hh:mm)")
        end_time = input()
        end_time = end_time.split(":")
        new_entry.append(end_time[0])
        new_entry.append(end_time[1])

        print("You are available on %s/%s/%s from %s:%s to %s:%s\n"
                                        %(new_entry[2], new_entry[3],
                                         new_entry[1], new_entry[4],
                                         new_entry[5], new_entry[6],
                                         new_entry[7]))
        print("Is this correct?")
        confirm = input()
        if confirm == "y":
            band_member.add_availability(new_entry)

        print("Would you like to add another time? y/n")

        add_another = input()
        if add_another != "y":
            break


def load_availability(band_member_list):
    availability = []

    #read from csv file into availability
    with open("KTLschedule.txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                availability.append(row)
            line_count = line_count + 1

        #deal with 0, convert to 00
        for date in range(len(availability)):
            for item in range(len(availability[date])):
                if availability[date][item] == '0':
                    availability[date][item] = "00"
    
    for player in band_member_list:
        name = player.get_name().lower()
        for date in availability:
            if name == date[0]:
                player.add_availability(date)

def print_band_members(band_member_list):
    for i in range(len(band_member_list)):
        print(i+1, ": ", band_member_list[i].get_name())
        

def main():
    band_member_list = []
    #availability = []

    print("Welcome to band scheduler!")

    band = open("KTLRoster.txt")
    for i in band:
        name = ""
        for char in i:
            if char != "\n":
                name += char
        band_member_list.append(Player(name))
    band.close()

    print_band_members(band_member_list)

    print("Who are you? (choose a number)")
    band_member = band_member_list[int(input()) -1]
    #band_member = band_member.lower()
    #band_member = band_member.strip()

    load_availability(band_member_list)

    #display_availability(band_member, availability)
    for player in band_member_list:
        print(player.get_availability())

    user_input = 0
    while(True):
        print("What you like to do? \n"
               "    Press 1 to add availability.\n"
               "    Press 2 to delete availability\n"
               "    Press 3 to see all availability\n"
               "    Press 4 to see your availability\n"
               "    Press -1 to exit")
        user_input = int(input())

        if user_input == 1:
            availability = add_availability(band_member)
            print("new availability is: ", band_member.get_availability())
        elif user_input == 2:
            delete_availability()
        elif user_input == 3:
            see_all_availability()
        elif user_input == 4:
            display_availability(band_member, availability)
        elif user_input == -1:
            update_csv(band_member_list)
            print("goodbye")
            break
        else:
            print("I'm sorry I didn't understand you")

main()

# for i in band_member_list:    
#     print ("i loop: ", i.get_name(), i.get_availability())
#     i.add_availability(1)

# for i in band_member_list:
#     i.print_name()
#     print(i.get_availability())
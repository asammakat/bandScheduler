import datetime
import csv

def print_band_members(band_list):
    for j in range(len(band_list)):
        print(j + 1, ": ", band_list[j], sep='')

def display_availability(band_member, availability):
    print("Your current availability is: \n")
    for i in availability:
        if i[0] == band_member:
            print("    %s/%s/%s from %s:%s to %s:%s"
            %(i[2],i[3],i[1],i[4],i[5],i[6],i[7]))
    print("\n")

def parse_availability():
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
    return availability

def add_availability(band_member, availability):
    #name, year, month, day, startHour, startMinute, endHour, endMinute
    while(True):
        new_entry = []
        new_entry.append(band_member)

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
            availability.append(new_entry)

        print("Would you like to add another time? y/n")

        add_another = input()
        if add_another != "y":
            return availability
            break

def update_csv(availability):
    with open("KTLschedule.txt", mode='w') as schedule:
        schedule_writer = csv.writer(schedule, delimiter=',')
        schedule_writer.writerow(["name", "year", "month", "day",
                          "startHour", "startMinute", "endHour",
                          "endMinute"])
        for date in availability:
            schedule_writer.writerow(date)



def delete_availability():
    print("delete_availability")

def see_all_availability():
    print("see_all_availability")

def main():
    band_member_list = []
    availability = []

    print("Welcome to band scheduler!")

    band = open("KTLRoster.txt")
    for i in band:
        band_member_list.append(i)
    band.close()
    print_band_members(band_member_list)

    print("Who are you? (choose a number)")
    band_member = band_member_list[int(input()) -1]
    band_member = band_member.lower()
    band_member = band_member.strip()

    availability = parse_availability()

    display_availability(band_member, availability)

    user_input = 0;
    while(True):
        print("What you like to do? \n"
               "    Press 1 to add availability.\n"
               "    Press 2 to delete availability\n"
               "    Press 3 to see all availability\n"
               "    Press 4 to see your availability\n"
               "    Press -1 to exit")
        user_input = int(input())

        if user_input == 1:
            availability = add_availability(band_member, availability)
        elif user_input == 2:
            delete_availability()
        elif user_input == 3:
            see_all_availability()
        elif user_input == 4:
            display_availability(band_member, availability)
        elif user_input == -1:
            print(availability)
            update_csv(availability)
            print("goodbye")
            break
        else:
            print("I'm sorry I didn't understand you")

main()

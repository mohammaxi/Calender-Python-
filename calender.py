import sys
import re

miladi_months = ["", "January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
shamsi_months = ["", "Farvardin", "Ordibehesht", "Khordad", "Tir", "Mordad", "Shahrivar",
                 "Mehr", "Aban", "Azar", "Dey", "Bahman", "Esfand"]

def validate_time(func):
    def wrapper(self, hour, minute):
        if not (isinstance(hour, int) and 0 <= hour <= 23 and isinstance(minute, int) and 0 <= minute <= 59):
            raise ValueError("Invalid time")
        return func(self, hour, minute)
    return wrapper

def validate_day(func):
    def wrapper(self, miladi_day, shamsi_day):
        if not (isinstance(miladi_day, int) and 1 <= miladi_day <= 30 and isinstance(shamsi_day, int) and 1 <= shamsi_day <= 30):
            raise ValueError("Invalid day")
        return func(self, miladi_day, shamsi_day)
    return wrapper

def validate_month(func):
    def wrapper(self, miladi_month_num, shamsi_month_num, miladi_month_name, shamsi_month_name):
        if not (isinstance(miladi_month_num, int) and 1 <= miladi_month_num <= 12 and isinstance(shamsi_month_num, int) and 1 <= shamsi_month_num <= 12):
            raise ValueError("Invalid month num")
        if miladi_month_name != miladi_months[miladi_month_num] or shamsi_month_name != shamsi_months[shamsi_month_num]:
            raise ValueError("Invalid month name")
        return func(self, miladi_month_num, shamsi_month_num, miladi_month_name, shamsi_month_name)
    return wrapper

def validate_year(func):
    def wrapper(self, miladi_year, shamsi_year):
        if not (isinstance(miladi_year, int) and miladi_year > 0 and isinstance(shamsi_year, int) and shamsi_year > 0):
            raise ValueError("Invalid year")
        return func(self, miladi_year, shamsi_year)
    return wrapper

def validate_name(func):
    def wrapper(self, name):
        if not re.match(r'^[a-zA-Z0-9_]+$', name):
            raise ValueError("Invalid name")
        return func(self, name)
    return wrapper

class Time:
    def __init__(self, hour=0, minute=0):
        self._hour = hour
        self._minute = minute

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @validate_time
    def change_time(self, hour, minute):
        self._hour = hour
        self._minute = minute

    def __str__(self):
        return f"{self.hour}:{self.minute}"

class Day(Time):
    def __init__(self, miladi_day=1, shamsi_day=1, hour=0, minute=0):
        super().__init__(hour, minute)
        self._miladi_day = miladi_day
        self._shamsi_day = shamsi_day

    @property
    def miladi_day(self):
        return self._miladi_day

    @property
    def shamsi_day(self):
        return self._shamsi_day

    @validate_day
    def change_day(self, miladi_day, shamsi_day):
        self._miladi_day = miladi_day
        self._shamsi_day = shamsi_day

    def __str__(self):
        return f"{self.miladi_day}/{self.shamsi_day} {self.hour}:{self.minute}"

class Month(Day):
    def __init__(self, miladi_month_num=1, shamsi_month_num=1, miladi_month_name="January", shamsi_month_name="Farvardin", miladi_day=1, shamsi_day=1, hour=0, minute=0):
        super().__init__(miladi_day, shamsi_day, hour, minute)
        self._miladi_month_num = miladi_month_num
        self._shamsi_month_num = shamsi_month_num
        self._miladi_month_name = miladi_month_name
        self._shamsi_month_name = shamsi_month_name

    @property
    def miladi_month_num(self):
        return self._miladi_month_num

    @property
    def shamsi_month_num(self):
        return self._shamsi_month_num

    @property
    def miladi_month_name(self):
        return self._miladi_month_name

    @property
    def shamsi_month_name(self):
        return self._shamsi_month_name

    @validate_month
    def change_month(self, miladi_month_num, shamsi_month_num, miladi_month_name, shamsi_month_name):
        self._miladi_month_num = miladi_month_num
        self._shamsi_month_num = shamsi_month_num
        self._miladi_month_name = miladi_month_name
        self._shamsi_month_name = shamsi_month_name

    def __str__(self):
        return f"{self.miladi_month_name}/{self.shamsi_month_name} {self.miladi_day}/{self.shamsi_day} {self.hour}:{self.minute}"

class Calendar(Month):
    def __init__(self, id_, name, miladi_year=2024, shamsi_year=1402, miladi_month_num=1, shamsi_month_num=1, miladi_month_name="January", shamsi_month_name="Farvardin", miladi_day=1, shamsi_day=1, hour=0, minute=0):
        super().__init__(miladi_month_num, shamsi_month_num, miladi_month_name, shamsi_month_name, miladi_day, shamsi_day, hour, minute)
        self._id = id_
        self._name = name
        self._miladi_year = miladi_year
        self._shamsi_year = shamsi_year
        self._events = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def miladi_year(self):
        return self._miladi_year

    @property
    def shamsi_year(self):
        return self._shamsi_year

    @validate_year
    def change_year(self, miladi_year, shamsi_year):
        self._miladi_year = miladi_year
        self._shamsi_year = shamsi_year

    @validate_name
    def change_name(self, name):
        self._name = name

    def __str__(self):
        return f"{self.id} {self.name}: Calendar"

class Event:
    def __init__(self, title, event_type, miladi_date, shamsi_date, id_):
        self._title = title
        self._type = event_type
        self._miladi_date = miladi_date
        self._shamsi_date = shamsi_date
        self._id = id_

    @property
    def title(self):
        return self._title

    @property
    def type(self):
        return self._type

    @property
    def miladi_date(self):
        return self._miladi_date

    @property
    def shamsi_date(self):
        return self._shamsi_date

    @property
    def id(self):
        return self._id

    def __str__(self):
        return f"Event {self.title}: {self.type}"

users = {}
user_calendars = {}
user_enabled = {}
current_user = None

def print_reg_menu():
    print("Please choose")
    print("Register for registering a new user")
    print("Login for logging in")
    print("Change Password for changing the password")
    print("Remove for removing a user")
    print("Show All Usernames for showing all usernames")
    print("Exit for exiting from the program")

def print_main_menu():
    print("Please choose")
    print("Create New Calendar for creating a new calendar")
    print("Open Calendar for opening a calendar")
    print("Enable Calendar for enabling a calendar")
    print("Disable Calendar for disabling a calendar")
    print("Delete Calendar for deleting a calendar")
    print("Edit Calendar for editing a calendar")
    print("ChangeTime for changing time")
    print("ChangeDay for changing day")
    print("ChangeMonth for changing month")
    print("ChangeYear for changing year")
    print("Show for showing events")
    print("Show Enabled Calendars for showing enabled calendars")
    print("Logout for logging out")

def print_calendar_menu():
    print("Please choose")
    print("Add Event for adding an event")
    print("Delete Event for deleting an event")
    print("Back for going back to main menu")

def reg_menu_loop():
    global current_user
    print_reg_menu()
    while True:
        try:
            line = input().strip()
        except EOFError:
            sys.exit(0)
        parts = line.split()
        if not parts:
            print_reg_menu()
            continue
        if parts[0] == "Exit":
            sys.exit(0)
        elif parts[0] == "Register" and len(parts) == 3:
            username, password = parts[1], parts[2]
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                print("Invalid input")
                print_reg_menu()
                continue
            if len(password) < 5 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
                print("Invalid input")
                print_reg_menu()
                continue
            if username in users:
                print("Invalid input")
                print_reg_menu()
                continue
            users[username] = password
            print("User registered successfully")
        elif parts[0] == "Login" and len(parts) == 3:
            username, password = parts[1], parts[2]
            if username not in users or users[username] != password:
                print("Invalid input")
                print_reg_menu()
                continue
            current_user = username
            if username not in user_calendars:
                user_calendars[username] = {}
                cal = Calendar(1, username, 2024, 1402, 1, 1, "January", "Farvardin", 1, 1, 0, 0)
                user_calendars[username][1] = cal
                user_enabled[username] = {1}
            print("Login successful")
            main_menu_loop()
            current_user = None
        elif parts[0] == "Change" and parts[1] == "Password" and len(parts) == 5:
            username, old_pass, new_pass = parts[2], parts[3], parts[4]
            if username not in users or users[username] != old_pass:
                print("Invalid input")
                print_reg_menu()
                continue
            if len(new_pass) < 5 or not re.search(r'[A-Z]', new_pass) or not re.search(r'[a-z]', new_pass) or not re.search(r'\d', new_pass):
                print("Invalid input")
                print_reg_menu()
                continue
            users[username] = new_pass
            print("Password changed successfully")
        elif parts[0] == "Remove" and len(parts) == 3:
            username, password = parts[1], parts[2]
            if username not in users or users[username] != password:
                print("Invalid input")
                print_reg_menu()
                continue
            del users[username]
            user_calendars.pop(username, None)
            user_enabled.pop(username, None)
            print("User removed successfully")
        elif parts[0] == "Show" and parts[1] == "All" and parts[2] == "Usernames" and len(parts) == 3:
            if not users:
                print("nothing")
            else:
                us = sorted(users.keys())
                for u in us:
                    print(u)
        else:
            print("Invalid input")
        print_reg_menu()

def main_menu_loop():
    global current_user
    print_main_menu()
    while True:
        try:
            line = input().strip()
        except EOFError:
            sys.exit(0)
        parts = line.split()
        if not parts:
            print_main_menu()
            continue
        if parts[0] == "Logout":
            print("Logged out successfully")
            return
        elif parts[0:3] == ["Create", "New", "Calendar"] and len(parts) == 4:
            title = parts[3]
            if not re.match(r'^[a-zA-Z0-9_]+$', title):
                print("Invalid input")
                print_main_menu()
                continue
            if current_user not in user_calendars:
                user_calendars[current_user] = {}
            next_id = max(user_calendars[current_user].keys(), default=0) + 1
            cal = Calendar(next_id, title, 2024, 1402, 1, 1, "January", "Farvardin", 1, 1, 0, 0)
            user_calendars[current_user][next_id] = cal
            print("Calendar created successfully")
        elif parts[0:2] == ["Open", "Calendar"] and len(parts) == 3:
            try:
                cid = int(parts[2])
            except ValueError:
                print("Invalid input")
                print_main_menu()
                continue
            if cid not in user_calendars[current_user]:
                print("Invalid input")
                print_main_menu()
                continue
            print("Calendar opened successfully")
            calendar_menu_loop(cid)
            print("Returned to main menu")
        elif parts[0:2] == ["Enable", "Calendar"] and len(parts) == 3:
            try:
                cid = int(parts[2])
            except ValueError:
                print("Invalid input")
                print_main_menu()
                continue
            if cid not in user_calendars[current_user]:
                print("Invalid input")
                print_main_menu()
                continue
            user_enabled.setdefault(current_user, set()).add(cid)
            print("Calendar enabled successfully")
        elif parts[0:2] == ["Disable", "Calendar"] and len(parts) == 3:
            try:
                cid = int(parts[2])
            except ValueError:
                print("Invalid input")
                print_main_menu()
                continue
            if cid not in user_calendars[current_user]:
                print("Invalid input")
                print_main_menu()
                continue
            user_enabled.get(current_user, set()).discard(cid)
            print("Calendar disabled successfully")
        elif parts[0:2] == ["Delete", "Calendar"] and len(parts) == 3:
            try:
                cid = int(parts[2])
            except ValueError:
                print("Invalid input")
                print_main_menu()
                continue
            if cid not in user_calendars[current_user]:
                print("Invalid input")
                print_main_menu()
                continue
            del user_calendars[current_user][cid]
            user_enabled.get(current_user, set()).discard(cid)
            print("Calendar deleted successfully")
        elif parts[0:2] == ["Edit", "Calendar"] and len(parts) == 4:
            try:
                cid = int(parts[2])
            except ValueError:
                print("Invalid input")
                print_main_menu()
                continue
            new_title = parts[3]
            if not re.match(r'^[a-zA-Z0-9_]+$', new_title):
                print("Invalid input")
                print_main_menu()
                continue
            if cid not in user_calendars[current_user]:
                print("Invalid input")
                print_main_menu()
                continue
            try:
                user_calendars[current_user][cid].change_name(new_title)
                print("Calendar edited successfully")
            except ValueError:
                print("Invalid input")
        elif parts[0] == "ChangeTime" and len(parts) == 4:
            try:
                cid, hour, minute = int(parts[1]), int(parts[2]), int(parts[3])
            except ValueError:
                print("Invalid input")
                print_main_menu()
                continue
            if cid not in user_calendars[current_user]:
                print("Invalid input")
                print_main_menu()
                continue
            try:
                user_calendars[current_user][cid].change_time(hour, minute)
                print("Time changed successfully")
            except ValueError:
                print("Invalid input")
        elif parts[0] == "ChangeDay" and len(parts) == 4:
            try:
                cid, miladi_day, shamsi_day = int(parts[1]), int(parts[2]), int(parts[3])
            except ValueError:
                print("Invalid input")
                print_main_menu()
                continue
            if cid not in user_calendars[current_user]:
                print("Invalid input")
                print_main_menu()
                continue
            try:
                user_calendars[current_user][cid].change_day(miladi_day, shamsi_day)
                print("Day changed successfully")
            except ValueError:
                print("Invalid input")
        elif parts[0] == "ChangeMonth" and len(parts) == 6:
            try:
                cid, mil_mn, sha_mn = int(parts[1]), int(parts[2]), int(parts[3])
                mil_name, sha_name = parts[4], parts[5]
            except ValueError:
                print("Invalid input")
                print_main_menu()
                continue
            if cid not in user_calendars[current_user]:
                print("Invalid input")
                print_main_menu()
                continue
            try:
                user_calendars[current_user][cid].change_month(mil_mn, sha_mn, mil_name, sha_name)
                print("Month changed successfully")
            except ValueError:
                print("Invalid input")
        elif parts[0] == "ChangeYear" and len(parts) == 4:
            try:
                cid, mil_year, sha_year = int(parts[1]), int(parts[2]), int(parts[3])
            except ValueError:
                print("Invalid input")
                print_main_menu()
                continue
            if cid not in user_calendars[current_user]:
                print("Invalid input")
                print_main_menu()
                continue
            try:
                user_calendars[current_user][cid].change_year(mil_year, sha_year)
                print("Year changed successfully")
            except ValueError:
                print("Invalid input")
        elif parts[0] == "Show" and len(parts) == 2:
            date_str = parts[1]
            if not re.match(r'^\d{2}_\d{2}_\d{4}$', date_str):
                print("Invalid input")
                print_main_menu()
                continue
            dparts = date_str.split('_')
            try:
                dd, mm, yyyy = int(dparts[0]), int(dparts[1]), int(dparts[2])
            except ValueError:
                print("Invalid input")
                print_main_menu()
                continue
            if not (1 <= dd <= 30 and 1 <= mm <= 12 and yyyy > 0):
                print("Invalid input")
                print_main_menu()
                continue
            print(f"events on {date_str}")
            all_events = []
            for cal in user_calendars[current_user].values():
                for ev in cal._events:
                    if ev.miladi_date.miladi_day == dd and ev.miladi_date.miladi_month_num == mm and ev.miladi_date.miladi_year == yyyy:
                        all_events.append(ev)
            if all_events:
                all_events.sort(key=lambda e: e.title)
                for ev in all_events:
                    print(str(ev))
        elif parts[0:3] == ["Show", "Enabled", "Calendars"] and len(parts) == 3:
            enabled_ids = sorted(user_enabled.get(current_user, set()))
            if not enabled_ids:
                print("nothing")
            else:
                for cid in enabled_ids:
                    if cid in user_calendars[current_user]:
                        cal = user_calendars[current_user][cid]
                        print(f"{cid} {cal.name}: Calendar")
        else:
            print("Invalid input")
        print_main_menu()

def calendar_menu_loop(cid):
    print_calendar_menu()
    while True:
        try:
            line = input().strip()
        except EOFError:
            return
        parts = line.split()
        if not parts:
            print_calendar_menu()
            continue
        if parts[0] == "Back":
            return
        elif parts[0:2] == ["Add", "Event"] and len(parts) == 6:
            title = parts[2]
            event_type = parts[3]
            mil_date_str = parts[4]
            sha_date_str = parts[5]
            if event_type not in ["ShowTrade", "Ceremony", "VIP", "conference"]:
                print("Invalid input")
                print_calendar_menu()
                continue
            if not re.match(r'^\d{2}_\d{2}_\d{4}$', mil_date_str) or not re.match(r'^\d{2}_\d{2}_\d{4}$', sha_date_str):
                print("Invalid input")
                print_calendar_menu()
                continue
            mil_parts = mil_date_str.split('_')
            sha_parts = sha_date_str.split('_')
            try:
                mdd, mmm, myyy = int(mil_parts[0]), int(mil_parts[1]), int(mil_parts[2])
                sdd, smm, syyy = int(sha_parts[0]), int(sha_parts[1]), int(sha_parts[2])
            except ValueError:
                print("Invalid input")
                print_calendar_menu()
                continue
            if not (1 <= mdd <= 30 and 1 <= mmm <= 12 and myyy > 0 and 1 <= sdd <= 30 and 1 <= smm <= 12 and syyy > 0):
                print("Invalid input")
                print_calendar_menu()
                continue
            mil_name = miladi_months[mmm]
            sha_name = shamsi_months[smm]
            miladi_cal = Calendar(0, "", myyy, 1402, mmm, 1, mil_name, "Farvardin", mdd, 1, 0, 0)
            shamsi_cal = Calendar(0, "", 2024, syyy, 1, smm, "January", sha_name, 1, sdd, 0, 0)
            cal = user_calendars[current_user][cid]
            event_id = len(cal._events) + 1
            ev = Event(title, event_type, miladi_cal, shamsi_cal, event_id)
            cal._events.append(ev)
            print("Event added successfully")
        elif parts[0:2] == ["Delete", "Event"] and len(parts) == 3:
            title = parts[2]
            cal = user_calendars[current_user][cid]
            for ev in cal._events:
                if ev.title == title:
                    cal._events.remove(ev)
                    print("Event deleted successfully")
                    break
            else:
                print("Invalid input")
        else:
            print("Invalid input")
        print_calendar_menu()

if __name__ == "__main__":
    reg_menu_loop()
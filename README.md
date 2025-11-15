# 🗓️ Calendar Management System (Miladi–Shamsi)

This is a **command-line based calendar and event management system** written in Python.  
It supports **user registration, login, multiple calendars, and event management** with **validation for Miladi and Shamsi dates**.

---

## 🚀 Features

- 👤 **User System**
  - Register, Login, Change Password, Remove user
  - Password validation (min length, uppercase, lowercase, digit)
  - Username format validation (`[a-zA-Z0-9_]`)

- 📅 **Calendar Management**
  - Create, Open, Edit, Enable, Disable, Delete calendars
  - Each user can have multiple calendars
  - Change time, day, month, and year with validation decorators

- 🕒 **Date Handling**
  - Supports both **Miladi (Gregorian)** and **Shamsi (Persian)** calendars
  - Validates months, days, and years before applying changes

- 🎉 **Event Management**
  - Add or delete events in calendars
  - Events contain both Miladi and Shamsi dates
  - Supports event types: `Show Trade`, `Ceremony`, `VIP`, `Conference`

- 🔍 **Search & Display**
  - Show all enabled calendars
  - Display all events on a specific date

---

## 🧩 Example Usage

▶️ Registration Menu
  - Please choose
  - Register for registering a new user
  - Login for logging in
  - Change Password for changing the password
  - Remove for removing a user
  - Show All Usernames for showing all usernames
  - Exit for exiting from the program

▶️ Register a new user
  - Register ali Ali123
  - User registered successfully

▶️ Login
  - Login ali Ali123
  - Login successful

▶️ Main Menu (after login)
  - Create New Calendar myCal
  - Calendar created successfully
  
  - Open Calendar 1
  - Calendar opened successfully

▶️ Add Event
  - Add Event Birthday VIP 01_05_2024 12_02_1403
  - Event added successfully

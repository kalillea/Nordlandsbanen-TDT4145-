# Norwegian railway

This is a train ticketing system database, designed to store information about train routes, schedules, stations, and ticketing information for the Norwegian railway.

## Database Tables

The database consists of the following tables:

Operator: Stores the train operators.

TrainRoute: Stores train routes and their respective operators.

Train: Stores the trains and their associated fuel types and routes.

Schedule: Stores the schedules for each train route and station.

Station: Stores the train stations and their altitudes.

Car: Stores the individual cars in each train.

SleepingCar: Stores the sleeping cars.

SleepingCompartment: Stores the sleeping compartments within sleeping cars.

ChairCar: Stores the chair cars.

Bed: Stores the beds within sleeping compartments.

Seat: Stores the seats within chair cars.

ChairCarTicket: Stores the tickets for chair cars and their associated schedules.

SleepingCarTicket: Stores the tickets for sleeping compartments and their associated schedules.

CustomerOrder: Stores the customer orders.

Customer: Stores the customers and their contact information.

Ticket: Stores the ticket information and their associated orders.

## Python Files

The project consists of the following Python files:

1. `main.py` - The main entry point for the application.
2. `operations.py` - Contains functions for performing CRUD operations on the database.
3. `shared.py` - Contains shared variables and constants.
4. `validators.py` - Contains validation functions.
5. `nordlandsbanen.py` - Writes information about the Nordlandsbanen railway to the database.
6. `menu.py` - Contains functions for displaying the main menu and submenus to the terminal.
7. `relations.py` - Contains functions for writing and reading from the database. Also includes the helper functions nice_print(data) and translate_station_name_to_id(station_name).

## Setup

1. Install any necessary dependencies (e.g., Python, SQLite). Notice that the 'tabulate' install also is necessary for proper table showage.
2. Create a database and execute the provided SQL script to create the necessary tables.
3. Update `shared.py` with the appropriate database connection details.
4. Run `main.py` to start the application.

## Usage

The application provides a simple command-line interface to interact with the railway system. Users can perform various tasks such as checking train schedules, booking tickets, and managing customer information.

Follow the on-screen prompts to navigate through the available options and perform the desired actions.

## Authors

- Knut Lilleaas (kalillea@ntnu.no)
- William Soma (willavs@ntnu.no)
- Jonas Skjerpe (jonasisk@ntnu.no)

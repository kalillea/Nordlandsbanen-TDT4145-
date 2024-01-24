from operations import insert_data, write
import os
import shared
from datetime import datetime


def nordlandsbanen():  # User story f)
    # Insert data for train routes, schedules, and ticket purchases

    response = input(
        'Do you want to initialize the Nordlandsbanen-database? Y/N: ').lower()

    if not response == 'y':
        print('Did not initialize.')
        return None

    write('''INSERT OR REPLACE INTO Operator (OperatorID, OperatorName) VALUES (?, ?)''', (1, 'SJ',))

    train_route_data = [
        # TrainRouteID, TrainRouteName, OperatorID
        (1, 'Trondheim-Bodø-Dag', 'north', 1),
        (2, 'Trondheim-Bodø-Natt', 'north', 1),
        (3, 'Mo i Rana-Trondheim', 'south', 1),
    ]

    insert_data(
        "INSERT OR REPLACE INTO TrainRoute (TrainRouteID, TrainRouteName, Direction, OperatorID) VALUES (?, ?, ?, ?)",
        train_route_data
    )

    # Arrival and Departure for a specific station.
    schedule_data_trondheim_bodø_dag = [
        (1, datetime(2023, 4, 3, 7, 49), 1, 1),  # Trondheim S
        (2, datetime(2023, 4, 3, 9, 51), 2, 1),  # Steinkjær
        (3, datetime(2023, 4, 3, 13, 20), 3, 1),  # Mosjøen
        (4, datetime(2023, 4, 3, 14, 31), 4, 1),  # Mo i Rana
        (5, datetime(2023, 4, 3, 16, 49), 5, 1),  # Fauske
        (6, datetime(2023, 4, 3, 17, 34), 6, 1),  # Bodø

        (19, datetime(2023, 4, 4, 7, 49), 1, 1),  # Trondheim S
        (20, datetime(2023, 4, 4, 9, 51), 2, 1),  # Steinkjær
        (30, datetime(2023, 4, 4, 13, 20), 3, 1),  # Mosjøen
        (40, datetime(2023, 4, 4, 14, 31), 4, 1),  # Mo i Rana
        (50, datetime(2023, 4, 4, 16, 49), 5, 1),  # Fauske
        (60, datetime(2023, 4, 4, 17, 34), 6, 1),  # Bodø
    ]

    schedule_data_trondheim_bodø_natt = [
        (7, datetime(2023, 4, 3, 23, 5), 1, 2),  # Trondheim S
        (8, datetime(2023, 4, 4, 0, 57), 2, 2),  # Steinkjær
        (9, datetime(2023, 4, 4, 4, 41), 3, 2),  # Mosjøen
        (10, datetime(2023, 4, 4, 5, 55), 4, 2),  # Mo i Rana
        (11, datetime(2023, 4, 4, 8, 19), 5, 2),  # Fauske
        (12, datetime(2023, 4, 4, 9, 5), 6, 2),  # Bodø

        (70, datetime(2023, 4, 4, 23, 5), 1, 2),  # Trondheim S
        (80, datetime(2023, 4, 5, 0, 57), 2, 2),  # Steinkjær
        (90, datetime(2023, 4, 5, 4, 41), 3, 2),  # Mosjøen
        (100, datetime(2023, 4, 5, 5, 55), 4, 2),  # Mo i Rana
        (110, datetime(2023, 4, 5, 8, 19), 5, 2),  # Fauske
        (120, datetime(2023, 4, 5, 9, 5), 6, 2),  # Bodø
    ]

    schedule_data_moirana_trondheim = [
        (13, datetime(2023, 4, 3, 8, 11), 4, 3),  # Mo i Rana
        (14, datetime(2023, 4, 3, 9, 14), 3, 3),  # Mosjøen
        (15, datetime(2023, 4, 3, 12, 31), 2, 3),  # Steinkjær
        (16, datetime(2023, 4, 3, 14, 13), 1, 3),  # Trondheim S

        (130, datetime(2023, 4, 4, 8, 11), 4, 3),  # Mo i Rana
        (140, datetime(2023, 4, 4, 9, 14), 3, 3),  # Mosjøen
        (150, datetime(2023, 4, 4, 12, 31), 2, 3),  # Steinkjær
        (160, datetime(2023, 4, 4, 14, 13), 1, 3),  # Trondheim S
    ]

    insert_data(
        "INSERT OR REPLACE INTO Schedule (ScheduleID, DepartureTime, StationID, TrainRouteID) VALUES (?, ?, ?, ?)",
        schedule_data_trondheim_bodø_dag
    )

    insert_data(
        "INSERT OR REPLACE INTO Schedule (ScheduleID, DepartureTime, StationID, TrainRouteID) VALUES (?, ?, ?, ?)",
        schedule_data_trondheim_bodø_natt
    )

    insert_data(
        "INSERT OR REPLACE INTO Schedule (ScheduleID, DepartureTime, StationID, TrainRouteID) VALUES (?, ?, ?, ?)",
        schedule_data_moirana_trondheim
    )

    station_data = [
        # StationID, Name, Altitude
        (1, "Trondheim S", 5.1),
        (2, "Steinkjær", 3.6),
        (3, "Mosjøen", 6.8),
        (4, "Mo i Rana", 3.5),
        (5, "Fauske", 34),
        (6, "Bodø", 4.1),
    ]

    insert_data(
        "INSERT OR REPLACE INTO Station (StationID, Name, Altitude) VALUES (?, ?, ?)",
        station_data
    )

    train_data = [
        # TrainID, FuelType, TrainRouteID
        (1, 'diesel', 1),
        (2, 'diesel', 2),
        (3, 'diesel', 3),
        (4, 'fairy-dust', 4),
    ]

    insert_data(
        "INSERT OR REPLACE INTO Train (TrainID, FuelType, TrainRouteID) VALUES (?, ?, ?)",
        train_data
    )

    bed_data = [
        # BedNumber, CompartmentID
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 2),
        (5, 3),
        (6, 3),
        (7, 4),
        (8, 4),
    ]

    insert_data(
        "INSERT OR REPLACE INTO Bed (BedNumber, CompartmentID) VALUES (?, ?)",
        bed_data
    )

    sleeping_car_data = [
        (1, 4),  # SleepingCarID, CarID
    ]

    sleeping_compartment_data = [
        (1, 1),  # CompartmentID, SleepingCarID
        (2, 1),
        (3, 1),
        (4, 1),
    ]
    insert_data(
        "INSERT OR REPLACE INTO SleepingCar (SleepingCarID, CarID) VALUES (?, ?)",
        sleeping_car_data
    )
    insert_data(
        "INSERT OR REPLACE INTO SleepingCompartment (CompartmentID, SleepingCarID) VALUES (?, ?)",
        sleeping_compartment_data
    )

    seat_data = [
        (1, 1),  # SeatNumber, ChairCarID
        (2, 1),
        (3, 1),
        (4, 1),
        (5, 1),
        (6, 1),
        (7, 1),
        (8, 1),
        (9, 1),
        (10, 1),
        (11, 1),
        (12, 1),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (5, 2),
        (6, 2),
        (7, 2),
        (8, 2),
        (9, 2),
        (10, 2),
        (11, 2),
        (12, 2),
        (1, 3),
        (2, 3),
        (3, 3),
        (4, 3),
        (5, 3),
        (6, 3),
        (7, 3),
        (8, 3),
        (9, 3),
        (10, 3),
        (11, 3),
        (12, 3),
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 4),
        (6, 4),
        (7, 4),
        (8, 4),
        (9, 4),
        (10, 4),
        (11, 4),
        (12, 4),
    ]

    insert_data(
        "INSERT OR REPLACE INTO Seat (SeatNumber, ChairCarID) VALUES (?, ?)",
        seat_data
    )

    chair_car_data = [
        (1, 1),  # ChairCarID, CarID
        (2, 2),
        (3, 3),
        (4, 5),
    ]
    
    insert_data(
        "INSERT OR REPLACE INTO ChairCar (ChairCarID, CarID) VALUES (?, ?)",
        chair_car_data
    )

    car_data = [
        (1, 1, 1),  # CarID, CarNumberFrontToBack, TrainID
        (2, 2, 1),
        (3, 1, 2),
        (4, 2, 2),
        (5, 1, 3),
    ]

    insert_data(
        "INSERT OR REPLACE INTO Car (CarID, CarNumberFrontToBack, TrainID) VALUES (?, ?, ?)",
        car_data
    )

    print('Overwrite complete.\n')


def overwrite_db():
    response = input(
        'Do you really want to overwrite the entire database? Y/N: ').lower()

    if not response == 'y':
        print('Did not overwrite database.')
        return None
    try:
        os.remove(shared.db_name)
    except:
        pass
    with open('data/tables.txt') as f:
        tables = [i + ';' for i in f.read().split(';')]
    for i in tables:
        write(i)

    nordlandsbanen()

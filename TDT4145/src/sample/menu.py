from relations import (get_train_routes_by_start_end_date_time, purchase_ticket, nice_print,
                       register_customer, get_train_routes_by_station)
from nordlandsbanen import overwrite_db
from validators import user_in_database
from operations import read, write
from datetime import datetime, timedelta
import shared


def main_menu():
    # Velkommen til menyen for
    print(f"Velkommen til menyen for {shared.db_name}")

    print(
        """
        Hva vil du gjøre?

        1) Få info om en stasjon 
        2) Få rutene mellom to stasjoner 
        3) Opprett bruker 
        4) Kjøp billetter (Krever bruker) 
        5) Se mine billetter (Krever bruker) 
        6) Logg inn 
        0) Gå ut

        Skriv inn tilsvarende nummer under
        """
    )

    action = input("Velg handling: ")
    print("\n------------------------------------------\n")
    try:
        if action == "1":
            choose_station_menu()

        elif action == "2":
            choose_two_stations_menu()

        elif action == "3":
            register_customer_menu()

        elif action == "4":
            if not user_in_database(shared.customerID):
                print("Du må være logget inn.")
                login_menu()
            else:
                buy_ticket_menu()

        elif action == "5":
            if not user_in_database(shared.customerID):
                print("Du må være logget inn.")
                login_menu()
            else:
                user_ticket_menu()

        elif action == "6":
            login_menu()

        elif action == "0":
            print('Ha en fin dag!')
            return None

        elif action == '?':
            debug_menu()
        main_menu()
        return 0

    except ValueError:
        # Viser feilmelding hvis brukeren taster noe som ikke er godkjent.
        print('Velg et tall fra menyen')
        main_menu()


def choose_station_menu():
    try:
        station = input("Skriv inn Stasjonsnavn: ")
        train_routes = get_train_routes_by_station(station)

        nice_print(train_routes)

        # for i in train_routes:
        #     print(f'| {i[1]} | {i[0]} |')
        print('\n')
        main_menu()

    except ValueError:
        # Viser feilmelding hvis brukeren taster noe som ikke er godkjent.
        print('Velg mellom Trondheim S, Steinkjer, Mosjøen, Mo I Rana, Fauske eller Bodø')
        choose_station_menu()


def choose_two_stations_menu():
    start_station = input("Skriv inn startstasjon: ")
    end_station = input("Skriv inn sluttstasjon: ")
    # date_time er en string. da virker den ikke sammen me timedelta
    try:
        date_time = datetime.strptime(
            input("Skriv inn dato: (YYYY-MM-DD) "), '%Y-%m-%d').date()
    except:
        print('Ikke riktig format.')
        choose_two_stations_menu()

    nice_print(get_train_routes_by_start_end_date_time(
        start_station, end_station, date_time))


def register_customer_menu():  # Denne er kvalitetssjekket og skal ikke røres.

    name = input("Skriv inn fullt navn: ")
    email = input("Skriv inn email: ")
    mobile_number = input("Skriv inn telefonnummer: ")
    register_customer(name, email, mobile_number)

    try:
        print(
            f"Takk for registreringen. Din BrukerID er {shared.customerID}")
        main_menu()

    except ValueError:
        # Viser feilmelding hvis brukeren taster noe som ikke er godkjent.
        print('Du skrev inn noe galt. Prøv igjen.')
        register_customer_menu()


def buy_ticket_menu():

    n_tickets = int(input('Hvor mange billetter vil du bestille? '))
    ticket_kind = input(
        'Hvilken type billett vil du kjøpe? ("seat" eller "bed") ').lower()

    if ticket_kind not in ['seat', 'bed']:
        print("Velg 'seat' eller 'bed'!")
        buy_ticket_menu()

    start_station = input('Hvor vil du reise fra? ')
    end_station = input('Hvor vil du reise til? ')
    user_input = input('Når vil du reise? (YYYY-MM-DD) ')

    try:
        travel_date = datetime.strptime(
            user_input, '%Y-%m-%d')  # legg til klokkeslett
    except ValueError:
        print('Ikke akseptert datoformat')
        buy_ticket_menu()

    order_id = purchase_ticket(n_tickets, ticket_kind,
                               start_station, end_station, travel_date)

    if order_id == None:
        print('Ingen billetter tilgjengelig.')
        main_menu()

    else:
        nice_print(read(
            '''
        SELECT *
        FROM CustomerOrder co
        Join Ticket t ON t.OrderID = co.OrderID
        WHERE t.OrderID = ?
        ''',
            (order_id,)
        ))
    print('\n')
    main_menu()


# Denne er skrevet av William. Han mener den skal virke fint, men har ikke testet den.
def user_ticket_menu():
    print("Mine billetter (sitteplasser)")
    nice_print(read(
        '''
        SELECT ti.TicketID, co.OrderTime, co.OrderID, cct.SeatNumber, tr.TrainRouteName
        FROM Ticket ti
        JOIN CustomerOrder co ON ti.OrderID = co.OrderID
		JOIN ChairCarTicket cct ON ti.TicketID = cct.TicketID
		JOIN Schedule sch ON sch.ScheduleID = cct.ScheduleID
		JOIN TrainRoute tr ON tr.TrainRouteID = sch.TrainRouteID
        WHERE co.CustomerID = ?
		GROUP BY cct.SeatNumber
        ''',
        (shared.customerID,)
    ))
    print('\n')
    print("Mine billetter (soveplasser)")
    nice_print(read(
        '''
        SELECT ti.TicketID, co.OrderTime, co.OrderID, sct.BedNumber, sct.CompartmentID as Compartment, tr.TrainRouteName
        FROM Ticket ti
        JOIN CustomerOrder co ON ti.OrderID = co.OrderID
		JOIN SleepingCarTicket sct ON ti.TicketID = sct.TicketID
        JOIN SleepingCompartment scp ON scp.CompartmentID = sct.CompartmentID
        JOIN SleepingCar sc ON sc.SleepingCarID = sct.SleepingCarID
        JOIN Car c ON c.CarID = sc.CarID
        JOIN Train t ON t.TrainID = c.TrainID
        JOIN TrainRoute tr ON tr.TrainRouteID = t.TrainRouteID
        WHERE co.CustomerID = ?
		GROUP BY sct.BedNumber
        ''',
        (shared.customerID,)
    ))
    main_menu()


def debug_menu():
    print(
        f"Welcome to the debug menu for the chosen database {shared.db_name}")

    print(
        """
        How can we be of service today? \n
        Input the correponding number. Would you like to: \n
        1) Print customers \n
        2) Custom read\n
        3) Custom write\n
        4) Overwrite database\n
        0) Exit debug menu
        """
    )

    action = input("Choose your next action:")
    print("---------------------------------------------")

    if action == '1':  # Print customers
        nice_print(read('''SELECT * FROM Customer'''))
    if action == '2':  # Custom read
        query = input('Query: ')
        nice_print(read(query))
    if action == '3':
        query = input('Query: ')
        write(query)
        print('Done!')
    if action == '4':
        overwrite_db()
    main_menu()


def login_menu():

    # Ber brukeren om å taste inn sin bruker-ID
    declared_user_id = int(input("Skriv inn BrukerID: "))
    try:
        # Sjekker om brukeren finnes i databasen
        if user_in_database(declared_user_id):
            # Setter shared.customerID til den angitte bruker-ID-en
            shared.customerID = declared_user_id
            name = read(
                '''SELECT CustomerName FROM Customer WHERE CustomerID = ?''', (shared.customerID,))[1][0]
            print(f'\nVelkommen {name}!\n')  # Viser velkomstmelding

        else:
            # Viser feilmelding hvis brukeren ikke finnes i databasen
            print("BrukerID er ikke funnet i databasen.\n")

    except ValueError:
        # Viser feilmelding hvis brukeren taster inn en streng i stedet for et heltall
        print('Din BrukerID er et heltall')
        login_menu()

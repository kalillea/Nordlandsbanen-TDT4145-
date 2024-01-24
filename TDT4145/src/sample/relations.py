from datetime import timedelta, datetime
import shared
from operations import read, write, insert_data
from tabulate import tabulate


def nice_print(rows):
    data = [list(row) for row in rows]
    print(tabulate(data[1:], headers=data[0], tablefmt="fancy_grid"))


def dep_nice_print(rows):
    for i in rows[1]:
        print(i)


def create_new_order():  # Denne er kvalitetssjekket og skal ikke røres.
    order_id = read('SELECT MAX(OrderID) FROM CustomerOrder')[1][0]
    if order_id is None:
        order_id = 1
    else:
        order_id += + 1

    order_time = datetime.now()

    write(
        '''
        INSERT INTO CustomerOrder (OrderID, OrderTime, CustomerID)
        VALUES (?, ?, ?)
        ''',
        (order_id, order_time, shared.customerID)
    )
    return order_id


def get_train_routes_by_station(station):
    result = read(
        '''
        SELECT sc.DepartureTime AS "Departure time", st.Name AS "Station"
        FROM Schedule sc
        JOIN Station st ON sc.StationID = st.StationID
        WHERE st.Name = ? ''',
        (station,)
    )
    if result == []:
        print('Denne stasjonen er ikke i databasen.')
    return result

# Denne er kvalitetssjekket og skal ikke røres.


def get_train_routes_by_start_end_date_time(start_station, end_station, date):

    start_station_id = translate_station_name_to_id(start_station)
    end_station_id = translate_station_name_to_id(end_station)

    if start_station_id > end_station_id:
        start_station_id, end_station_id = end_station_id, start_station_id

    result = read(
        '''
        SELECT DISTINCT sc1.DepartureTime AS DepartureTime, sc1.TrainRouteID, st1.Name AS StartStationName, st2.Name AS EndStationName, tr.TrainRouteName AS TrainRouteName
        FROM Schedule sc1
        JOIN Schedule sc2 ON sc1.TrainRouteID = sc2.TrainRouteID
        JOIN Station st1 ON st1.StationID = sc1.StationID AND st1.Name = ?
        JOIN Station st2 ON st2.StationID = sc2.StationID AND st2.Name = ?
        JOIN TrainRoute tr ON tr.TrainRouteID = sc1.TrainRouteID
        WHERE sc1.DepartureTime BETWEEN ? AND ?
        ORDER BY DepartureTime
        ''',
        (start_station, end_station, date, date + timedelta(1))
    )
    if result == []:
        print('Ingen togruter i dette intervallet.')
    return result

# Denne er kvalitetssjekket og skal ikke røres.lt


# Denne er kvalitetssjekket og skal ikke røres.
def register_customer(name, email, mobile_number):
    customerID = read(f'''SELECT MAX(CustomerID) FROM Customer''')[1][0]
    if customerID is None:
        customerID = 1
    else:
        customerID += 1

    write(
        '''
        INSERT INTO Customer (CustomerID, CustomerName, Email, MobileNumber)
        VALUES (?, ?, ?, ?)
        ''',
        (customerID, name, email, mobile_number)
    )
    shared.customerID = customerID


def get_train_routes_by_station_and_weekday(station, weekday):
    return read(
        '''
        SELECT s.StationID
        FROM Station s.
        ''',
        (station, weekday)
    )


def create_new_ticket():
    ticket_id = read(f'''SELECT MAX(TicketID) FROM Ticket''')[1][0]
    if ticket_id is None:
        ticket_id = 1
    else:
        ticket_id += 1
    return ticket_id


def purchase_ticket(n_tickets, ticket_kind, start_station_name, end_station_name, travel_time):
    order_id = create_new_order()
    start_station_id = translate_station_name_to_id(start_station_name)
    end_station_id = translate_station_name_to_id(end_station_name)
    if start_station_id < end_station_id:
        direction = 'north'
        diff = end_station_id - start_station_id

    elif start_station_id > end_station_id:
        direction = 'south'
        diff = start_station_id - end_station_id

        start_station_id, end_station_id = end_station_id, start_station_id
    else:
        print('Noe gikk galt...')

    for _ in range(n_tickets):

        if ticket_kind == "seat":

            eligeble_ticket = read(
                '''
                SELECT sc.ScheduleID, s.SeatNumber, cc.ChairCarID
                FROM Schedule sc
                JOIN Train t ON sc.TrainRouteID = t.TrainRouteID
                JOIN TrainRoute tr ON tr.TrainRouteID = t.TrainRouteID
                JOIN Car c ON c.TrainID = t.TrainID
                JOIN ChairCar cc ON cc.CarID = c.CarID
                JOIN Seat s ON s.ChairCarID = cc.ChairCarID
                WHERE (sc.ScheduleID, s.SeatNumber, cc.ChairCarID) NOT IN
                (SELECT cct.ScheduleID, cct.SeatNumber, cct.ChairCarID
                FROM Ticket tkt
                JOIN ChairCarTicket cct ON tkt.TicketID = cct.TicketID)
                AND (sc.DepartureTime >= ?  AND sc.DepartureTime <= ?)
                AND (sc.StationID >= ? AND StationID <= ? )
                AND ( tr.Direction = ? )
                GROUP BY sc.ScheduleID
                ORDER BY sc.ScheduleID ASC
                LIMIT ?
                ''',
                (travel_time, travel_time + timedelta(1),
                 start_station_id, end_station_id - 1, direction, diff)
            )

            ticket_id = create_new_ticket()

            schedule_id = [i[0] for i in eligeble_ticket[1:]]
            seat_number_data = [i[1] for i in eligeble_ticket[1:]]
            chair_car_data = [i[2] for i in eligeble_ticket[1:]]

            ticket_data = []
            for i in range(len(schedule_id)):
                ticket_data.append(
                    [ticket_id, seat_number_data[i], chair_car_data[i], schedule_id[i]])

            insert_data('INSERT INTO ChairCarTicket (TicketID, SeatNumber, ChairCarID, ScheduleID) VALUES (?, ?, ?, ?)',
                        ticket_data)

        if ticket_kind == "bed":

            eligeble_ticket = read(
                '''
                SELECT sc.ScheduleID, sc.SleepingCarID, sco.CompartmentID, b.BedNumber
                FROM Schedule sc
                JOIN Train t ON sc.TrainRouteID = t.TrainRouteID
                JOIN TrainRoute tr ON tr.TrainRouteID = t.TrainRouteID
                JOIN Car c ON c.TrainID = t.TrainID
                JOIN SleepingCar sc ON sc.CarID = c.CarID
                JOIN SleepingCompartment sco ON sco.SleepingCarID = sc.SleepingCarID
                JOIN Bed b ON b.CompartmentID = sco.CompartmentID
                WHERE (sc.SleepingCarID, sco.CompartmentID, b.BedNumber) NOT IN
                (SELECT sct.SleepingCarID, sct.CompartmentID, sct.BedNumber
                FROM Ticket tkt
                JOIN SleepingCarTicket sct ON sct.TicketID = tkt.TicketID)
                AND (sc.SleepingCarID, sco.CompartmentID) NOT IN
                (SELECT sct.SleepingCarID, sct.CompartmentID
                FROM Ticket tkt
                JOIN SleepingCarTicket sct ON sct.TicketID = tkt.TicketID
                WHERE tkt.OrderID != ?)
                AND (sc.DepartureTime >= ?  AND sc.DepartureTime <= ?)
                AND (sc.StationID >= ? AND StationID <= ? )
                AND ( tr.Direction = ? )
                GROUP BY sc.ScheduleID
                ORDER BY sc.ScheduleID ASC
                LIMIT ?
                ''',
                (order_id, travel_time, travel_time + timedelta(1),
                 start_station_id, end_station_id - 1, direction, diff)
            )

            ticket_id = create_new_ticket()

            schedule_id = [i[0] for i in eligeble_ticket[1:]]
            sleepincarID = [i[1] for i in eligeble_ticket[1:]]
            compartmentID = [i[2] for i in eligeble_ticket[1:]]
            bednumber = [i[3] for i in eligeble_ticket[1:]]

            ticket_data = []
            for i in range(len(schedule_id)):
                ticket_data.append(
                    [ticket_id, compartmentID[i], sleepincarID[i], bednumber[i]])

            insert_data('INSERT INTO SleepingCarTicket (TicketID, CompartmentID, SleepingCarID, BedNumber) VALUES (?, ?, ?, ?)',
                        ticket_data)

        write('INSERT INTO Ticket (TicketID, OrderID) VALUES (?,?)',
              (ticket_id, order_id))
    return order_id


def translate_station_name_to_id(station_name):
    try:
        station_id = read(
            '''
            SELECT s.StationID
            FROM Station s
            WHERE s.Name = ?
            ''', (station_name,)
        )
        return station_id[1][0]
    except IndexError:
        print("Feil stasjon.")
        pass

# denne funksjonen skal finne seter/senger som ikke allerede har en ticket relasjon på disse schedule id-ene.
# Opprette en ny ticketID som har relajson til schedule og sete som angitt.
# Til slutt skal den legge bilettene til en ordre ved bruk av create_new_order() og returnere ordreID-en.

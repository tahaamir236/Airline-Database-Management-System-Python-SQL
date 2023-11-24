# test.py
import mysql.connector
import os
import time
import pandas as pd
mydb = mysql.connector.connect(
host="localhost",
user="root",
passwd="root"
)

mycursor = mydb.cursor()
mycursor.execute("USE airline")

def create_passenger():
	print ("****NEW PASSENGER****\n")
	name = input("Full Name: ")

	while True:
		cnic = input("CNIC: ")
		if len(cnic) != 13:
			print ("*ERROR*: CNIC Invalid!")
			continue
		else:
			break

	while True:
		phone = input("Phone: ")
		if len(phone) != 11:
			print ("*ERROR*: Phone Invalid!")
			continue
		else:
			break

	address = input("Address: ")
	nationality = input("Nationality: ")

	query = "INSERT INTO passenger(name, cnic, phone, address, nationality) VALUES(%s,%s,%s,%s,%s)"
	args = (name, cnic, phone, address, nationality)
	try:
		mycursor.execute(query, args)
		mydb.commit()
		print("Passenger Created!\n")
	except mysql.connector.IntegrityError as err:
		print("*ERROR*: Passenger Already Exists!\n")


def update_passenger():
	print ("****UPDATE PASSENGER****\n")

	while True:
		nic = input("CNIC: ")
		if len(nic) != 13:
			print ("*ERROR*: CNIC Invalid!")
			continue
		else:
			break

	mycursor.execute("SELECT cnic FROM passenger WHERE cnic = %s", (nic,))
	check = mycursor.fetchall()

	if not check:
		print ("Passenger Does Not Exist!\n")
		return

	else:
		query = "SELECT name FROM passenger WHERE cnic = %s"
		args = (nic,)
		mycursor.execute(query, args)
		row = mycursor.fetchall()
		for r in row:
			print("Updating Records For:", '\n'.join(r))

		while True:
			phone = input("Phone: ")
			if len(phone) != 11:
				print ("*ERROR*: Phone Invalid!")
			else:
				break

		address = input("Address: ")
		nationality = input("Nationality: ")

		update_query = "UPDATE passenger SET phone = %s, address = %s, nationality = %s WHERE cnic = %s"
		update_args = (phone, address, nationality, nic)
		mycursor.execute(update_query, update_args)
		mydb.commit()

		print("Record Updated\n")

def view_flights():
	print ("****VIEW FLIGHTS****\n")
	while True:
		dep = input("Departure Airport: ")
		if len(dep) != 3:
			print ("*ERROR*: Invalid IATA Code")
			continue
		else:
			break

	while True:
		arr = input("Arrival Airport: ")
		if len(arr) != 3:
			print ("*ERROR*: Invalid IATA Code")
			continue
		else:
			break

	date = input("Date(YYYY-MM-DD): ")

	start = input("From: ")
	end = input("Till: ")

	start = start + '00';
	end = end + '00';


	query = "SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s AND departure_time BETWEEN %s AND %s"
	args = (dep, arr,date, start, end)
	mycursor.execute(query, args)
	rows = mycursor.fetchall()
	if not rows:
		print("No Results!")
	else:
		df = pd.DataFrame(rows, columns = [
			'flight_id', 'departure_airport', 'arrival_airport', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time', 'airplane', 'fare'])
		print (df)

def cheapest():
	print ("****CHEAPEST FLIGHTS****\n")
	while True:
		dep = input("Departure Airport: ")
		if len(dep) != 3:
			print ("*ERROR*: Invalid IATA Code")
			continue
		else:
			break

	while True:
		arr = input("Arrival Airport: ")
		if len(arr) != 3:
			print ("*ERROR*: Invalid IATA Code")
			continue
		else:
			break
	query = "SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND fare = (SELECT MIN(fare) from flight WHERE departure_airport = %s AND arrival_airport = %s)"
	args = (dep, arr, dep, arr)
	mycursor.execute(query, args)

	rows = mycursor.fetchall()
	if not rows:
		print ("Search Results Empty!!\n")
	else:
		df = pd.DataFrame(rows, columns = [
			'flight_id', 'departure_airport', 'arrival_airport', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time', 'airplane', 'fare'])
		print (df)

def ticket_record():
	print ("****GENERATE TICKET****\n")
	while True:
		nic = input("CNIC: ")
		if len(nic) != 13:
			print ("*ERROR*: CNIC Invalid!")
			continue
		else:
			break

	while True:
		flight_in = input("Flight ID: ")
		if len(flight_in) != 5:
			print ("*ERROR*: Invalid Flight ID!")
			continue
		else:
			break
	try:
		query = "INSERT INTO ticket(cnic, flight_id) VALUES(%s,%s)"
		args = (nic, flight_in)
		mycursor.execute(query, args)
		mydb.commit()
		print("Ticket Generated\n")
		print_ticket = "SELECT name, cnic, flight_id, departure_airport, arrival_airport, departure_date, departure_time, arrival_date, arrival_time, fare FROM passenger, flight WHERE passenger.cnic = %s AND flight.flight_id = %s"
		args_ticket = (nic, flight_in)
		mycursor.execute(print_ticket, args_ticket)
		rows = mycursor.fetchall()
		df = pd.DataFrame(rows, columns = [
			'name', 'cnic', 'flight_id', 'departure_airport', 'arrival_airport', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time', 'fare'])
		print (df)
	except mysql.connector.IntegrityError as err:
		print("No Such Passenger or Flight!\n")

def flight_history():
	print ("****PASSENGER FLIGHT HISTORY****\n")
	while True:
		nic = input("CNIC: ")
		if len(nic) != 13:
			print ("*ERROR*: CNIC Invalid!")
			continue
		else:
			break

	query_check = "SELECT cnic FROM passenger WHERE cnic = %s"
	args_check = (nic,)
	mycursor.execute(query_check,args_check)
	check = mycursor.fetchall()
	if not check:
		print("Passenger Does not Exist!\n")
		return

	query = "SELECT ticket.flight_id, departure_airport, arrival_airport, departure_date, arrival_date FROM ticket JOIN flight ON ticket.flight_id = flight.flight_id WHERE cnic = %s"
	args = (nic,)
	mycursor.execute(query, args)
	rows = mycursor.fetchall()
	if not rows:
		print("Flight History Empty!\n")
		return
	else:
		df = pd.DataFrame(rows, columns = [
			'flight_id', 'departure_airport', 'arrival_airport', 'departure_date', 'arrival_date'])
		print (df)

def cancel_ticket():
	print ("****CANCEL TICKET****\n")
	while True:
		nic = input("CNIC: ")
		if len(nic) != 13:
			print ("*ERROR*: CNIC Invalid!")
			continue
		else:
			break

	while True:
		flight_in = input("Flight ID: ")
		if len(flight_in) != 5:
			print ("*ERROR*: Invalid Flight ID!")
			continue
		else:
			break

	query_check = "SELECT cnic FROM ticket WHERE cnic = %s"
	args_check = (nic,)
	mycursor.execute(query_check,args_check)
	check = mycursor.fetchall()
	if not check:
		print("Ticket does not exist for this passenger\n!")
		return

	query_check = "SELECT flight_id FROM ticket WHERE flight_id = %s AND cnic = %s"
	args_check = (flight_in, nic)
	mycursor.execute(query_check,args_check)
	check = mycursor.fetchall()
	if not check:
		print("Passenger did not book this flight!\n")
		return

	query = "DELETE FROM ticket where cnic = %s AND flight_id = %s"
	args = (nic, flight_in)
	mycursor.execute(query, args)
	mydb.commit()
	print("Ticket Record Deleted!\n")

def add_flight():
	print ("****ADD FLIGHT****\n")
	while True:
		fid = input("Flight ID: ")
		if len(fid) != 5:
			print ("*ERROR*: ID Invalid!")
			continue
		else:
			break

	while True:
		dep = input("Departure Airport: ")
		if len(dep) != 3:
			print ("*ERROR*: Invalid IATA Code")
			continue
		else:
			break

	while True:
		arr = input("Arrival Airport: ")
		if len(arr) != 3:
			print ("*ERROR*: Invalid IATA Code")
			continue
		else:
			break
	
	dep_date = input("Departure Date(YYYY-MM-DD): ")

	while True:
		start = input("Departure Time: ")
		if start > '2359':
			print ("*ERROR*: Invalid Time")
			continue
		else:
			start = start + '00';
			break

	arr_date = input("Arrival Date(YYYY-MM-DD): ")

	while True:
		end = input("Arrival Time: ")
		if end > '2359':
			print ("*ERROR*: Invalid Time")
			continue
		else:
			end = end + '00';
			break

	airplane = input("Airplane: ")
	fare = input("Fare:")

	query = "INSERT INTO flight(flight_id, departure_airport, arrival_airport, departure_date, departure_time, arrival_date, arrival_time, airplane, fare) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	args = (fid, dep, arr, dep_date, start, arr_date, end, airplane, fare)
	try:
		mycursor.execute(query, args)
		mydb.commit()
		print("Flight Added!\n")
	except mysql.connector.IntegrityError as err:
		print("*ERROR*: Flight Already Exists!\n")

def update_flight():
	print ("****UPDATE FLIGHT****\n")

	while True:
		fid = input("Flight ID: ")
		if len(fid) != 5:
			print ("*ERROR*: ID Invalid!")
			continue
		else:
			break

	mycursor.execute("SELECT flight_id FROM flight WHERE flight_id = %s", (fid,))
	check = mycursor.fetchall()

	if not check:
		print ("Flight Does Not Exist!\n")
		return

	else:

		query = "SELECT flight_id FROM flight WHERE flight_id = %s"
		args = (fid,)
		mycursor.execute(query, args)
		row = mycursor.fetchall()
		for r in row:
			print("\nUpdating Records For:", '\n'.join(r))

	while True:
		dep = input("Departure Airport: ")
		if len(dep) != 3:
			print ("*ERROR*: Invalid IATA Code")
			continue
		else:
			break

	while True:
		arr = input("Arrival Airport: ")
		if len(arr) != 3:
			print ("*ERROR*: Invalid IATA Code")
			continue
		else:
			break

	dep_date = input("Departure Date(YYYY-MM-DD): ")
		
	while True:
		start = input("Departure Time: ")
		if start > '2359':
			print ("*ERROR*: Invalid Time")
			continue
		else:
			start = start + '00';
			break

	arr_date = input("Arrival Date(YYYY-MM-DD): ")

	while True:
		end = input("Arrival Time: ")
		if end > '2359':
			print ("*ERROR*: Invalid Time")
			continue
		else:
			end = end + '00';
			break

	airplane = input("Airplane: ")
	fare = input("Fare:")

	update_query = "UPDATE flight SET departure_airport = %s, arrival_airport = %s, departure_date = %s, departure_time = %s, arrival_date = %s, arrival_time = %s, airplane = %s, fare = %s WHERE flight_id = %s"
	update_args = (dep, arr, dep_date, start, arr_date, end, airplane, fare, fid)
	mycursor.execute(update_query, update_args)
	mydb.commit()

	print("Flight Updated!\n")

def cancel_flight():
	print ("****CANCEL FLIGHT****\n")

	while True:
		flight_in = input("Flight ID: ")
		if len(flight_in) != 5:
			print ("*ERROR*: Invalid Flight ID!")
			continue
		else:
			break

	query_check = "SELECT flight_id FROM flight WHERE flight_id = %s"
	args_check = (flight_in,)
	mycursor.execute(query_check,args_check)
	check = mycursor.fetchall()
	if not check:
		print("Flight Does not Exist!\n")
		return
	else:
		query = "DELETE FROM flight WHERE flight_id = %s"
		args = (flight_in,)
		mycursor.execute(query, args)
		mydb.commit()
		print("Flight Cancelled!\n")

def date_flights():
	print ("****IN/OUT FLIGHTS****\n")
	while True:
		airport = input("Airport: ")
		if len(airport) != 3:
			print ("*ERROR*: Invalid IATA Code")
			continue
		else:
			break

	date = input("Date(YYYY-MM-DD): ")

	dep_query = "SELECT * FROM flight WHERE departure_airport = %s AND departure_date = %s"
	dep_args = (airport, date)

	mycursor.execute(dep_query, dep_args)
	rows = mycursor.fetchall()
	print("\n***Flights Taking-Off***\n")
	if not rows:
		print("***No Flights Leaving on This Day!***\n")
	else:
		df = pd.DataFrame(rows, columns = [
			'flight_id', 'departure_airport', 'arrival_airport', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time', 'airplane', 'fare'])
		print (df)

	arr_query = "SELECT * FROM flight WHERE arrival_airport = %s AND arrival_date = %s"
	arr_args = (airport, date)

	mycursor.execute(arr_query, arr_args)
	rows = mycursor.fetchall()
	print("\n***Flights Landing***\n")
	if not rows:
		print("***No Flights Arriving on This Day***!\n")
	else:
		
		df = pd.DataFrame(rows, columns = [
			'flight_id', 'departure_airport', 'arrival_airport', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time', 'airplane', 'fare'])
		print (df)

reception_id = 'reception'
reception_pwd = 'reception'
admin_id = 'admin'
admin_pwd = 'admin'

def view_all():
	print ("****VIEW DATABASE****\n")

	print("\n***FLIGHT***")
	query_f = "SELECT * FROM flight"
	mycursor.execute(query_f)
	rows_f = mycursor.fetchall()
	df_f = pd.DataFrame(rows_f, columns = [
		'flight_id', 'departure_airport', 'arrival_airport', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time', 'airplane', 'fare'])
	print (df_f)


	print("\n***PASSENGER***")
	query_p = "SELECT * FROM passenger"
	mycursor.execute(query_p)
	rows_p = mycursor.fetchall()
	df_p = pd.DataFrame(rows_p, columns = [
		'name', 'cnic', 'phone', 'address', 'nationality'])
	print (df_p)


	print("\n***TICKET***")
	query_t = "SELECT * FROM ticket"
	mycursor.execute(query_t)
	rows_t = mycursor.fetchall()
	df_t = pd.DataFrame(rows_t, columns = [
		'cnic', 'flight_id'])
	print (df_t)

def login():
	choice = input("***Login***\nPress 1 for Reception\nPress 2 for Admin\nPress 3 to Quit\nChoice: ")
	time.sleep(0.5)
	os.system('clear')
	if (choice) == '1':
		while True:
			print("********RECEPTION DESK********")
			user_id = input("User ID: ")
			pwd = input("Password: ")

			if user_id != 'reception' or pwd != 'reception':
				print ("Invalid Credentials!")
				time.sleep(1)
				os.system('clear')
			else:
				print("Login Successful!")
				time.sleep(1)
				os.system('clear')
				break

	if (choice) == '2':
		while True:
			print("********ADMINISTRATOR********")
			user_id = input("User ID: ")
			pwd = input("Password: ")

			if user_id != 'admin' or pwd != 'admin':
				print ("Invalid Credentials!")
				time.sleep(1)
				os.system('clear')
			else:
				print("Login Successful!")
				time.sleep(1)
				os.system('clear')
				break
	
	return choice

def reception():
	print("""********RECEPTION DESK********
1. New Passenger
2. Update Passenger
3. View Flights
4. Generate Ticket
5. View Cheapest Flight
6. Passenger Flight History
7. Cancel Ticket
8. Logout""")

	menu = input("\n=>Choice: ")
	time.sleep(1)
	os.system('clear')

	while (menu) == '1':
		create_passenger()
		check = input("\nDo you wish to create another passenger? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break

	while (menu) == '2':
		update_passenger()
		check = input("\nDo you wish to update another passenger? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break

	while (menu) == '3':
		view_flights()
		check = input("\nDo you wish to view more flights? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break

	while (menu) == '4':
		ticket_record()
		check = input("\nDo you wish to generate more tickets? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break

	while (menu) == '5':
		cheapest()
		check = input("\nDo you wish to view another cheapest flight? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break

	while (menu) == '6':
		flight_history()
		check = input("\nDo you wish to view another flight history? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break

	while (menu) == '7':
		cancel_ticket()
		check = input("\nDo you wish to cancel another ticket? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break	

	if (menu) == '8':
		print("\nLogged Out!")
		time.sleep(0.5)
		os.system('clear')
		return 8;

	reception()	

def administrator():
	print("""********ADMINISTRATOR********
1. Add New Flight
2. Update Existing Flight
3. Cancel a Flight
4. View Outgoing and Incoming Flights
5. View Database
6. Logout""")

	menu = input("\n=>Choice: ")
	time.sleep(1)
	os.system('clear')

	while (menu) == '1':
		add_flight()
		check = input("\nDo you wish to add another flight? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break

	while (menu) == '2':
		update_flight()
		check = input("\nDo you wish to update another flight? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break

	while (menu) == '3':
		cancel_flight()
		check = input("\nDo you wish to cancel more flights? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break


	while (menu) == '5':
		view_all()
		check = input("\nDo you wish to exit view? :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			break
		else:
			time.sleep(0.5)
			os.system('clear')
			continue

	while (menu) == '4':
		date_flights()
		check = input("\nDo you wish to view more flights? (y/n) :")
		if check == 'y':
			time.sleep(0.5)
			os.system('clear')
			continue
		else:
			time.sleep(0.5)
			os.system('clear')
			break

	if (menu) == '6':
		print("Logged Out!")
		time.sleep(0.5)
		os.system('clear')
		return 8;

	administrator()

print("""
	                                        :::'###::::'####:'########::'##:::::::'####:'##::: ##:'########:
                                                ::'## ##:::. ##:: ##.... ##: ##:::::::. ##:: ###:: ##: ##.....::
                                                :'##:. ##::: ##:: ##:::: ##: ##:::::::: ##:: ####: ##: ##:::::::
                                                '##:::. ##:: ##:: ########:: ##:::::::: ##:: ## ## ##: ######:::
                                                 #########:: ##:: ##.. ##::: ##:::::::: ##:: ##. ####: ##...::::
                                                 ##.... ##:: ##:: ##::. ##:: ##:::::::: ##:: ##:. ###: ##:::::::
                                                 ##:::: ##:'####: ##:::. ##: ########:'####: ##::. ##: ########:
                                                ..:::::..::....::..:::::..::........::....::..::::..::........::
                           '##::::'##::::'###::::'##::: ##::::'###:::::'######:::'########:'##::::'##:'########:'##::: ##:'########:
                            ###::'###:::'## ##::: ###:: ##:::'## ##:::'##... ##:: ##.....:: ###::'###: ##.....:: ###:: ##:... ##..::
                            ####'####::'##:. ##:: ####: ##::'##:. ##:: ##:::..::: ##::::::: ####'####: ##::::::: ####: ##:::: ##::::
                            ## ### ##:'##:::. ##: ## ## ##:'##:::. ##: ##::'####: ######::: ## ### ##: ######::: ## ## ##:::: ##::::
                            ##. #: ##: #########: ##. ####: #########: ##::: ##:: ##...:::: ##. #: ##: ##...:::: ##. ####:::: ##::::
                            ##:.:: ##: ##.... ##: ##:. ###: ##.... ##: ##::: ##:: ##::::::: ##:.:: ##: ##::::::: ##:. ###:::: ##::::
                            ##:::: ##: ##:::: ##: ##::. ##: ##:::: ##:. ######::: ########: ##:::: ##: ########: ##::. ##:::: ##::::
                           ..:::::..::..:::::..::..::::..::..:::::..:::......::::........::..:::::..::........::..::::..:::::..:::::
                                                 :'######::'##:::'##::'######::'########:'########:'##::::'##:
                                                 '##... ##:. ##:'##::'##... ##:... ##..:: ##.....:: ###::'###:
                                                  ##:::..:::. ####::: ##:::..::::: ##:::: ##::::::: ####'####:
                                                 . ######::::. ##::::. ######::::: ##:::: ######::: ## ### ##:
                                                 :..... ##:::: ##:::::..... ##:::: ##:::: ##...:::: ##. #: ##:
                                                 '##::: ##:::: ##::::'##::: ##:::: ##:::: ##::::::: ##:.:: ##:
                                                 . ######::::: ##::::. ######::::: ##:::: ########: ##:::: ##:
                                                 :......::::::..::::::......::::::..:::::........::..:::::..::""")

time.sleep(2.5)
os.system('clear')

while True:

	x = login()
	if x == '1':
		y = reception()
		if y == '8':
			continue
	if x =='2':
		y = administrator()
		if y == '5':
			continue
	if x == '3':
		print("""
	                                
		9/11 WAS AN INSIDE JOB              			
                                    |
                                  .-'-.
                                 ' ___ '
                       ---------'  .-.  '---------
       _________________________'  '-'  '_________________________
        ''''''-|---|--/    \==][^',_m_,'^][==/    \--|---|-''''''
                      \    /  ||/   H   \||  \    /
                       '--'   OO   O|O   OO   '--'""")

		time.sleep(3)
		os.system('clear')
		exit()


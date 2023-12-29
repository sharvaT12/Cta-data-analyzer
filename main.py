#
# This project analyze and works with the data of CTA daily ridership. It finds the details and plots the data in the graph from command 1-9
# 
# Sharva Thakur
# UIN:- 654135206
# CS 341 Project 1
#

import sqlite3
import matplotlib.pyplot as plt



##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
  dbCursor = dbConn.cursor()
  print("General stats:")

  # prints the number stations
  dbCursor.execute("Select count(*) From Stations;")
  row = dbCursor.fetchone();
  print("  # of stations:", f"{row[0]:,}")

  # prints the number Stops
  dbCursor.execute("Select count(*) From Stops;")
  row = dbCursor.fetchone();
  print("  # of stops:", f"{row[0]:,}")

  # prints the number Ride entries
  dbCursor.execute("Select count(*) From Ridership;")
  row = dbCursor.fetchone();
  print("  # of ride entries:", f"{row[0]:,}")

  # prints the date range of the data base
  dbCursor.execute("Select date(min(ride_date)), date(max(ride_date)) from Ridership;")
  row = dbCursor.fetchone();
  print("  date range:", row[0], "-", row[1])

  # prints the Total Ridership
  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  row = dbCursor.fetchone();
  a = row[0]
  print("  Total ridership:", f"{row[0]:,}")

  # prints the Total Ridership on weekdays
  dbCursor.execute("Select sum(Num_Riders) From Ridership Where Type_of_Day is 'W';")
  row = dbCursor.fetchone();
  print("  Weekday ridership:", f"{row[0]:,}",f"({(row[0]/a)*100:.2f}%)")

  # prints the Total Ridership on saturdays
  dbCursor.execute("""Select sum(Num_Riders) From Ridership Where Type_of_Day is 'A';""")
  row = dbCursor.fetchone();
  print("  Saturday ridership:", f"{row[0]:,}",f"({(row[0]/a)*100:.2f}%)")

  # prints the Total Ridership on sundays and holidays
  dbCursor.execute("Select sum(Num_Riders) From Ridership Where Type_of_Day is 'U';")
  row = dbCursor.fetchone();
  print("  Sunday/holiday ridership:", f"{row[0]:,}",f"({(row[0]/a)*100:.2f}%)", "\n")



#
# commandOne
#
# This command finds the station or stations which are similar to input if none found then it prints no stations found
# 
def commandOne(dbConn):
  dbCursor = dbConn.cursor()
  t = input('\nEnter partial station name (wildcards _ and %): ')

  #sql statement
  sql = """Select Station_ID, Station_Name From Stations Where Station_Name Like '{0}' Order by Station_Name""" .format(t)
  dbCursor.execute(sql)
  rows = dbCursor.fetchall();

  #if no stations found
  if len(rows) == 0:
    print("**No stations found...")
  #if stations found
  else:
    for row in rows:
      print(row[0] ,":" , row[1] )



#
# commandTwo
#
# This function prints the ridership at all stations with their percentage
# 
def commandTwo(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership all stations **")

  #sql statement
  sql = """select Station_Name, (sum(Num_Riders)) from Stations join Ridership on Stations.Station_ID = Ridership.Station_ID group by Station_Name order by Station_Name ASC"""

  dbCursor.execute(sql)
  rows = dbCursor.fetchall();

  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  r1 = dbCursor.fetchone();

  #prints ridership at all stations
  for row in rows:
    print(row[0] ,":", f"{row[1]:,}" , f"({(row[1]/r1[0])*100:.2f}%)")



#
# commandThree
#
# This function prints the ridership at top 10 stations with their percentage
# 
def commandThree(dbConn):
  dbCursor = dbConn.cursor()
  print("** top-10 stations **")

  #sql statement
  sql = """select Station_Name, sum(Num_Riders) from Stations join Ridership on Stations.Station_ID = Ridership.Station_ID group by Station_Name order by sum(Num_Riders) DESC limit 10"""

  dbCursor.execute(sql)
  rows = dbCursor.fetchall();

  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  r1 = dbCursor.fetchone();

  #prints ridership at top 10 stations
  for row in rows:
    print(row[0] ,":", f"{row[1]:,}" , f"({(row[1]/r1[0])*100:.2f}%)")



#
# commandFour
#
# This function prints the ridership at 10 least crowded stations with their percentage
# 
def commandFour(dbConn):
  dbCursor = dbConn.cursor()
  print("** least-10 stations **")

  #sql statement
  sql = """select Station_Name, sum(Num_Riders) from Stations join Ridership on Stations.Station_ID = Ridership.Station_ID group by Station_Name order by sum(Num_Riders) ASC limit 10"""

  dbCursor.execute(sql)
  rows = dbCursor.fetchall();

  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  r1 = dbCursor.fetchone();

  #prints ridership at bottom 10 stations
  for row in rows:
    print(row[0] ,":", f"{row[1]:,}" , f"({(row[1]/r1[0])*100:.2f}%)")


#
# commandFive
#
# This function prints all the stations, their directions and if it is accessible or not at the given line(color)
# 
def commandFive(dbConn):
  dbCursor = dbConn.cursor()
  t = input('\nEnter a line color (e.g. Red or Yellow): ')

  #sql statement
  sql = """select Stop_Name, Direction, ADA from Lines join StopDetails on Lines.line_id = StopDetails.line_id join Stops on StopDetails.stop_id = Stops.stop_id where color like '{0}' group by stop_name order by stop_name asc; """ .format(t)

  dbCursor.execute(sql)
  rows = dbCursor.fetchall(); 

  #if invalid line
  if len(rows) == 0:
    print("**No such line...")
  else:
    for row in rows:
      if(row[2] == 1):
        a = "yes"
      else:
        a = "no"
      
      print(row[0] ,": direction =" , row[1], "(accessible? {0})" .format(a) )
      

#
# commandSix
#
# This function prints the ridership by month and their month. This function also plots the graph where x axis is the month and y axis is the ridership
# 
def commandSix(dbConn):

  print("** ridership by month **")


  #sql statement
  sql = """select strftime('%m', ride_date) as month, sum(num_riders) from Ridership group BY month order by month ASC"""

  dbCursor = dbConn.cursor()
  dbCursor.execute(sql)
  rows = dbCursor.fetchall(); 

  #prints month and ridership
  for row in rows:
    print(row[0] ,":", f"{row[1]:,}")


  t = input("\nPlot? (y/n) ")

  if(t == "y"):
    x = []
    y = []

    #adding month and riders
    for row in rows:
      x.append(row[0])
      y.append(row[1])

    plt.xlabel("month")
    plt.ylabel("number of riders (x*10^8)  ")
    plt.title("monthly ridership")
    plt.plot(x, y)
    plt.show()
  else:
    return
    
#
# commandSeven
#
# This function prints the ridership by year and their year. This function also plots the graph where x axis is the year(last two digits) and y axis is the ridership
# 
def commandSeven(dbConn):

  print("** ridership by year **")


  #sql statement
  sql = """select strftime('%Y', ride_date) as year, sum(num_riders) from Ridership group BY year order by year ASC"""

  dbCursor = dbConn.cursor()
  dbCursor.execute(sql)
  rows = dbCursor.fetchall(); 

  #adding year and riders
  for row in rows:
    print(row[0] ,":", f"{row[1]:,}")


  t = input("\nPlot? (y/n) ")

  if(t == "y"):
    x = []
    y = []

     #adding year and riders
    for row in rows:
      a = row[0]
      a = a[2:]
      x.append(a)
      y.append(row[1])

    plt.xlabel("year")
    plt.ylabel("number of riders (x*10^8)")
    plt.title("yearly ridership")
    plt.plot(x, y)
    plt.show()
  else:
    return


#
# commandEight
#
# This function takes 3 inputs. First is the year second and third are the name or similar name to the given input, if any one is not correct it terminates the function. This function prints the first and the last five ridership of both the stations and plots both the graphs.
# 
def commandEight(dbConn):
  year = input('\nYear to compare against?' )


  dbCursor = dbConn.cursor()
  station1 = input('\nEnter station 1 (wildcards _ and %): ')

  #sql statement
  sql1 = """select distinct Station_Name, Station_ID from Stations where Station_Name like '{0}'""".format(station1)

  dbCursor.execute(sql1)
  stat = dbCursor.fetchall();

  #if no match
  if(len(stat) == 0):
    print("**No station found...")
    return
  #if multiple stations found
  elif(len(stat)>1):
    print("**Multiple stations found...")
    return
    
  
  station2 = input('\nEnter station 2 (wildcards _ and %): ')

  #sql statement
  sql2 = """select distinct Station_Name, Station_ID from Stations where Station_Name like '{0}'""".format(station2)

  dbCursor.execute(sql2)
  stat1 = dbCursor.fetchall();

  #if no match
  if(len(stat1) == 0):
    print("**No station found...")
    return
  #if multiple stations found
  elif(len(stat1)>1):
    print("**Multiple stations found...")
    return
  

  #sql statement
  sql3 = """select date(ride_date), sum(num_riders), strftime('%j', ride_date) from Ridership join Stations on Ridership.Station_ID = Stations.Station_ID Where Station_Name like '{0}' and  strftime('%Y', ride_date) = '{1}' group by date(ride_date) order by date(ride_date) asc""".format(station1 , year)

  #sql statement
  sql4 = """select date(ride_date), sum(num_riders), strftime('%j', ride_date) from Ridership join Stations on Ridership.Station_ID = Stations.Station_ID Where Station_Name like '{0}' and  strftime('%Y', ride_date) = '{1}' group by date(ride_date) order by date(ride_date) asc""".format(station2 , year)

  
  
  dbCursor = dbConn.cursor()
  dbCursor.execute(sql3)
  rows = dbCursor.fetchall();

  dbCursor = dbConn.cursor()
  dbCursor.execute(sql4)
  rows1 = dbCursor.fetchall();

  print("Station 1:", stat[0][1], stat[0][0])
  #prints the first 5
  for n in range(0,5):
    print(rows[n][0], rows[n][1])

  #prints the last 5
  for n in range(len(rows)-5, len(rows)):
    print(rows[n][0], rows[n][1])


  print("Station 2:", stat1[0][1], stat1[0][0])
  #prints the first 5
  for n in range(0,5):
    print(rows1[n][0], rows1[n][1])

  #prints the last 5
  for n in range(len(rows1)-5, len(rows1)):
    print(rows1[n][0], rows1[n][1])


  p = input("\nPlot? (y/n) ")

  if p == "y":
    x = []
    y = []

    for row in rows:
      x.append(int(row[2]))
      y.append(row[1])

    plt.xlabel("day")
    plt.ylabel("number of riders")
    plt.title("riders each day of "+str(year))
    plt.plot(x, y, label = stat[0][0])


    x1 = []
    y1 = []

    for row in rows1:
      x1.append(int(row[2]))
      y1.append(row[1])

    plt.plot(x1, y1, label = stat1[0][0])
    
    plt.legend()
    
    plt.show()

  else:
    return


#
# commandNine
#
# This function takes input from of a line and prints the stop names and their latitude and longitude and then plots the exact stations on a map.
# 
def commandNine(dbConn):
  color = input('\nEnter a line color (e.g. Red or Yellow): ')

  #sql statement
  sql = """select distinct Station_Name, Latitude, Longitude from Lines join StopDetails on Lines.line_id = StopDetails.line_id join Stops on StopDetails.stop_id = Stops.stop_id join Stations on Stops.Station_ID = Stations.Station_ID where color like '{0}'group by Station_Name order by Station_Name asc""" .format(color)

  dbCursor = dbConn.cursor()
  dbCursor.execute(sql)
  rows = dbCursor.fetchall(); 

  #invalid line
  if len(rows) == 0:
    print("**No such line...")
    return;
  else:
    for row in rows:
      print(row[0],":", "({0}, {1})".format(row[1],row[2]))

  
  p = input("\nPlot? (y/n) ")

  if p == "y":
    x = []
    y = []

    for row in rows:
      x.append(row[2])
      y.append(row[1])

    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012,42.0868]

    plt.imshow(image, extent = xydims)
    
    plt.title(color + " line")

    if color.lower() == "purple-express":
      color = "Purple"

    plt.plot(x,y,"o", c = color)

    for row in rows:
      plt.annotate(row[0], (row[2], row[1]))

    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])

    plt.show()


#
# commands
#
# This function only handles in command
# 
def commands(dbConn):

  com = input('Please enter a command (1-9, x to exit): ')

  while(com != 'x'):
    if(com == '1'):
      commandOne(dbConn)
    elif(com == "2"):
      commandTwo(dbConn)
    elif(com == "3"):
      commandThree(dbConn)
    elif(com == "4"):
      commandFour(dbConn)
    elif(com == "5"):
      commandFive(dbConn)
    elif(com == "6"):
      commandSix(dbConn)
    elif(com == "7"):
      commandSeven(dbConn)
    elif(com == "8"):
      commandEight(dbConn)
    elif(com== "9"):
      commandNine(dbConn)
    else: 
      print ("**Error, unknown command, try again...")

    com = input('\nPlease enter a command (1-9, x to exit): ')
  

##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)
commands(dbConn)


#
# done
#
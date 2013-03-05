import customer as c
import order as o
from datetime import datetime
# start on main menu
#pot value to serial on change
#python reads in pot value
#look at twisted framework
#UI w/ pot value
#each time someone places a new order
#instantiate customer object
#JS -> sends to python -> send to 

a = c.Customer(raw_input('What is your name?'),datetime.now())
# print a
a_date = a.getOrderStartTime()

f = open("file.txt","a+")
f.write(str(a.selection) + "," + str(a.name)+",'"+str(a_date)+"'\n")

a = c.Customer('Moneyshot',datetime.now())
# print a
a_date = a.getOrderStartTime()

f = open("file.txt","a+")
f.write(str(a.selection) + "," + str(a.name)+",'"+str(a_date)+"'\n")
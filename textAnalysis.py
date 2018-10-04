### purpose: manipulate string data in python

###GOAL
amendMax = 0
#read in the constitution
with open('us_constitution.txt','r') as text:
	constitution = text.read()
	check =0
	#figure out the man number of amendments by cycling through looking for Amendment # until the Amendment can't be found
	amendMax = 0
	while (check != -1) :
		amendFind = "Amendment " + str(amendMax + 1)
		check = constitution.find(amendFind)
		if( check != -1) :
			amendMax += 1

def GetInt(str, default):
	#use when getting user input
	#the default is used to return a value that won't perform any actions and will cause the while lopp to repeat
	if StringIsInt(str):
		return int(str)
	else:
		return default

def StringIsInt(str):
	#see if getting an int from the string is valid
	try:
		int(str)
		return True
	#if not, print an error message
	except ValueError:
		print("A number was not entered")
		return False

def AddAmend():
	global constitution
	global amendMax
	#get the users amendment
	newAmend = input("Enter your new amendment:")
	#attach the amendment to the end of the document and increase the max number of amendments
	amendMax += 1
	constitution += "\nAmendment " + str(amendMax) + "\n\n" + newAmend
			
#new thing
def ShoutOut():
	printNum = 0
	#get user input and check if it's an int and an existing amendment
	while (printNum < 1 or printNum > amendMax):
		num = input('Choose a number between 1 and '+str(amendMax)+': ')
		if StringIsInt(printNum):
			printNum = int(printNum)
			if (printNum < 1):
				print("Please enter a positive number")
			if (printNum > amendMax):
				print("That number is too large. There are currently only ",amendMax," amendments.")
		else:
			printNum = 0
			
	thisAmend = "Amendment " + str(printNum)
	nextAmend = "Amendment " + str(printNum + 1)
	#find index of first amendment
	startAmend = constitution.find(thisAmend)
	#find index of second amendment
	endAmend = constitution.find(nextAmend)
	ammendClean = constitution[startAmend:endAmend].upper().strip()
	return ammendClean

def RemoveAmend():
	num = 0
	global constitution
	#get user's amendment number they'd like to delete
	while (num < 1 or num > amendMax):
		num = input('Choose a number between 1 and '+str(amendMax)+': ')
		if StringIsInt(num):
			num = int(num)
			if (num < 1):
				print("Please enter a positive number")
			if (num > amendMax):
				print("That number is too large. There are currently only ",amendMax," amendments.")
		else:
			num = 0
	#find start and end of that amendment by locating the terms Amendment # and Amendment # + 1
	thisAmend = "Amendment " + str(num)
	nextAmend = "Amendment " + str(num + 1)
	startAmend1 = constitution.find(thisAmend)
	endAmend1 = constitution.find(nextAmend)
	
	#edit the constitution string by adding everything before and after the two indexes
	constitution = constitution[0:startAmend1] + constitution[endAmend1:]

option = 0
while (option != 6):
	#print user options
	print("\nWhat would you like to do?")
	print("1 = View an existing amendment")
	print("2 = Add an amendment")
	print("3 = Remove an amendment")
	print("4 = See the whole constitution")
	print("5 = Save edited constitution")
	print("5 = Exit the program")
	#get user input
	option = input()
	option = GetInt(option, 0)
	#do what the user says
	if option == 1:
		#print out an amendment
		print(ShoutOut())
	if option == 2:
		#have user input a new amendment and attach it to the end, then increment the maxAmend
		AddAmend()
	if option == 3:
		#remove an amendment based on user input
		RemoveAmend()
	if option == 4:
		#print the whole thing
		print(constitution)

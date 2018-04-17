import serial #Importing libraries I need to run program
import time
import requests
import json
import serial.tools.list_ports
import timeit
from tkinter import *

class data: #Creating a class for all the functions I need to do dealing with data
    def loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2, avg, avg2): #Defining function that will be responsible for collecting and storing data
        
        try: #Will attempt to do what's below, if unable to do so will skip to the except IOError (This is a section of the code that handles errors)
            
            distance = ser.readline().decode().replace('\n', '') #Reading in the first distance sent from the Arduino
            distance2 = ser.readline().decode().replace('\n', '') #Reading in the second distance sent from the Arduino
            
            if start < 30 and distance != "" and distance != 0 : #Code below will only run in first 30 seconds, and only if I'm getting valid values for distance
            
                if start == 0: #Code below will run if it's the first iteration
                    object.status(False) #Calls on function status, and will pass value 0 to it (this will affect what I do in the function)
                elif start == 29: # Code will run once we hit 29 seconds
                    object.status(True) #Calls on function status, and will pass value 0 to it (this will affect what I do in the function)
                start+=1 #Keeping track of how many times we've run through this section, will run every time
                
                if start<5: #Calculating modifiers for first 5 seconds, although only the last one will be used. This must be done in order to throw away the first few inaccurate values gathered form the arduino.
                    modifier = float(distance)
                    modifier2 = float(distance2)
                
                elif start>=5: #Once 5 seconds have passed, I'll start to take an average of the modifiers so that our final modifier is an average of these pre-deflection readings
                    modifier = self.average(modifier, distance) #Calls on a function to average out values with new value, and then saves it as the new modifer
                    modifier2 = self.average(modifier2, distance2) #Calls on a function to average out values with new value, and then saves it as the new modifer2
            
            if distance != "" and distance2 != "" and start == 30 : #Code will run if we have valid arduino reading and we have surpassed the 30 second calibration that just took place
                
                distance = str(float(distance) - float(modifier)) #Distance will now be relative to whatever the starting value was (the modifier)
                distance2 = str(float(distance2) - float(modifier2)) #Same for distance 2
                
                if avg == -100.0: #This code will only ever run for the first iterartion of an average every 30 seconds
                    avg = float(distance) #Storing the very first data point in the 30 seconds. Will be needed when using the average function later
                    avg2 = float(distance2)

                else: #After the first iteration of the 30 seconds, code below will run
                    avg = self.average(avg, distance) #Calls on the average function to find the new average with the new data avaliable, and then sets the average to that value
                    avg2 = self.average(avg2, distance2) #Calls on the average function to find the new average with the new data avaliable, and then sets the average to that value
            
                time_hhmmss = time.strftime('%H:%M:%S') #Gets the time
                date_mmddyyyy = time.strftime('%d/%m/%Y') #Gets the date
                
                object.change(modifier, distance, modifier2, distance2, avg, avg2) #Calls on function to change labels in User Interface
                
                print('D1: ' + distance + ', ' + time_hhmmss + ', ' + date_mmddyyyy) #For debugging purposes
                print('D2: ' + distance2 + ', ' + time_hhmmss + ', ' + date_mmddyyyy)
                
                if count == 0 and sendTime != -1 : #At the start of the test, we will send information to the arduino
                    ser.write(b'0')
                    print("LED turned on!")
                
                if sendTime == count: #At the end, we will send more information to the arduino
                    ser.write(b'0')
                    print("LED turned off!")
                
                count+=1 #Adds 1 to the count of how many times we've ran through the program
                
                if count%30 == 0: #Code will run if the count is a multiple of 30 (the % function simply caluclates the remainder)
                    
                    data = {'date':date_mmddyyyy, 'time':time_hhmmss, 'dist':avg, 'dist2':avg2} #Preparing data in a format that firebase can read
                    result = requests.post(firebaseURL + '/' + urlAddition +'.json', data=json.dumps(data)) #Sending the data to firebase
                    print("Sent!")
                    avg = -100.0 #Setting averages back to unrealistic values so we know we are starting over
                    avg2 = -100.0
                    root.after(780, lambda: self.loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2, avg, avg2))
                    #Here we essentially tell our program to run this function again after 780 milliseconds. Notice that we don't use 1000, since uploaidng to firebase takes approximately 0.22 seconds.
                    #Note that this will only run every 30 seconds, and every time this is run the rest of the lines in this function won't be read since we would have already told the function to restart
            
            root.after(1000, lambda: self.loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2, avg, avg2))
            #Here we essentially tell our program to run this function again after 1 second.
        
        except IOError: #Code will run in the case that we have an error
            print('Error! Something went wrong.')
            root.after(1000, lambda: self.loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2, avg, avg2))

    def startTest(self, connections, buttons, entryTestName, entryTestLength): #Defining function that will run when we start the test
    
        firebaseURL = "https://work-5b7b6.firebaseio.com/" #Storing the url of the database I'll be uploading to
        
        connected = False #Creating variable that will keep track of whether or not the user conncted to a port
        
        for i in range(0, len(connections)): #Code will run for every port avaliable
            if connections[i]["text"]=="Connected.": #Checks if user connected to that specific port
                ser = serial.Serial(buttons[i]["text"], 9600, timeout=0) #If so, saves that port
                connected = True #Tells us that this user did indeed connect
                print(connections[i]["text"])
            i=+1 #Increases i so that the next port is checked
        
        if connected == False: #If user did not connect
            ser = serial.Serial('/dev/cu.usbmodem1461', 9600, timeout=0) #We'll set this port as the default (Note that this will only work for Macs, I am unsure what the port is common for windows
        
        sendTime = -1 #This section is just creating variables that are going to be updated in the loop function
        urlAddition = 'voltage'
        count = 0
        start = 0
        modifier = 0
        modifier2 = 0
        avg = -100.0
        avg2 = -100.0
        
        try:
            urlAddition = str(entryTestName.get()) #Attempts to get the test name user entered
        except (ValueError):
            print("Not a valid test name, voltage will be used.") #Will use /voltage if user doesn't enter valid name
        
        try:
            sendTime = int(entryTestLength.get()) #Attempts to get how long the test needs to be run for
        except (ValueError):
            print("Invalid time recieved, LED will not go off") #If invalid vlaue is entered, sendTime stays atg -1 and never goes off
        
        data.loop(data, self, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2, avg, avg2) #Starts the loop function

    def average(avg, new): #Function to calculate the average
        alpha=0.0645 #Closer to 0 gives less weight to new values, closer to 1 gives more weight to new values (Using 2/(N+1) right now)
        avg = (alpha * float(new)) + (1.0 - alpha) * avg #Calculates the average
        return avg; #Sends the new average back to wherever called on the function

class GUI(Frame): #Creating a class for all the functions I need to do dealing with the Graphic User Interface
    
    def connect(self, i):
        print(self.buttons[i]["text"])
        self.connections[i]["text"] = "Connected." #Function will connect to whatever port the user clicked
        
        for j in range(0, len(self.connections)): #Will run for every port
            if j==i: #Code will run if we are at port we just connected to
                continue #If it's the port we just connected to, we don't do anything
            else:
                self.connections[j]["text"]="" #In case that it's a different port, we make sure we aren't connected

    def closeWindow(self): #Function to close the program
        root.destroy() #Destorys frame
        exit() #Ends program
    
    def __init__(self, master): #Creates graphic user interface (i.e. making labels, buttons, attaching functions to buttons etc
        super(GUI, self).__init__() #Since we inherited from Frame, this is how we call the constructor for the window (This is my current understanding, I could be wrong. Never really learned object-oriented coding)
        self.grid() #Creates grid so we can place labels and buttons accordingly
        
        self.buttons = [] #Makes array for buttons, will be needed later
        self.connections = [] #Makes array for port connections, will be needed later
        
        self.labelTitle = Label(self, text = "Sash Testing With Sound") #Creating Title label
        self.labelTitle.grid(row=0, column = 1) #Placing Title label
        
        self.labelModifierStay = Label(self, text = "Modifier: ") #Creating Modifier label
        self.labelDistanceStay = Label(self, text = "Distance: ") #Creating Distance label
        self.labelLEDStay = Label(self, text = "LED: ") #Creating LED label
        self.labelAvgStay = Label(self, text= "Avg: ") #Creating Average label
        
        self.labelModifierStay.grid(row=1, column=3, sticky=E) #Placing Modifier label
        self.labelDistanceStay.grid(row=2, column=3, sticky = E) #Placing Distance label
        self.labelLEDStay.grid(row=3,column=3, sticky = E) #Placing LED label
        self.labelAvgStay.grid(row=4,column=3, sticky = E) #Placing Average label
        
        self.labelModifier = Label(self, text = "Value") #Creating Modifier Value label
        self.labelDistance = Label(self, text = "Value") #Creating Distance Value label
        self.labelLED = Label(self, text = "Green") #Creating LED Colour label
        self.labelAvg = Label(self, text = "Value") #Creating Average Value label
        
        self.labelModifier.grid(row=1, column=4, sticky=W) #Placing Modifier Value label
        self.labelDistance.grid(row=2, column=4,sticky=W) #Placing Distance Value label
        self.labelLED.grid(row=3, column=4, sticky=W) #Placing LED Colour label
        self.labelAvg.grid(row=4, column=4, sticky=W) #Placing Average Value label
        
        #Repeat of labels, except for second sensor. Refer to comments above, same logic applies.
        self.labelModifierStay2 = Label(self, text = "Modifier2: ")
        self.labelDistanceStay2 = Label(self, text = "Distance2: ")
        self.labelLEDStay2 = Label(self, text = "LED2: ")
        self.labelAvgStay2 = Label(self, text= "Avg: ")
        
        self.labelModifierStay2.grid(row=1, column=6, sticky=E)
        self.labelDistanceStay2.grid(row=2, column=6, sticky = E)
        self.labelLEDStay2.grid(row=3,column=6, sticky = E)
        self.labelAvgStay2.grid(row=4,column=6, sticky = E)
        
        self.labelModifier2 = Label(self, text = "Value")
        self.labelDistance2 = Label(self, text = "Value")
        self.labelLED2 = Label(self, text = "Red")
        self.labelAvg2 = Label(self, text = "Value")
        
        self.labelModifier2.grid(row=1, column=7, sticky=W)
        self.labelDistance2.grid(row=2, column=7,sticky=W)
        self.labelLED2.grid(row=3, column=7, sticky=W)
        self.labelAvg2.grid(row=4, column=7, sticky=W)
        #End of repeat
        
        self.labelTestName = Label(self, text = "Test Name: ") # Creating TestName label
        self.labelTestLength = Label(self, text = "Length of Test: ") #Creating LengthOfTest label
        self.entryTestName = Entry(self) #Creating textbox for TestName
        self.entryTestLength = Entry(self) #Creating textbox for Length of Test
        
        self.labelTestName.grid(row=1, column=0, sticky=E) #Placing TestName label
        self.labelTestLength.grid(row=2, column=0, sticky=E) #Placing LengthOfTest label
        self.entryTestName.grid(row=1, column=1, sticky=W) #Placing TestName textbox
        self.entryTestLength.grid(row=2, column=1, sticky=W) #Placing LengthOfTest textbox
        
        self.buttonStart = Button(self, text="Start", command = lambda:data.startTest(self, self.connections, self.buttons, self.entryTestName, self.entryTestLength)) #Creating Start Butyon
        #Note that with the "command" part, we attatched a function to start our test
        self.buttonStart.grid(row=3, column = 0) #Placing start button
        
        #Space
        self.labelSpace = Label(self, text = "             ") #Creating empty space to space out buttons and labels
        self.labelSpace2 = Label(self, text = "             ")
        self.labelSpace3 = Label(self, text = "             ")

        self.labelSpace.grid(row=1, column = 5) #Placing empty space to space out buttons and labels
        self.labelSpace.grid(row=2, column = 5)
        self.labelSpace.grid(row=3, column = 5)
        self.labelSpace.grid(row=4, column = 5)
        
        self.labelSpace2.grid(row=1, column = 2)
        self.labelSpace2.grid(row=2, column = 2)
        self.labelSpace2.grid(row=3, column = 2)
        self.labelSpace2.grid(row=4, column = 2)
        
        
        self.labelSpace3.grid(row=1, column = 8)
        self.labelSpace3.grid(row=2, column = 8)
        self.labelSpace3.grid(row=3, column = 8)
        self.labelSpace3.grid(row=4, column = 8)
        #End of space
        
        self.buttonExit = Button(self, text="Exit", command = self.closeWindow) #Creating Exit Button. Note that with the "command" part, we attached a function to close the program.
        self.buttonExit.grid(row=4, column = 0) #Placing Exit Button
    
        self.labelStatus = Label(self, text="") #Creating Status label
        self.labelStatus.grid(row=5, column=0) #Placing Status label
    
    def ports(self): #Function to display ports
        
        self.ports = list(serial.tools.list_ports.comports()) #Makes a list of ports
        
        i=0 #counter for the loop below
        for self.p in self.ports: #Code will run for every port in the list of ports
            
            #Creating the buttons for the ports
            self.port = (str(self.p)).split(" ")
            self.buttons.append(Button(self, text=self.port[0], command=lambda i=i: self.connect(i)))
            self.connections.append(Label(self, text=""))
            self.connections[i].grid(column=10, row=i+1, sticky=W)
            self.buttons[i].grid(column=9, row=i+1, sticky=W)
            print(self.p)
            i+=1

    def change(self, modifier, distance, modifier2 , distance2, avg, avg2): #Functions to change labels as they are updated
        self.labelModifier.config(text=modifier)
        self.labelDistance.config(text=distance)
        self.labelModifier2.config(text=modifier2)
        self.labelDistance2.config(text=distance2)
        self.labelAvg.config(text=str(avg))
        self.labelAvg2.config(text=str(avg2))

    def status(self, status): #Function to tell user the status of the test
        if status == False: #If we just started the test, we'll tell the user we're calibrating
            self.labelStatus.config(text="Calibrating, please wait!")
        else: #Here we are telling the user that the test is actually running and done calibrating
            self.labelStatus.config(text="Test is now running!")

root = Tk() #Creating window
myGui = GUI(root) #Creating object of class
myGui.ports() #Calling ports function to display the ports

root.mainloop() #Keeps the UI visible


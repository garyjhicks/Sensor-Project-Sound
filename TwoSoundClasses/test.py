import serial 
import time
import requests
import json
import serial.tools.list_ports
import timeit
from tkinter import *

class data: 
    def loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2, avg, avg2): 
        
        try: 
            
            distance = ser.readline().decode().replace('\n', '') 
            distance2 = ser.readline().decode().replace('\n', '') 
            
            if start < 30 and distance != "" and distance != 0 and distance2 !="" and distance2 !=0: 
            
                if start == 0: 
                    object.status(False) 
                elif start == 29: 
                    object.status(True) 
                start+=1 
                
                if start<5: 
                    modifier = float(distance)
                    modifier2 = float(distance2)
                
                elif start>=5: 
                    modifier = self.average(modifier, distance) 
                    modifier2 = self.average(modifier2, distance2) 
            
            if distance != "" and distance2 != "" and start == 30 : 
                
                distance = str(float(distance) - float(modifier)) 
                distance2 = str(float(distance2) - float(modifier2)) 
                
                if avg == -100.0: 
                    avg = float(distance) 
                    avg2 = float(distance2)

                else: 
                    avg = self.average(avg, distance) 
                    avg2 = self.average(avg2, distance2) 
            
                time_hhmmss = time.strftime('%H:%M:%S') 
                date_mmddyyyy = time.strftime('%d/%m/%Y') 
                
                object.change(modifier, distance, modifier2, distance2, avg, avg2) 
                
                print('D1: ' + distance + ', ' + time_hhmmss + ', ' + date_mmddyyyy) 
                print('D2: ' + distance2 + ', ' + time_hhmmss + ', ' + date_mmddyyyy)
                
                if count == 0 and sendTime != -1 : 
                    ser.write(b'0')
                    print("LED turned on!")
                
                if sendTime == count: 
                    ser.write(b'0')
                    print("LED turned off!")
                
                count+=1 
                
                if count%30 == 0: 
                    
                    data = {'date':date_mmddyyyy, 'time':time_hhmmss, 'dist':avg, 'dist2':avg2} 
                    result = requests.post(firebaseURL + '/' + urlAddition +'.json', data=json.dumps(data)) 
                    print("Sent!")
                    avg = -100.0 
                    avg2 = -100.0
                    root.after(780, lambda: self.loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2, avg, avg2))
            
            root.after(1000, lambda: self.loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2, avg, avg2))
        
        except IOError: 
            print('Error! Something went wrong.')
            root.after(1000, lambda: self.loop(self, object, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2, avg, avg2))

    def startTest(self, connections, buttons, entryTestName, entryTestLength): 
    
        firebaseURL = "https://work-5b7b6.firebaseio.com/" 
        
        connected = False 
        
        for i in range(0, len(connections)): 
            if connections[i]["text"]=="Connected.": 
                ser = serial.Serial(buttons[i]["text"], 9600, timeout=0) 
                connected = True 
                print(connections[i]["text"])
            i=+1 
        
        if not connected: 
            ser = serial.Serial('/dev/cu.usbmodem1461', 9600, timeout=0) 
            
        sendTime = -1 
        urlAddition = 'voltage'
        count = 0
        start = 0
        modifier = 0
        modifier2 = 0
        avg = -100.0
        avg2 = -100.0
        
        try:
            urlAddition = str(entryTestName.get()) 
        except (ValueError):
            print("Not a valid test name, voltage will be used.") 
        
        try:
            sendTime = int(entryTestLength.get()) 
        except (ValueError):
            print("Invalid time recieved, LED will not go off") 
        
        data.loop(data, self, firebaseURL, ser, sendTime, urlAddition, count, start, modifier, modifier2, avg, avg2) 
    
    @staticmethod
    def average(avg, new): 
        alpha=0.0645 
        avg = (alpha * float(new)) + (1.0 - alpha) * avg 
        return avg; 

class GUI(Frame): 
    
    def connect(self, i):
        print(self.buttons[i]["text"])
        self.connections[i]["text"] = "Connected." 
        
        for j in range(0, len(self.connections)): 
            if j==i: 
                continue 
            else:
                self.connections[j]["text"]="" 

    def closeWindow(self): 
        root.destroy() 
        exit() 
    
    def __init__(self, master): 
        super(GUI, self).__init__() 
        self.grid() 
        
        self.buttons = [] 
        self.connections = [] 
        
        self.labelTitle = Label(self, text = "Sash Testing With Sound") 
        self.labelTitle.grid(row=0, column = 1) 
        
        self.labelModifierStay = Label(self, text = "Modifier: ") 
        self.labelDistanceStay = Label(self, text = "Distance: ") 
        self.labelLEDStay = Label(self, text = "LED: ") 
        self.labelAvgStay = Label(self, text= "Avg: ") 
        
        self.labelModifierStay.grid(row=1, column=3, sticky=E) 
        self.labelDistanceStay.grid(row=2, column=3, sticky = E) 
        self.labelLEDStay.grid(row=3,column=3, sticky = E) 
        self.labelAvgStay.grid(row=4,column=3, sticky = E) 
        
        self.labelModifier = Label(self, text = "Value") 
        self.labelDistance = Label(self, text = "Value") 
        self.labelLED = Label(self, text = "Green") 
        self.labelAvg = Label(self, text = "Value") 
        
        self.labelModifier.grid(row=1, column=4, sticky=W) 
        self.labelDistance.grid(row=2, column=4,sticky=W) 
        self.labelLED.grid(row=3, column=4, sticky=W) 
        self.labelAvg.grid(row=4, column=4, sticky=W) 
        
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
        
        self.labelTestName = Label(self, text = "Test Name: ") 
        self.labelTestLength = Label(self, text = "Length of Test: ") 
        self.entryTestName = Entry(self) 
        self.entryTestLength = Entry(self) 
        
        self.labelTestName.grid(row=1, column=0, sticky=E) 
        self.labelTestLength.grid(row=2, column=0, sticky=E) 
        self.entryTestName.grid(row=1, column=1, sticky=W) 
        self.entryTestLength.grid(row=2, column=1, sticky=W) 
        
        self.buttonStart = Button(self, text="Start", command = lambda:data.startTest(self, self.connections, self.buttons, self.entryTestName, self.entryTestLength))
        self.buttonStart.grid(row=3, column = 0) 
        
        #Space
        self.labelSpace = Label(self, text = "             ") 
        self.labelSpace2 = Label(self, text = "             ")
        self.labelSpace3 = Label(self, text = "             ")

        self.labelSpace.grid(row=1, column = 5) 
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
        
        self.buttonExit = Button(self, text="Exit", command = self.closeWindow) 
        self.buttonExit.grid(row=4, column = 0) 
    
        self.labelStatus = Label(self, text="") 
        self.labelStatus.grid(row=5, column=0) 
    
    def ports(self): 
        
        self.ports = list(serial.tools.list_ports.comports()) 
        
        i=0 
        for self.p in self.ports: 
            
            self.port = (str(self.p)).split(" ")
            self.buttons.append(Button(self, text=self.port[0], command=lambda i=i: self.connect(i)))
            self.connections.append(Label(self, text=""))
            self.connections[i].grid(column=10, row=i+1, sticky=W)
            self.buttons[i].grid(column=9, row=i+1, sticky=W)
            print(self.p)
            i+=1

    def change(self, modifier, distance, modifier2 , distance2, avg, avg2): 
        self.labelModifier.config(text=modifier)
        self.labelDistance.config(text=distance)
        self.labelModifier2.config(text=modifier2)
        self.labelDistance2.config(text=distance2)
        self.labelAvg.config(text=str(avg))
        self.labelAvg2.config(text=str(avg2))

    def status(self, status): 
        if not status: 
            self.labelStatus.config(text="Calibrating, please wait!")
        else: 
            self.labelStatus.config(text="Test is now running!")

root = Tk() 
myGui = GUI(root) 
myGui.ports() 

root.mainloop() 


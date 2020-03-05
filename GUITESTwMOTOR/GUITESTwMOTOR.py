from tkinter import * 
from gpiozero import PWMOutputDevice as PWM, LED, Button as GP
import csv
# Needs to be imported as "hx" to work later on
#pin 38 is the data pin, pin 40 is the sclk.
from hx711 import HX711
class Window(Frame):
    #initializes parameters
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()
        self.initGPIO()
        
        
        #creates the window widget
    def init_window(self, bg= "Black"):
        self.configure(background=bg)
        self.master.title("GUItest") #parent widget
        self.pack(fill=BOTH, expand = 1) #give parent widget the whole window
        #Parameters
        self.CValue = 0
        self.CName = "PSBC"
        self.MaxCValue = 0
        self.TMaxValue = 0
        self.MaxTeamName = 'none yet'
       
        #Labels
        #separated for my own clarity, these are used to load and update the text
        self.textWeight= Label(self, bg= None, fg= 'Black', text =str(self.CValue), font = ('Arial', 80), height = 2, relief = RIDGE )
        self.textWeight.pack(side = RIGHT)
        self.tName= Label(self,bg= None, fg= 'Black', text = self.CName, font = ('Arial', 80), height = 2, relief = RIDGE )
        self.tName.pack(side = TOP)
        self.HX7 = HX711()
    

        #Buttons
        ForwardButton= Button(text= 'calibrate', command = self.selfcalibrate)  #create test button, remove and replace with GPIO button
        ForwardButton.pack(side=BOTTOM)
        BackButton= Button(text='Backward', command= self.backward) #create test button, remove and replace with GPIO button
        BackButton.pack(side=BOTTOM)
        test3= Button(text='Brake', command= self.neutral) #create test button, remove and replace with GPIO button
        test3.pack(side=BOTTOM)
        test4 = Button(text= 'Forward', command = self.forward)
        test4.pack(side=BOTTOM)

    def selfcalibrate(self):
        #we are going to use a known weight and a magic number to calibrate the load cell. no way around this.
        weight = self.HX7.getweight()
        #in this line put in the reference weight
        knownweight = 1
        #leave the rest alone, the magic happens there
        self.reference = weight/knownweight
        hx.set_reference_unit(self.reference)#this line is how you set the referencce number you divide by this
        print(self.reference)
        self.CValue = self.reference
        self.textWeight(text = '"Weight Bared = " +str(self.CValue)')
        
    def conversion(self):
        self.weight = hx.getweight()
        self.weight = self.weight * 2.2046
        
#initialize the GPIO for the new driver -_- youre welcome Israel. lol. 
    def initGPIO(self):
        
        #these are the physical number pins corresponding to the BCM pins
        pin3 = 2
        pin5 = 3
        pin7 = 4 
        pin11= 17
        pin21 = 9
        #declaring pins to be outputs. LED is digital output.
        self.R_EN = LED(pin3)
        self.R_EN.on()
        self.L_EN = LED(pin5)
        self.L_EN.on()
        self.RPWM = PWM(pin7)
        self.LPWM = PWM(pin11)
        #declare the buttons        
        #the start button requires 4 pins, ground, 5 volt, ground 2, and pin 21
        #self.Start = GP(pin21, bounce_time = self.bounce)
        #self.Stop = GP(pin19, bounce_time= self.bounce)

    #this is for the motor driver
    #its important to turn off first so that you arent forcing the motor to burn out by trying to turn left and right.
    def forward(self):
        self.LPWM.value = self.off
        self.RPWM.value = self.startspeed
        

    def backward(self):
        self.RPWM.value = self.off
        self.LPWM.value = self.startspeed

    def neutral(self):
        self.RPWM.value= self.LPWM.value = 0
        
    def fullForward(self):
        self.LPWM.value = self.off
        self.RPWM.value = self.fullspeed

    def fullBackward(self):
        self.RPWM.value = self.off
        self.LPWM.value = self.fullspeed
       
    #this is the automation in the program
#From Here on, this is the stuff that concerns the buttons.
#The bad programming starts here.
    def StartRead(self):
        self.start = None #Turn off the start button.
        ReadOp() # Not sure what this is, will investigate -Jim
                
    def TurnoffAll(self):
        self.destroy()

#From here on this is the stuff that concerns the HX711/Load Cell
    def GetValue(self):
        self.CValue = hx.getValue() #the Value straight from the ADC

    def tare(self):
        hx.tare() #It does what it says -_-


#From here on this is the stuff that concerns the Digital Potentiometer

#From here on this is the stuff that concerns running the GUI
    
    #writes data as a CSV
    def WriteCSV(self):
        with open('BridgeData.csv', 'a') as csvfile: #this is to creat/open a file, the a is to write at the end of the file.
            filewrite= csv.writer(csvfile)
            filewrite.writerow([self.c1, self.c2, self.c3])  #these are placeholders for actual variables.
            iteration = iteration + 1
     
                        #this is for reading the team name and weight of the bridge in 1st place.
    def ReadCSVMax(self):
        loopIter = -1
        with open('BridgeData.csv', 'r') as csvfile:
             read= list(csv.reader(csvfile, delimiter= ','))#fucking shit, im stuck here.
             for row in read:            
                if row:
                    self.names.append(row[0])
                    self.weights.append(row[1])
             for number in self.weights:
                loopIter += 1
                if number:
                    if loopIter == 0:
                        continue
                    if loopIter == 1:
                        self.tMaxwght= float(self.weights[loopIter])
                        self.tMaxName= self.names[loopIter]
                    else:
                         if self.tMaxwght < float(self.weights[loopIter]):
                            self.tMaxwght =float(self.weights[loopIter])   
     

root = Tk() 
root.attributes('-fullscreen', True)
app = Window(root) # creates the instance 
#this is the equivalent to while(1). 
root.mainloop()

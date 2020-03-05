from tkinter import *
from PIL import Image, ImageTk
from gpiozero import PWMOutputDevice, DigitalOutputDevice, Button
import csv

class Window(Frame):
    #initializes parameters
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()
        self.init_GPIO()
        
        
        #creates the window widget
    def init_window(self, bg= "Black"):
        self.configure(background=bg)
        self.master.title("GUItest") #parent widget
        self.pack(fill=BOTH, expand = 1) #give parent widget the whole window

        filename= PhotoImage(file= "webb-dark" )#IMPORTANT, THIS FILE LOCATION WILL CHANGE WHEN IT GOES ONTO THE PI !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        test= Button(text= 'Forward', command = self.Forward)  #create test button, remove and replace with GPIO button
        test.pack(side=BOTTOM)
        test2= Button(text='Backward', command= self.Backward) #create test button, remove and replace with GPIO button
        test2.pack(side=BOTTOM)

    def init_GPIO(self):
        #The pins that will control the Hbridge are pins 11,12,13,14. 
        #pin 12 is meant for PWM.
        self.pin12 = PWMOutputDevice(18)
        self.pin12.frequency = 60
        self.pin12.value= 0.00
        #Pins 11 and 13 are meant for motion. 11 goes to to topmost IO on the driver. 11 is IN 1
        self.pin11 = DigitalOutputDevice(17)
        self.pin11.initial_value = 0
        self.pin13 = DigitalOutputDevice(27)
        #pin15 is meant for the button to start. 


#From here on, this concerns Driver Controls.
        #Call to Move Motor Forward
    def Forward(self):
        self.pin12.value = 0.25
        self.pin13.off()
        self.pin11.on()

          #Call to Move Motor Backward      
    def Backward(self):
        self.pin12.value = 0.25
        self.pin11.off()
        self.pin13.on()

        #Call for Fullspeed Forward
    def FullForward(self):
        Forward()
        self.pin12.value=1

        #Call for Fullspeed Backward
    def FullBackward(self):
        Backward()
        self.pin12.value =1

        #Call for Brake
    def Brake(self):
        self.pin11.off()
        self.pin13.off()
        self.pin12.value= 0

        #Call for Neutral State
    def Neutral():
        self.pin12.value = 0
        self.pin11.on()
        self.pin1.on()
#From Here on, this is the stuff that concerns the buttons.
#From here on this is the stuff that concerns the HX711/Load Cell
#From here on this is the stuff that concerns the Digital Potentiometer
#From here on, this is stuff the concerns the GUI
     
     

root = Tk() 
root.attributes('-fullscreen', True)
app = Window(root) # creates the instance 
#this is the equivalent to while(1). 
root.mainloop()
from PyQt5 import QtCore, QtWidgets
from gpiozero import LED as led, PWMOutputDevice as out, Button as gp
import hx711 as hx 

QtCore.QThread = QT
#the while loop and the sleep should not stop the main window as it is running in its own thread.
#Qthreads are started using .start
class StartThread(QtCore.QThread):

    def _init_(self):
        QT._init_(self)
        self.initValues()
        self.initgpio()


    def initgpio(self):
        #bounce time is time to prevent double clicks
        bounce = 0.5
        self.PWM = .25
        #physical pins = BCM of Rpi
        pin7 = 4
        pin11 = 17
        pin13 = 27
        pin15 = 22
        self.L_EN = led(pin7)
        self.L_PWM = out(pin11, frequency = self.frequency)
        self.R_EN = led(pin13)
        self.R_PWM = out(pin15, frequency = self.frequency)
        self.L_EN.on()
        self.R_EN.on()
        #Buttons
        pin12 = 18
        pin16 = 23
        self.startB = gp(pin12, bounce_time = bounce, hold_time = 5)
        self.startB.when_pressed = self.setRunning
        self.StartB.when_held = self.turnOffProgram
        self.emergencyB = gp(pin16, bounce_time = 5)
        self.emergencyB.when_pressed = self.setEmergency

        
    def initValues(self):
        #these are to run logic
        self.running = True
        self.start = False
        self.emergency = False
        #PWM frequency
        self.frequency = 20000
        #this is PWM value
        self.value = 0  
        #logic for the switch case
        self.Forward = False
        self.Backward = False
        #initialize the HX711 class
        self.weight= HX711(dout= 38, pd_sck = 40) 
        #im not really sure how to do this so ima make up a value and Jimmy can deal with this
        self.CWeight = 0
           
    def setStart(self):
        self.start= True
        self.Forward = True
        self.start.when_pressed = disableStart

    def disableStart(self):
        self.start = False
        self.Forward = False
        self.Backward = True
        self.start.when_pressed = setStart

    def setEmergency(self):
        self.L_EN.off()
        self.R_EN.off()
        self.emergencyB.wait_for_press()            
        if self.start.is_pressed() == True:
            self.L_EN.on()
            self.R_EN.on()
        else:
            self.running == False

    def turnOffProgram(self):
        self.R_PWM.value = 0
        self.L_PWM.value = 1
        time.sleep(10)
        self.running = False
        self.L_EN.off()
        self.R_EN.off()
        value = 0
        self.R_PWM.value = self.L_PWM.value = value

        #slowly increase PWM
    def increase(self):
        self.value += 0.01

           #slowly decrease PWM
    def decrease(self):
        self.value -= 0.


    def movingAvg(self):
        #i know there are better ways to do this, but i got lazy.
        average = 0
        for x in range(0,10):
            average += self.weight.get_value_A
        average /= 10
        return average


    def run(self):
        pass1 = True
        #as long as running is true, this thread wont close.
        while self.running == True:
            #I kind of hate how i wrote this part
            if pass1 == True and self.start == True:
                pass1 = False


            if self.start == True:
                if   self.Forward == True and self.value == 1:
                     pass #This pass is going to be replaced with read from load cell code and logic.
                elif self.Forward == True:
                     self.increase()
                     pass  #this pass is also going to be replaced with read from load cell code and logic.
                elif self.Backward == True and self.value == 0:
                     pass  #this pass is also also going to be replaced with read from load cell code and logic.
                elif self.Backward == True:
                     self.decrease()
                     pass #this pass is also also also going to be replaced with read from load cell code and logic
                else:
                     #end the while loop
                     self.start == False 


            time.sleep(.5)

               
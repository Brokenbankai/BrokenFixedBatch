from gpiozero import PWMOutputDevice as PWM, LED, Button as GP #i dont know why i named it gold pieces
import hx711 as hx

class Peripherals:
    #bounce time prevents buttons from double inputs.
    bounce = 0.5
    startspeed = 0.25   
    frequency = 20000
    off = 0
    fullspeed = 1


    #this is for the hx711, which uses 5volt, GND, pin 38, and pin 40.
    def selfcalibrate(self):
        #we are going to use a known weight and a magic number to calibrate the load cell. no way around this.
        weight = hx.getweight()
        #in this line put in the reference weight
        knownweight = 1
        #leave the rest alone, the magic happens there
        self.reference = weight/knownweight
        hx.set_reference_unit(self.reference)#this line is how you set the referencce number you divide by this
        print(reference)

    def conversion(self)
        self.weight = hx.getweight()
        self.weight = self.weight * 2.2046
        
#initialize the GPIO for the new driver -_- youre welcome Israel. lol. 
    def initGPIO():
        
        #these are the physical number pins corresponding to the BCM pins
        pin3 = 2
        pin5 = 3
        pin7 = 4 
        pin11= 17
        pin21 = 9
        #declaring pins to be outputs. LED is digital output.
        self.R_EN = LED(pin3)
        self.R_EN.on()
        self.L_EN.on()
        self.L_EN = LED(pin5)
        self.RPWM = PWM(pin7)
        self.LPWM = PWM(pin11)
        #declare the buttons        
        #the start button requires 4 pins, ground, 5 volt, ground 2, and pin 21
        self.Start = GP(pin21, bounce_time = self.bounce)
        self.Stop = GP(pin19, bounce_time= self.bounce)

    #this is for the motor driver
    #its important to turn off first so that you arent forcing the motor to burn out by trying to turn left and right.
    def forward():
        self.LPWM.value = self.off
        self.RPWM.value = self.startspeed
        

    def backward():
        self.RPWM.value = self.off
        self.LPWM.value = self.startspeed

    def neutral():
        self.RPWM.value= self.LPWM.value = 0
        
    def fullForward():
        self.LPWM.value = self.off
        self.RPWM.value = self.fullspeed

    def fullBackward():
        self.RPWM.value = self.off
        self.LPWM.value = self.fullspeed
       
    #this is the automation in the program

#JIMMY, I CANT START THIS PART UNTIL I CAN SEE THE PYQT STUFF, OR ELSE IM RUNNING BLIND IN WHAT I CAN AND CANT DO LOL.


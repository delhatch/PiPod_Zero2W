import os
import RPi.GPIO as GPIO
import pygame
import csv
import Adafruit_ADS1x15
import Adafruit_GPIO

Vadj = 0.00022917  #Adjusts raw ADC value = ((4.096 / 32767) / 1.2) * 2.2

class PiPod:
    sleep = 0
    # Create a list of battery voltage values. Will use to low-pass filter the ADC values.
    lp=[]
    for i in range(15):
        lp.append(0.0)

    def __init__(self):
        # Initialize ADC
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48,busnum=1)

        # Set backlight pin as output and turn it on
        GPIO.setwarnings(False)  # disable warning because it is known that the pin is already set as output
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(26,GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO 26 = volume up
        def VolUp( channel ):
            #print("Was %s" %channel)
            volUpEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_u)
            pygame.event.post(volUpEvent)
        GPIO.add_event_detect(26,GPIO.RISING,callback=VolUp,bouncetime=100)

        GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO 13 = volume down
        def VolDown( channel ):
            volDownEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d)
            pygame.event.post(volDownEvent)
        GPIO.add_event_detect(13,GPIO.RISING,callback=VolDown,bouncetime=100)

        GPIO.setup(20,GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO 20 = up arrow
        def UpArrow( channel ):
            upEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
            pygame.event.post(upEvent)
        GPIO.add_event_detect(20,GPIO.RISING,callback=UpArrow,bouncetime=100)

        GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO 17 = down arrow
        def DownArrow( channel ):
            downEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
            pygame.event.post(downEvent)
        GPIO.add_event_detect(17,GPIO.RISING,callback=DownArrow,bouncetime=100)

        GPIO.setup(5,GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO 5 = left arrow
        def LeftArrow( channel ):
            leftEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
            pygame.event.post(leftEvent)
        GPIO.add_event_detect(5,GPIO.RISING,callback=LeftArrow,bouncetime=100)

        GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO 27 = right arrow
        def RightArrow( channel ):
            rightEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
            pygame.event.post(rightEvent)
        GPIO.add_event_detect(27,GPIO.RISING,callback=RightArrow,bouncetime=100)

        GPIO.setup(22,GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO 22 = center button
        def Return( channel ):
            returnEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
            pygame.event.post(returnEvent)
        GPIO.add_event_detect(22,GPIO.RISING,callback=Return,bouncetime=100)

        GPIO.setup(6,GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO 6 = 'sleep' button
        def Escape( channel ):
            escapeEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
            pygame.event.post(escapeEvent)
        GPIO.add_event_detect(6,GPIO.RISING,callback=Escape,bouncetime=100)

        GPIO.setup(23, GPIO.OUT)    # Backlight on/off control
        GPIO.output(23, GPIO.HIGH)

    def getStatus(self):
        status = [0, 0, 0]
        #Note: adc0 = external USB voltage
        #Note: adc1 = internal battery voltage
        adc0 = self.adc.read_adc(0, gain=1) * Vadj * 1.005 #observed adjustment
        adc1 = self.adc.read_adc(1, gain=1) * Vadj * 1.005
        self.lp.append(adc1)  # put new battery voltage reading at end of list.
        self.lp.pop(0)        # delete/remove the oldest value
        adc1 = sum(self.lp) / len(self.lp)  # calculate the average value.
        status[0] = adc0 > 4.5
        status[1] = "%.2f" % round(adc1, 2)
        status[2] = self.sleep

        return status

    def toggleSleep(self):
        if self.sleep == 0:
            GPIO.output(23, GPIO.LOW)
            self.sleep = 1
        else:
            GPIO.output(23, GPIO.HIGH)
            self.sleep = 0

    def shutdown(self):
        os.system("sudo halt now")
        return 1

    def reboot(self):
        os.system("sudo reboot now")
        return 1

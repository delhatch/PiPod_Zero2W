import os
import RPi.GPIO as GPIO
import pygame
import csv
import Adafruit_ADS1x15

class PiPod:
    sleep = 0

    def __init__(self):
        # Initialize ADC
        #DRH self.adc = Adafruit_ADS1x15.ADS1115()

        # Set backlight pin as output and turn it on
        GPIO.setwarnings(False)  # disable warning because it is known that the pin is already set as output
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20,GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO 20 = volume up
        def VolUp( channel ):
            #print("Was %s" %channel)
            upEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_u)
            pygame.event.post(upEvent)
        GPIO.add_event_detect(20,GPIO.RISING,callback=VolUp,bouncetime=100)
        GPIO.setup(23, GPIO.OUT)
        GPIO.output(23, GPIO.HIGH)

    def getStatus(self):
        status = [0, 0, 0]
        #DRH adc0 = self.adc.read_adc(0, gain=1) * (4.096 / 32767) / 1.2 * 2.2
        #DRH adc1 = self.adc.read_adc(1, gain=1) * (4.096 / 32767) / 1.2 * 2.2
        adc0 = 4.0
        adc1 = 3.9
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
        os.system("sudo halt")
        return 1

    def reboot(self):
        os.system("sudo reboot")
        return 1

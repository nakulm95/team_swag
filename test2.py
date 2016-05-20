import RPi.GPIO as GPIO
import time
import os
import RPIO



SPICLK = 15
SPIMISO = 13
SPIMOSI = 11
SPICS = 7
IRRX = 15
IRTX = 11

def main():
    init()
    while True:
        print(GPIO.input(IRRX))
##        GPIO.output(IRTX, True)
##        time.sleep(.000013)
##        GPIO.output(IRTX, False)
##        time.sleep(.000013)
        
        #v = readadc(0,SPICLK,SPIMOSI,SPIMISO,SPICS)
        #if v == 1023:
        #    print "shitz"
         #   break
        #else:
         #   print v
    #while(True):
        #if not GPIO.input(11):
            #print("shit detected")
            #time.sleep(2)
                        
def init():
    GPIO.setmode(GPIO.BOARD)
    # set up the SPI interface pins
   # GPIO.setup(SPIMOSI, GPIO.OUT)
   # GPIO.setup(SPIMISO, GPIO.IN)
   # GPIO.setup(SPICLK, GPIO.OUT)
   # GPIO.setup(SPICS, GPIO.OUT)
    GPIO.setup(IRRX, GPIO.IN)
    GPIO.setup(IRTX, GPIO.OUT)
    #GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
# vibration sensor
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
 
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

if __name__ == "__main__":
    main()

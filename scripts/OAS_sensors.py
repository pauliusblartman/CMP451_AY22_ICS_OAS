#Libraries
import sys
import time
import RPi.GPIO as GPIO
import OAS_data as data

GPIO.setmode(GPIO.BOARD)

#set GPIO Pins
#GPIO_TRIGGER = 11
#GPIO_ECHO1 = 13
GPIO_ECHO1 = 3
GPIO_ECHO2 = 5
GPIO_ECHO3 = 32
GPIO_ECHO4 = 11
GPIO_ECHO5 = 13
GPIO_ECHO6 = 26
#GPIO_ECHO2 = 15
GPIO_TRIGGER1 = 29
GPIO_TRIGGER2 = 31
GPIO_TRIGGER3 = 33
GPIO_TRIGGER4 = 35
GPIO_TRIGGER5 = 16
GPIO_TRIGGER6 = 8
#GPIO_TRIGGER7 = 22


#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER4, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER5, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER6, GPIO.OUT)

GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_ECHO3, GPIO.IN)
GPIO.setup(GPIO_ECHO4, GPIO.IN)
GPIO.setup(GPIO_ECHO5, GPIO.IN)
GPIO.setup(GPIO_ECHO6, GPIO.IN)
#GPIO.setup(GPIO_ECHO2, GPIO.IN)

def distance(i):
    #SensorName = 0
# set Trigger to HIGH
    #print(i)
    if(i == 1):
        #print("yes")
        GPIO.output(GPIO_TRIGGER1, True)
        time.sleep(0.001)
        GPIO.output(GPIO_TRIGGER1, False)
        StartTime = time.time()
        StopTime = time.time()
        #print("before while")
        while GPIO.input(GPIO_ECHO1) == 0:
            StartTime = time.time()
            #print("-o-")
    # save time of arrival
        #print("after while")
        while GPIO.input(GPIO_ECHO1) == 1:
            StopTime = time.time()
    # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance
    elif(i == 2):
        GPIO.output(GPIO_TRIGGER2, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER2, False)
        StartTime = time.time()
        StopTime = time.time()
        #print("before while")
        while GPIO.input(GPIO_ECHO2) == 0:
            StartTime = time.time()
    # save time of arrival
        while GPIO.input(GPIO_ECHO2) == 1:
            StopTime = time.time()
    # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance
    elif(i == 3):
        GPIO.output(GPIO_TRIGGER3, True)
        time.sleep(0.00001)

        GPIO.output(GPIO_TRIGGER3, False)
        StartTime = time.time()
        StopTime = time.time()
        #print("before while")
        while GPIO.input(GPIO_ECHO3) == 0:
            StartTime = time.time()
    # save time of arrival
        while GPIO.input(GPIO_ECHO3) == 1:
            StopTime = time.time()
    # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance
    elif(i == 4):
        GPIO.output(GPIO_TRIGGER4, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER4, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO4) == 0:
            StartTime = time.time()
    # save time of arrival
        while GPIO.input(GPIO_ECHO4) == 1:
            StopTime = time.time()
    # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance
    elif(i == 5):
        GPIO.output(GPIO_TRIGGER5, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER5, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO5) == 0:
            StartTime = time.time()
    # save time of arrival
        while GPIO.input(GPIO_ECHO5) == 1:
            StopTime = time.time()
    # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance
    elif(i == 6):
        
        GPIO.output(GPIO_TRIGGER6, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER6, False)
        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(GPIO_ECHO6) == 0:
            #print("vghvghvh")
            StartTime = time.time()
    # save time of arrival
        while GPIO.input(GPIO_ECHO6) == 1:
            StopTime = time.time()
    # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance


def main(top : data):
#GPIO Mode (BOARD / BCM)

    sensors_to_test = [GPIO_TRIGGER1, GPIO_TRIGGER2, GPIO_TRIGGER3, GPIO_TRIGGER4, GPIO_TRIGGER5, GPIO_TRIGGER6]
    try:
        #print ("Object Detected by Sensor ")
        while True:
            #print ("Object Detected by Sensor ")
            i = 1
            detRanges = [] # tuple for holding detection data
            for sensor in sensors_to_test:
                dist = distance(i)
                #print ("Object Detected by Sensor " + str(i) + " Measured Distance = %.1f cm" % dist)
                detRanges = detRanges + [dist]
                if(dist < 400):
                    #print("Object should be avoided")
                    pass
                i = i + 1
                time.sleep(.1)
            top.setDetectionData(detRanges)
            time.sleep(1.25)
        time.sleep(5)   

# Reset by pressing CTRL + C
    except KeyboardInterrupt:
        #print("Measurement stopped by User")
        GPIO.cleanup()


if __name__ == '__main__':
    _top = data.OAS_data()
    main(_top)

import RPi.GPIO as GPIO
import spidev
import time
import struct

import OAS_data as data


cs_proc = 18
veh_proc = 22
auto = 24
GPIO.setmode(GPIO.BOARD)
GPIO.setup(cs_proc, GPIO.OUT)
GPIO.setup(veh_proc, GPIO.OUT)
GPIO.setup(auto, GPIO.IN)

def main(top : data):



    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000
    spi.mode = 0b00

    while True:    
        #print("Hi")
        autopin = GPIO.input(auto)
    # GPIO.output(cs_proc, False)
        #tubby = spi.readbytes(4)
        #print("wasnt", tubby)
        #GPIO.output(cs_proc, True)
        #while tubby == [0L]*4:
        #    print("was", tubby)
        #    GPIO.output(cs_proc, False)
        #    tubby = spi.readbytes(4)
        #    GPIO.output(cs_proc, True)

        #print("wasnt")
        if(autopin != 1):
            print("auto != 1")
            tubby = [0]
            while tubby != [255]:
                GPIO.output(cs_proc, False)
                time.sleep(0.001)
                tubby = spi.readbytes(1)
                GPIO.output(cs_proc, True)

            
            time.sleep(.0001)
            GPIO.output(cs_proc, False)
            time.sleep(.0001)
            
            if tubby != [0]:
                tubb2 = spi.readbytes(4)
                tubb3 = spi.readbytes(4)
                ba = struct.pack("BBBB", tubb2[0], tubb2[1], tubb2[2], tubb2[3])
                ba2 = struct.pack("BBBB", tubb3[0], tubb3[1], tubb3[2], tubb3[3])
                #tvalue = int.from_bytes(tubb2, "big", signed="True")
                tvalue2 = struct.unpack("f", ba)
                tvalue3 = struct.unpack("f", ba2)
                #struct.unpack("%f", tubb2[0:3])
                print("In 1: ", tvalue2)
                print("In 2: ", tvalue3)
                
                controlData = [tvalue2, tvalue3]
                
                top.setControlData(controlData)
                #print(tvalue)
            GPIO.output(cs_proc, True)
            time.sleep(0.0001)
            GPIO.output(veh_proc, False)
            time.sleep(0.0001)
            value = -.1
            baf = bytearray(ba)
            value2 = .8
            spi.writebytes(baf)
            #ba = bytearray(struct.pack("f", tvalue2))
            baf = bytearray(ba2)
            spi.writebytes(baf)
            GPIO.output(veh_proc, True)


        elif(autopin == 1):
            tubby = [0]
            while tubby != [255]:
                GPIO.output(cs_proc, False)
                time.sleep(.001)
                tubby = spi.readbytes(1)
                GPIO.output(cs_proc, True)

            
            time.sleep(.0001)
            GPIO.output(cs_proc, False)
            time.sleep(.0001)
            #print(tubby)
            #time.sleep(.020)
            if tubby != [0]:
                tubb2 = spi.readbytes(4)
                tubb3 = spi.readbytes(4)
                tubb4 = spi.readbytes(4)
                tubb5 = spi.readbytes(4)
                tubb6 = spi.readbytes(4)
                tubb7 = spi.readbytes(4)
                ba = struct.pack("BBBB", tubb2[0], tubb2[1], tubb2[2], tubb2[3])
                ba2 = struct.pack("BBBB", tubb3[0], tubb3[1], tubb3[2], tubb3[3])
                ba3 = struct.pack("BBBB", tubb4[0], tubb4[1], tubb4[2], tubb4[3])
                ba4 = struct.pack("BBBB", tubb5[0], tubb5[1], tubb5[2], tubb5[3])
                ba5 = struct.pack("BBBB", tubb6[0], tubb6[1], tubb6[2], tubb6[3])
                ba6 = struct.pack("BBBB", tubb7[0], tubb7[1], tubb7[2], tubb7[3])
                #tvalue = int.from_bytes(tubb2, "big", signed="True")
                tvalue2 = struct.unpack("f", ba)
                tvalue3 = struct.unpack("f", ba2)
                tvalue4 = struct.unpack("f", ba3)
                tvalue5 = struct.unpack("f", ba4)
                tvalue6 = struct.unpack("f", ba5)
                tvalue7 = struct.unpack("f", ba6)
                #struct.unpack("%f", tubb2[0:3])
            #print("In 1: ", tvalue2)
            #print("In 2: ", tvalue3)
            #print("In 3: ", tvalue4)
            #print("In 4: ", tvalue5)
            #print("In 5: ", tvalue6)
            #print("In 6: ", tvalue7)
            autoData = [tvalue2[0], tvalue3[0], tvalue4[0], tvalue5[0], tvalue6[0], tvalue7[0]]
            top.setAutonomousData(autoData)
            #print(tvalue)
        GPIO.output(cs_proc, True)
        time.sleep(.0001)
        GPIO.output(veh_proc, False)
        time.sleep(0.001)
        value = -.1
        baf = bytearray(ba)
        value2 = .8
        
        powFor, powTur = top.getControlData()
    
        
        powForB = bytearray(struct.pack("f",float(powFor)))
        powTurB = bytearray(struct.pack("f",float(powTur)))
        
        #print("ba pow ", powForB)
        #print("ba Tur", powTurB)
        
        spi.writebytes(powForB)
        spi.writebytes(powTurB)
        
        #spi.writebytes(baf)
        #ba = bytearray(struct.pack("f", tvalue2))
        baf = bytearray(ba2)
        #spi.writebytes(baf)
        GPIO.output(veh_proc, True)

if __name__ == '__main__':
    top = data.OAS_data()
    main(top)

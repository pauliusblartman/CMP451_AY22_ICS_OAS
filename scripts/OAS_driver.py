


import OAS_driver
import OAS_auto as auto
import OAS_sensors as sens
import OAS_spi_interface as inte
import OAS_data as data

import threading
import time



def main():

    top = data.OAS_data()
    # create threads for each subfunction
    autoT = threading.Thread(target=auto.main, args=(top,))
    sensT = threading.Thread(target=sens.main, args=(top,))
    inteT = threading.Thread(target=inte.main, args=(top,))

    # start each thread
    #autoT.start()
    #sensT.start()
    inteT.start()
    
    while(True):
        time.sleep(0.1)
        print("Provided Control Values")
        print(top.getAutonomousData())
        print("Provided Autonomous Values")
        print(top.getAutonomousData())
        print("Sensor stuff")
        print(top.getDetectionData())

if __name__ == "__main__":
    main()


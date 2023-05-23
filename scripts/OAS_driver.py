
import OAS_driver
import OAS_auto as auto
import OAS_sensors as sens
import OAS_spi_interface as inte
import OAS_data as data

import threading



def main():

    top = data()
    # create threads for each subfunction
    #auto = threading.Thread(target=auto.main, args=(top))
    #sens = threading.Thread(target=sens.main, args=(top))
    inte = threading.Thread(target=inte.main, args=(top))

    # start each thread
    auto.start()
    sens.start()
    inte.start()


if __name__ == "__main__":
    main()


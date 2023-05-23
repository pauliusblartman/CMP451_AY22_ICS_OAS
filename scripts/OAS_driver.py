
import OAS_driver
import OAS_auto as auto
import OAS_sensors as sens
import OAS_spi_interface as inte

import threading

direct_control = []
autono_data = []


def main():
    # create threads for each subfunction
    auto = threading.Thread(target=auto.main, args=(1,))
    sens = threading.Thread(target=sens.main, args=(1,))
    inte = threading.Thread(target=inte.main, args=(1,))

    # start each thread
    auto.start()
    sens.start()
    inte.start()


if __name__ == "__main__":
    main()


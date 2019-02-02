import time
from HAP.HAP_Handler import hap_handler
import threading


def main():
    try:
        hap_handler.start()
        i = 0
        while (i < 30):
            print("running...")
            time.sleep(1)
            i += 1
        hap_handler.accessories["Blinds Left"].send_current_pos(100)
    finally:
        hap_handler.stop()
        exit(0)





if __name__ == "__main__":
    main()

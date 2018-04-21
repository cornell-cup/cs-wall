import threading
import time
import socket
import traceback


class minibotConnector(threading.Thread):
    """Sends out UDP connection to Minibot. Adapted from Minibot Basestation:
    https://github.com/cornell-cup/cs-minibot/blob/develop/basestation/bot/connection/udp_connection.py
    """

    def __init__(self):
        """
        Initializes the UDP connection socket.
        """
        #super().__init__() #Python3 super init
        super(minibotConnector, self).__init__()

        # the time (sec) before an address is removed from our list
        self.__update_threshold = 40
        self.__port = 5001
        self.__IP_list = {}
        self.__listener_socket = socket.socket(socket.AF_INET,
                                               socket.SOCK_DGRAM)
        self.__listener_socket.bind(("", self.__port))
        return

    # def get_addresses(self) -> list:
    def get_addresses(self):
        """
        Returns:
            (list): The list of IPs that have been discovered and are
                currently active.
        """

        self.__clean_addresses()
        return sorted(self.__IP_list.keys())

    def run(self):
        """
        Runs the UDP Listener, and adds the IPs of the devices that are
        broadcasting.
        """
        try:
            while True:
                data = self.__listener_socket.recvfrom(512)
                device_address = data[1][0]
                self.__IP_list[device_address] = self.__get_current_time()

        except socket.error as e:
            msg = "Unable to receive broadcasts sent to the port " + \
                  str(self.__port) + "."
            self.log_exn_info(e, msg)

        return

    def __clean_addresses(self):
        """
        Filters the IPs in the internal map that have been inactive (not
        broadcasting) for time = `self.__update_threshold`.
        """

        now = self.__get_current_time()
        new_IP_list = {}

        for address, last_updated_time in self.__IP_list.items():
            if now - last_updated_time <= float(self.__update_threshold):
                new_IP_list[address] = last_updated_time

        self.__IP_list = new_IP_list
        return

    @staticmethod
    def __get_current_time():
        """
        Returns:
            (float): Current time in seconds, since the start of epoch.
        """
        return time.time()

    def log_exn_info(e, msg=""):
        """
        Logs the information of the error message in msg with a stack traceback

        Args:
            e (exn): The exception thrown. Its traceback will be logged
            msg (str): Message to log, default is `""` (empty string)
        """
        print(msg)  # currently printing instead of logging
        print("" + "[ ERROR ]: " + e.strerror + "")
        traceback.print_tb(e.__traceback__)
        return

if __name__ == "__main__":
    test = minibotConnector()
    test.start()
    while True:
        print("List of addresses")
        for idx in range(0,len(test.get_addresses())):
            print(test.get_addresses()[idx])

from serial import *
import time
class Serializer:

    # ---------------------------------------------------constructor --------------------------------------------------------
    def __init__(self,arg_port,arg_baude_rate = 9600,arg_parity = None,arg_stopbits = None):
        # ------------------------------------- configure serial port --------------------------------------------------------
        self.mstopbits   = arg_stopbits
        self.mparity     = arg_parity
        self.mport       = arg_port
        self.mbaudrate   = arg_baude_rate
        self.ser         = Serial(port = self.mport,baudrate = self.mbaudrate,parity = self.mparity,stopbits = self.mstopbits,timeout = None)
        print( "connect to -------------->  ",self.ser.portstr)

        # ----------------------------------------check which port is really used -----------------------------------
        if self.ser.portstr == self.mport:
            pass
        else:
            raise Exception("Wrong port or device ! check your usb port")

    # ---------------------------------------- encode_data -----------------------------------------
    def encode_data(self,arg_data):
        return str.encode(arg_data)
    # ---------------------------------------- sed data via serial port -----------------------------------------

    def send_data(self,arg_data):
        #time.sleep(0.1)
        l_data = self.encode_data(arg_data + '\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(l_data)


    # ---------------------------------------- destructor , close serial port -----------------------------------------
    def __del__(self):
        self.ser.close()

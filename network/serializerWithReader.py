from network.serializer import *
import threading
import time



class SerializerWithReader(Serializer):

    # --------------------------------------------------- constructor --------------------------------------------------------
    def __init__(self,arg_port,arg_baude_rate,arg_name):

        super().__init__(arg_port,arg_baude_rate,arg_parity=PARITY_NONE,arg_stopbits=STOPBITS_ONE)
        self.mthread_name     = arg_name
        self.mthread_target   = self.read_data
        self.mthread          = threading.Thread(name=self.mthread_name,target=self.mthread_target)
        self.thread_exit_flag = False
        self.m_data           = ""
        self.coded_data       = []
        self.name             = arg_name
        #print("****************************************", self.mthread_name, " serializer Init")

    # ---------------------------------------------------append data from serial port ------------------------------------
    def read_data(self):
        #print("thread for ",self.mthread_name," started ")
        self.clean_data()
        while self.thread_exit_flag == False:
            len_data = self.ser.inWaiting()
            if len_data != 0:
                data = self.ser.read(len_data)
                self.coded_data.append(data)
                time.sleep(0.01)

    # --------------------------------------------------- start_acquisition --------------------------------------------------------

    def start_acquisition(self):
        self.thread_exit_flag = False
        self.mthread = threading.Thread(name = self.mthread_name, target = self.mthread_target)
        self.mthread.start()


    # --------------------------------------------------- getter for data --------------------------------------------------------
    def get_data(self):
        self.m_data = ""
        for line in self.coded_data:
             self.m_data = self.m_data + line.decode('utf-8')
        return self.m_data

    # --------------------------------------------------- clean buffer --------------------------------------------------------
    def clean_data(self):
        self.m_data = ""
        self.coded_data.clear()

    # ---------------------------------------------------stop acquisition --------------------------------------------------------
    def stop_acquisition(self):
        self.thread_exit_flag = True
        self.mthread.join()
        #print("thread for ",self.mthread_name," STOPPED ")

    # --------------------------------------------------- destructor --------------------------------------------------------
    def __del__(self):
        super().__del__()



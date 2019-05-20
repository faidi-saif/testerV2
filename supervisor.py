from logParser import LogParser
import time
from interfaceExplorer import InterfaceExplorer
import os


class Supervisor:

    def __init__(self,camera):
        self.camera             = camera
        self.log_parser         = LogParser()
        self.interface_explorer = InterfaceExplorer()

    # ---------------------------------------- check if firmware boots ok  ---------------------------------------------
    def isfirmwareBooted(self,arg_log_path):
        return_val = self.log_parser.extract(arg_log_path,'compiled')
        if return_val == -1:
            raise Exception(' Problem with the Firmware , not a valid firmware !')
        else:
            print("Firmware booted correctly --------------> \n")
            print(return_val)


    def wait_for_connection(self,arg_ip,arg_timeout = 50):
        time_elapsed = 0
        reset_flag = False
        while self.interface_explorer.find_by_ip(arg_ip) == False:
            time.sleep(0.1)
            print('waiting for network connection')
            time_elapsed = time_elapsed + 0.1
            if time_elapsed >= arg_timeout / 2 and reset_flag == False:
                print( " reset camera ---- > look for interfaces again")
                reset_flag = True
                self.camera.reset()
            if time_elapsed >= arg_timeout :
                return False
        print( 'Connection established to ---> {}'.format(arg_ip))
        return True


    def check_not_empty(self,arg_path):
        files = os.listdir(arg_path)
        total_size = 0
        for f in files :
            path = arg_path + '/' + f
            total_size = total_size + os.path.getsize(path)
        if total_size == 0:
            #print("Directory is empty")
            return False
        else:
            #print("Directory is not empty")
            return True



# sup = Supervisor('maker')
# sup.check_not_empty('/home/saif/Desktop/test_capt')






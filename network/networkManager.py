from network.arduinoSerializer import ArduinoSerializer
from network.sshAgent import SshAgent
from network.serializerWithReader import SerializerWithReader
from network.webServerAgent import WebServerAgent
from network.interfaceExplorer import InterfaceExplorer
import os

class NetworkManager :

    def __init__(self,username,host,ssh_passwd,arduino_port,linux_port,rtos_port):
        self.arduino_port       = arduino_port
        self.linux_port         = linux_port
        self.rtos_port          = rtos_port
        self.arduino_ser        = ArduinoSerializer(arduino_port,9600)
        self.rtos_ser           = SerializerWithReader(rtos_port,115200,"RTOS")
        self.linux_ser          = SerializerWithReader(linux_port, 115200,"LINUX")
        self.ssh_agent          = SshAgent(arg_username = username,arg_host = host,arg_passwd = ssh_passwd)
        self.wb_server          = WebServerAgent()
        self.interface_explorer = InterfaceExplorer()

    # ---------------------------------------------- ------------------------------------------
    def refresh(self):
        self.arduino_ser = ArduinoSerializer(self.arduino_port , 9600)
        self.rtos_ser = SerializerWithReader(self.linux_port , 115200, "RTOS")
        self.linux_ser = SerializerWithReader(self.linux_port, 115200, "LINUX")

    # ---------------------------------------------- ------------------------------------------
    def __del__(self):
        self.arduino_ser.__del__()
        self.rtos_ser.__del__()
        self.linux_ser.__del__()

    # ---------------------------------------------- ------------------------------------------
    def fix_web_path(self,arg_path):
        path = arg_path
        if (arg_path.find('/tmp/fuse_d') != -1):
            path = arg_path.replace('/tmp/fuse_d','')
        return path

    # --------------------------------------------------- list full path for all files in a given path--------------------------------------------------------
    def list_remote_files(self,arg_path):
        path = self.fix_web_path(arg_path)
        return  self.wb_server.list_content(path)

    # --------------------------------------------------- download a specific file by path from remote path to local_dir--------------------------------------------------------
    def download_file(self,remote_path,local_dir):

        path = self.fix_web_path(remote_path)
        if path != '':
            if not os.path.isdir(local_dir) :
                os.makedirs(local_dir )
            self.wb_server.download(path,local_dir)
        else :
            pass

    # --------------------------------------------------- download all the files from remote path to local directory-----------------------------------------------
    def download_all(self,arg_remote_path,arg_dir):
        path = self.fix_web_path(arg_remote_path)
        files = self.list_remote_files(path)
        for file in files :
            self.download_file(file,arg_dir)


            #self.download_file_by_name(path_to_file,arg_dir)






# netwk = NetworkManager(username = 'root',host = '192.168.0.202',ssh_passwd='')
# netwk.download_all('192.168.0.202:8042/DCIM/100GOPRO/','/home/saif/Desktop')


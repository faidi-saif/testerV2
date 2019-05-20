from cameraMind import CameraMind
from testEnvironment import TestEnvironment


class Vcamera :

    def __init__(self,Camera):
        '''
         mode : can be still or video
        :param Camera: hardware camera , low level access
        '''

        self.camera = Camera
        self.test_env           = TestEnvironment()
        self.mind               = CameraMind(self)
        self.mode               = None


    # ---------------------------------------------- ------------------------------------------
    def take_photo(self,arg_mode):
        '''
        :param arg_mode: a dictionary of the different params of the photo
        example :
        params = {'fps': '25', 'res': '5.6K', 'flare': '1000'}
        :return: None
        '''
        self.set_test_mode(arg_mode)
        self.mind.take_photo()


    def record_video(self,arg_mode):
        '''
       :param arg_mode: a dictionary of the different params of the video
        example :
        params = {'fps': '25', 'res': '5.6K', 'flare': '1000'}
        :return: None
        '''
        pass

    # ---------------------------------------------- ------------------------------------------
    def get_frw_version(self):
        frw_version = self.mind.get_frw_version()
        return frw_version

    # ---------------------------------------------- ------------------------------------------
    def clean_content(self,arg_path):
        '''
        ( remove all files and directories in the arg_path )
        :param arg_path: path to clean
        :return: None
        '''
        self.camera.netwk_manager.ssh_agent.execute_command('rm -rf ' + arg_path)
    # ---------------------------------------------- ------------------------------------------

    def get_files(self,source_path,target_path):
        '''
        :param source_path: path from which the fle will be downloaded , example : /DCIM/100GOPRO/
        or '/tmp/fuse_d/DCIM/100GOPRO/'
        :param target_path: path for the downloaded file example : /logs ( for jenkins )
        :return: None
        '''
        complete_path = self.camera.host_ip + ':' + str(self.camera.web_port) + source_path
        #192.168.0.202:8042/tmp/fuse_d/DCIM/100GOPRO/
        self.camera.netwk_manager.download_all(complete_path,target_path)


    # ---------------------------------------------- ------------------------------------------
    def ls_files(self,arg_path):
        '''
        :param arg_path: path for files to be listed example : /tmp/fuse_d/DCIM/100GOPRO/
        :return: names of the files in the arg_path
        '''
        files = self.camera.netwk_manager.ssh_agent.execute_command('ls ' + arg_path)
        print(files)
        return files


    def get_file_stat(self,arg_path):
        '''
        :param arg_path: path to the searched file   : /tmp/fuse_d/DCIM/100GOPRO/GH010197.MP4
        :return: dictionnary containing, the size , name and permissions of the file
        example : {'file': '/tmp/fuse_d/DCIM/100GOPRO/GH010197.MP4', 'size': '27.8M', 'permission': '-rwxr-xr-x'}
        '''
        status = self.camera.netwk_manager.ssh_agent.execute_command('ls -lh '+ arg_path)
        status = status.split()
        # status = ['-rwxr-xr-x', '1', 'root', 'root', '27.8M', 'Jan', '3', '00:27', '/tmp/fuse_d/DCIM/100GOPRO/GH010197.MP4']
        stat = {'file' : status[8] , 'size' : status[4] ,'permission' :status[0]}
        return stat

     # ---------------------------------------------- ------------------------------------------

    def get_results(self, arg_path):
         if arg_path != '':
             # affectation de la variable tes_env_target_dir doit etre mise dans set_test_mode
             self.test_env.download_target_dir = arg_path
         self.mind.get_results(self.test_env.download_target_dir)


    # ---------------------------------------------- ------------------------------------------

    def get_file(self,source_path,target_path):
     '''
     :param source_path: path from which the fle will be downloaded , example : /DCIM/100GOPRO/
     or '/tmp/fuse_d/DCIM/100GOPRO/'
     :param target_path: path for the downloaded file example : /logs ( for jenkins )
     :return: None
     '''
     complete_path = self.camera.host_ip + ':' + str(self.camera.web_port) + source_path
     self.camera.netwk_manager.download_file(complete_path,target_path)

    # ---------------------------------------------- ------------------------------------------
    def get_status(self):
        return self.camera.get_status()

    # ---------------------------------------------- ------------------------------------------
    def get_test_mode(self):
        test_ev = self.test_env.get_environment()
        if self.mode == 'still':
            del test_ev['run_time']
        return test_ev

    # ---------------------------------------------- ------------------------------------------
    def set_test_mode(self,arg_dict_mode):
        self.test_env.set_environment(arg_dict_mode)


    # ---------------------------------------------- ------------------------------------------
    def reboot(self,arg_reboot_option):
        '''
        :param arg_reboot_option: to reboot the camera after a power cut or using gpdevSendCmd RB
        # for hard reboot we use power_on() from arduino class since it's based on  power cut using
        the 'ykushxs' device
        :return: None
        '''
        arg_reboot_option =arg_reboot_option.strip()
        assert(arg_reboot_option == 'hard' or arg_reboot_option =='soft') , ' Invalid reboot option ,  must be "soft " or " hard "'
        if arg_reboot_option == 'hard' :
            self.camera.netwk_manager.arduino_ser.reboot()
        elif arg_reboot_option == 'soft':
            self.camera.netwk_manager.ssh_agent.execute_command(self.mind._soft_reboot)


    # ---------------------------------------------- ------------------------------------------
    def reset(self,arg_mode):
        '''
        :param arg_mode: reset mode can be 'soft' or 'hard'
        :return: None
        '''
        arg_mode = arg_mode.strip()
        assert(arg_mode == 'soft' or arg_mode =='hard') , 'Invalid reset option , must be "soft" or "hard" '
        if arg_mode == 'soft':
            self.camera.soft_reset()
        else :
            self.camera.hard_reset()

    def is_ready(self,*arg_net_interfaces,arg_timeout = 30):
        """

        :param arg_net_interfaces: serial or ssh
        :param arg_timeout: maximum time took to check for the availability of the interfaces
        :return: boolean = True when interface(s) are available
        """
        return self.camera.is_ready(*arg_net_interfaces,arg_timeout=arg_timeout)

    # ---------------------------------------------- ------------------------------------------
    def start_acquisition(self):
        self.camera.start_acquisition()

    # ---------------------------------------------- ------------------------------------------
    def stop_acquisition(self):
        self.camera.stop_acquisition()

    # ---------------------------------------------- ------------------------------------------
    def get_data(self):
        '''
        :return: linux and rtos serial logs
        '''
        return self.camera.get_data()











#cam.get_files('/DCIM/100GOPRO/','/home/saif/Desktop/')
#cam.get_files('/tmp/fuse_d/DCIM/100GOPRO/','/home/saif/Desktop/') # cammed also this way
#print(cam.get_file_stat('/tmp/fuse_d/DCIM/100GOPRO/GH010197.MP4'))
#cam.clean_content('/tmp/fuse_d/DCIM/100GOPRO/*')
#cam.get_results('/home/saif/Desktop/test_capt')

#print (vcam.get_frw_version())
# f ={'fps': '6', 'res': 'rien', 'flare': '1000'}
# cam.set_test_mode(f)
# print(cam.get_test_mode())

# ----------------------------------------------  test : take_photo------------------------------------------
# f ={'fps': '25', 'res': '5.6K', 'flare': '1000'}
# vcam.take_photo(f)
import time
import os

class CameraMind :

    def __init__(self,vcamera):
        '''
        i'm the camera brain
        :param vcamera: vcamera asks me how to run such a scenario i can control here to do any action

        sleep actions in the action tables are for waiting the execution of the command on the rtos and getting the log from serial ports
        must adjust the delay according to the action to be executed

        '''
        self.test_mode        = '' # mode genrated for each test , example : 5.6K_EAC_25_W_HEVC_IMX577
        self.vcamera          =  vcamera
        self._version         = ['t dbg on','sleep 0.2','t version','sleep 0.2', 't dbg off','sleep 0.2']
        self._soft_reboot     = '/usr/local/gopro/bin/gpdevSendCmd RB &'


    # ---------------------------------------------- ------------------------------------------
    def get_cmds(self,arg_name):
        '''

        :param arg_name: name of the cmds list which can be a value of : 'setup' ,'pre_still' ,'still' , 'post_still'
        :return: a list of comands
        '''
        arg_name = arg_name.strip()
        setup                 = [
                                "t appc status disable", # gui off
                                "sleep 3",
                                "t frw cpu_boost enable",
                                "t hal act9150 reg 0x32 0x2C",
                                "t hal act9150 reg 0x33 0x2C",
                                "t hal mxm_coreclk_ctrl set_freq 660000000",
                                "t dbg off",
                                "sleep 0.5",
                                "t frw test disp_id 0",
                                "t frw test open",
                                "t frw audproc enable_awe 0",
                                "t frw stitch flare_fake_dsp_sleep "+self.vcamera.test_env.flare_fake+" "+self.vcamera.test_env.flare_fake_time,
                                "t frw stitch ring_high_res "+self.vcamera.test_env.ring_use_high_res
                                 ]
        pre_still             = [
                                "t dbg off",
                                "t frw stitch stub enable",
                                "t frw test mode " + self.test_mode ,
                                "sleep 0.1",
                                "t frw test graph still_spherical",
                                "t frw test liveview",
                                "sleep 1.5",
                                "t dbg "+self.vcamera.test_env.verbose
                                ]

        still                 = [
                                "t frw test mode PHOTO_18MP_30_W_IMX577"
                                ]

        post_still            = [
                                "sleep 0.5",
                                "t frw stitch stub disable",
                                "t frw test still",
                                "sleep 4",
                                "t frw test stop_still",
                                "sleep 2",
                                "t dbg off",
                                "t frw test mode " + self.test_mode,
                                "t frw stitch stub enable",
                                "t frw test liveview"
                                ]
        if arg_name == 'setup' :
            return setup
        elif arg_name == 'pre_still' :
            return pre_still
        elif arg_name == 'still':
            return still
        elif arg_name == 'post_still':
            return post_still
        else :
            raise Exception ( ' No command list associated to {}'.format(arg_name))



    # ---------------------------------------------- ------------------------------------------
    def find_cmd_type(self,arg_cmd):
        '''
        :param arg_cmd: command to be executed
        :return: type of the command which take one of these values [ tcmd , sleep , shell ]
        '''
        assert (type(arg_cmd) is str),'command must be of type str '
        arg_cmd = arg_cmd.lstrip()
        if arg_cmd.startswith('t ') :
            cmd_type = 'tcmd'
        elif arg_cmd.startswith('sleep'):
            cmd_type = 'sleep'
        else:
            cmd_type = 'shell'
        return cmd_type

    # ---------------------------------------------- ------------------------------------------

    def execute(self,arg_cmd):
        '''
        :param arg_cmd: a command to be executed by camera
        :return:  type of the command ( tcmd , sleep ... )
        '''
        cmd = self.find_cmd_type(arg_cmd)
        if cmd == 'tcmd':
            self.vcamera.camera.tcmd(arg_cmd)
            #print('tcmd ' + arg_cmd )
        elif cmd == 'sleep':
            duration = float(arg_cmd.split()[1])
            time.sleep(duration)
            #print('sleep ' + str(duration)  )
        else :
            print('command not recognized ----------------> !!! '+ arg_cmd)
            pass


    # ---------------------------------------------- ------------------------------------------
    def run_scenario(self,arg_cmd_list):
        '''
        :param arg_cmd_list: list of commands to eb executed
        :return: None
        '''
        for cmd in arg_cmd_list :
            #print(cmd)
            time.sleep(0.3)  # time given to each command to be sent on serial port  , test with 0.1s fails
            self.execute(cmd)





# ---------------------------------------------- ------------------------------------------
    def get_results(self,arg_result_path):
        '''
        1 - list all the files in the tmp/fuse_d/DCIM/100GOPRO/
        2 - deactivate the logs
        3 - save all the files in the directory  arg_result_path
        4 - clean the directory /tmp/fuse_d/DCIM/100GOPRO/ on the camera
        :param arg_result_path: path where to save the video or photo tested
        :return:
        '''
        self.vcamera.ls_files('/tmp/fuse_d/DCIM/100GOPRO/')
        self.vcamera.camera.tcmd('t dbg off')
        self.vcamera.get_files('/tmp/fuse_d/DCIM/100GOPRO/',arg_result_path)
        self.vcamera.clean_content('/tmp/fuse_d/DCIM/100GOPRO/*')


# ---------------------------------------------- ------------------------------------------
    def get_frw_version(self):
        '''
        :return: the version of the firmware, example : Release H19.03.00.07.00 compiled Apr 30 2019, 13:45:03 git-286fc0746-dirty
        '''
        self.vcamera.camera.start_acquisition()
        self.run_scenario(self._version)
        # delay is handled in the _version table
        self.vcamera.camera.stop_acquisition()
        log = self.vcamera.camera.get_data()[1]
        pos = log.find('Release')
        log = log[pos:pos+74] # 74 char from the position of the word 'Release'
        return log



    # ---------------------------------------------- ------------------------------------------
    def generate_mode(self):
        '''

        :return: mode generated from test_env of the camera ,example : 5K_EAC_30_W_HEVC_IMX577
        in = f ={'fps': '25', 'res': '5.6K', 'flare': '1000'}
        out = 5.6K_EAC_25_W_HEVC_IMX577
        '''
        self.test_mode  = self.vcamera.test_env.res + '_' + self.vcamera.test_env.stitch_mode + '_' +self.vcamera.test_env.fps \
        + '_W_' + self.vcamera.test_env.encoder + '_'+  self.vcamera.test_env.sensor


    # ---------------------------------------------- ------------------------------------------
    def generate_sceanrio(self,*args):
        '''
        :param args: lists of elementary scenario
        :return: a scenario of all the elementary scenarios
        example > in [1 ,2] ; [3 , 4]
                > ou [1 ,2 ,3 ,4 ]
        '''
        scenario = []
        for el_sc in args :
            scenario[len(scenario):len(scenario)] = el_sc
        return scenario


    # ---------------------------------------------- ------------------------------------------
    def take_photo(self):
        '''
        1 - updates the mode of the test based on the vaues of the test_env
        2 - run the list of commands
        :return:None
        '''
        self.generate_mode()
        scenario =self.generate_sceanrio(self.get_cmds('setup') ,self.get_cmds('pre_still') ,
                                         self.get_cmds('still'),self.get_cmds('post_still'))
        self.run_scenario(scenario)
        # for el in scenario :
        #     print(el)



#s_exec.execute('sleep    4')


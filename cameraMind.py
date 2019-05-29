import time
from cameraConfig import CameraConfig
import os

class CameraMind :

    def __init__(self,v_camera):
        '''
        i'm the camera brain
        :param vcamera: vcamera asks me how to run such a scenario i can control here to do any action

        sleep actions in the action tables are for waiting the execution of the command on the rtos and getting the log from serial ports
        must adjust the delay according to the action to be executed

        '''
        self.conf             = CameraConfig()
        self.test_mode        = '' # mode genrated for each test , example : 5.6K_EAC_25_W_HEVC_IMX577
        self.still_mode       = ''
        self.vcamera          =  v_camera
        self._version         = ['t dbg on','sleep 0.2','t version','sleep 0.2', 't dbg off','sleep 0.2']
        self._soft_reboot     = '/usr/local/gopro/bin/gpdevSendCmd RB &'


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
        self.vcamera.is_ready('ssh','serial',arg_timeout=40)
        self.vcamera.ls_files('/tmp/fuse_d/DCIM/100GOPRO/')
        self.vcamera.camera.tcmd('t dbg off')
        self.vcamera.get_files('/tmp/fuse_d/DCIM/100GOPRO/',arg_result_path)
        #self.vcamera.clean_content('/tmp/fuse_d/DCIM/100GOPRO/*')



    # ---------------------------------------------- ------------------------------------------
    def cleanup(self):
        self.vcamera.camera.soft_reset()
        self.vcamera.is_ready('ssh', arg_timeout=80)
        self.vcamera.clean_content('/tmp/fuse_d/DCIM/100GOPRO/*')
        self.vcamera.ls_files('/tmp/fuse_d/DCIM/100GOPRO/')


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
            time.sleep(0.3)
            #print('tcmd ' + arg_cmd )
        elif cmd == 'sleep':
            duration = float(arg_cmd.split()[1])
            time.sleep(duration)
            #print('sleep ' + str(duration)  )
        else :
            print('command "{}" not known ----------------> !'.format(arg_cmd))
            pass


    # ---------------------------------------------- ------------------------------------------
    def run_scenario(self,arg_cmd_list):
        '''
        :param arg_cmd_list: list of commands to eb executed
        :return: None
        '''
        for cmd in arg_cmd_list :
            print(cmd)
            #time.sleep(0.3)  # time given to each command to be sent on serial port  , test with 0.1s fails ---> remove inside execute
        # for co in arg_cmd_list :
        #     self.execute(co)



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



    def run(self,camera_mode):
        scenario = []
        if camera_mode == 'preview':
            scenario = scenario + self.preview()
        elif camera_mode == 'still':
            scenario = scenario + self.take_photo()
        elif camera_mode == 'video':
            scenario = scenario + self.record_video()
        else :
            raise Exception('{} is not a valid camera mode'.format(camera_mode))

        self.run_scenario(scenario)

    # ---------------------------------------------- ------------------------------------------
    def take_photo(self):
        '''
        1 - updates the mode of the test based on the values of the conf
        2 - run the list of commands
        :return:None
        '''
        still_cmds = []
        pre_still       = self.pre_still_cmds()
        flare_cmd       = self.get_flare_cmds()
        ring_cmd        = self.get_ring_cmds()
        dump_raw_cmd    = self.get_dump_raw_cmds()
        debug_dump_cmd  = self.get_debug_dump_cmds()
        tag_cmd         = self.get_still_cmds()
        post_still      = self.post_still_cmds()
        still_cmds      = still_cmds + pre_still + still_cmds + flare_cmd + ring_cmd + dump_raw_cmd + debug_dump_cmd + tag_cmd + post_still
        return still_cmds

    # ---------------------------------------------- ------------------------------------------
    def pre_still_cmds(self):
        pre_still =[]
        if self.conf.shooting_mode =='spherical':
            cmd = 't frw test graph still_spherical'
        elif self.conf.shooting_mode =='non_spherical':

            cmd = 't frw test graph still'
        else : # en dual fix it later
            cmd = 't frw test graph still_spherical'
        pre_still.append(cmd)
        return pre_still

    # ---------------------------------------------- ------------------------------------------
    def post_still_cmds(self):
        post_still =['t frw test still','sleep 4','t frw test stop_still']
        return  post_still

    # ---------------------------------------------- ------------------------------------------
    def get_still_cmds(self):
        cmd = []
        cmd.append('t frw test mode {}'.format(self.generate_tag('still')))
        return cmd



    # ---------------------------------------------- ------------------------------------------
    def record_video(self):
        self.check_conf('video')
        pre_video_cmds  =  self.pre_video_cmds()
        flare_cmd       =  self.get_flare_cmds()
        stab_cmd        =  self.get_stab_cmds()
        ring_cmd        =  self.get_ring_cmds()
        exposure_cmd    =  self.get_exposure_cmds()
        debug_dump_cmds =  self.get_debug_dump_cmds()
        vid_cmds        =  self.get_videos_cmds()
        video_cmds = pre_video_cmds + ring_cmd + flare_cmd + stab_cmd  + exposure_cmd + debug_dump_cmds + vid_cmds
        return video_cmds

    # ---------------------------------------------- ------------------------------------------
    def pre_video_cmds(self):
        cmd = []
        if self.conf.shooting_mode =='spherical':
            cmd =['t frw test graph video_spherical']
        elif self.conf.shooting_mode =='non_spherical':
            if self.conf.options_mode['rear'] == 'enable':
                cmd.append('t frw test graph video_rear')
            else : # disable
                cmd.append('t frw test graph video')
        return cmd

    # ---------------------------------------------- ------------------------------------------
    def get_videos_cmds(self):
        cmd = ['t frw test start_video','sleep {}'.format(self.conf.options_mode['run_time']),'t frw test stop_video']
        return cmd


    # def post_video_cmds(self):
    #     pass


    # ---------------------------------------------- preview ------------------------------------------
    def preview(self):
        prev_cmds = ['t appc status disable','sleep 4','t dbg on ','t frw test open']
        self.check_conf('preview')
        tag = self.generate_tag('preview')
        prev_cmds.append('t frw test mode {}'.format(tag))
        prev_cmds.append('t frw test liveview')
        return prev_cmds

    # ---------------------------------------------- get_flare_cmds ------------------------------------------
    def get_flare_cmds(self):
        cmd = []
        if self.conf.options_mode['flare'] == '0':
            cmd.append('t frw stitch flare disable')
        else :# flare = 1 or flare  = 2
            cmd.append('t frw stitch flare enable')
            if self.conf.options_mode['flare'] == '2':
                cmd.append('t frw stitch flare_art_cor enable {} {}'.format(self.conf.options_mode['flare_art_front_corr'],self.conf.options_mode['flare_art']))
            else : # flare = 1
                cmd.append('t frw stitch flare_art_cor disable')
        # finally
        cmd.append('t frw stitch flare_fake_dsp_sleep {} {}'.format(self.conf.options_mode['flare_fake'],self.conf.options_mode['flare_fake_time']))
        return cmd

    # ----------------------------------------------get_stab_cmds ------------------------------------------
    def get_stab_cmds(self):
        cmd = []
        if self.conf.options_mode['stab'] == 'disable':
            pass
        else :
            if self.conf.options_mode['spher_eis'] == '0':
                cmd.append('t frw stitch eis 0 0 0 0 0 0 0')
            else :
                cmd.append('t frw stitch eis {} 0 5 1 1 0 0'.format(self.conf.options_mode['stab_degree']))
        return cmd

    # ---------------------------------------------- get_ring_cmds ------------------------------------------
    def get_ring_cmds(self):
        cmd = []
        cmd.append('t frw stitch ring_high_res {}'.format(self.conf.options_mode['ring_high_res']))
        return cmd

    # ---------------------------------------------- get_exposure_cmds ------------------------------------------
    def get_exposure_cmds(self):
        cmd = []

        return cmd

    # ---------------------------------------------- get_debug_dump_cmds ------------------------------------------
    def get_debug_dump_cmds(self):
        cmd = []
        if self.conf.options_mode['debug_dump'] == 'enable':
            if self.conf.options_mode['debug_dump_opt'] != "":

                dump_opt  =  ['--' + el for el in self.conf.options_mode['debug_dump_opt'].split(',')]
                options   = ''.join(dump_opt)
                cmd.append('t frw stitch dump enable {}'.format(options))
        else: # debug_dump = disable
            cmd.append('t frw stitch dump disable')
        return cmd

    # ---------------------------------------------- ------------------------------------------
    def get_dump_raw_cmds(self):
        cmd = []
        if self.conf.options_mode['dump_raw'] == 'enable':
            cmd = ['t frw cal raw {}'.format(self.conf.options_mode['raw_nbits']) , 't frw cal bayer_width {}'.format(self.conf.options_mode['bayer_width'])]
        return cmd




    # ---------------------------------------------- generate_tag ------------------------------------------
    def generate_tag(self,arg_mode):
        '''
        :param arg_mode: 'preview or still'
        :return:  tag associated to the test case
        '''
        # tags with LP and REAR are not handled yet
        assert(arg_mode == 'preview' or arg_mode == 'still'),'invalid mode to generate a tag'
        tag = ''
        if arg_mode == 'preview' :

            tag = self.conf.params_mode['resolution'] + '_' + self.conf.params_mode['stitch_mode'] + '_' + self.conf.params_mode['fps'] \
            + '_W_' + self.conf.encoder
            # -------------handling LRV-------
            if self.conf.options_mode['lrv'] == 'disable':
                tag =tag + '_NO_LRV'
            tag  = tag + '_' +  self.conf.sensor # 5K_EAC_25_W_HEVC_IMX577 or 5K_EAC_30_W_HEVC_NO_LRV_IMX577
            # -------------handling BYPASS-------
            if self.conf.options_mode['bypass'] == 'enable':
                tag = tag + '_' + 'BYPASS' # 4K_ERP_24_W_IMX577_BYPASS
            # -------------handling SPLIT-------
            if self.conf.options_mode['eac_split'] == 'enable':
                tag = tag + '_' +'SPLIT'  # 5K_EAC_30_W_HEVC_IMX577_SPLIT or 5K_EAC_30_W_HEVC_IMX577_BYPASS_SPLIT
            if self.conf.options_mode['rear'] == 'enable': # add REAR if rear = enable else don't add tag
                tag = tag + '_' + 'REAR'


        elif arg_mode =='still' :

            tag = 'PHOTO_' + self.conf.options_mode['mpx'] + '_' + self.conf.params_mode['fps'] + '_W_' + self.conf.sensor # PHOTO_18MP_30_W_IMX577
            if self.conf.shooting_mode == 'non_spherical':
                if self.conf.params_mode['submode'] == 'PANO':
                    tag = tag + '_' + 'PANO' # PHOTO_6MP_30_W_IMX577_PANO

            elif  self.conf.shooting_mode == 'dual':
                tag = tag + '_' + 'DUAL'  #  PHOTO_18MP_30_W_IMX577_DUAL
                if self.conf.params_mode['submode'] == 'CAL':
                    tag = tag + '_' + 'CAL' #PHOTO_12MP_30_W_IMX577_DUAL_CAL
            else : # spherical
                pass
            if self.conf.options_mode['bypass'] == 'enable':
                tag = tag + '_' + 'BYPASS'  #  PHOTO_6MP_30_W_IMX577_PANO_BYPASS or PHOTO_6MP_30_W_IMX577_BYPASS or PHOTO_6MP_30_W_IMX577_DUAL_BYPASS or  PHOTO_18MP_30_W_IMX577

        return tag

    # ---------------------------------------------- ------------------------------------------
    def check_conf(self,arg_mode):
        '''

        :param arg_mode: preview , still or video
        :return:
        1- check shooting mode
        2- check params :
        3- check options
        '''
        self.check_shooting_mode(arg_mode)
        self.check_params(arg_mode)
        self.check_options(arg_mode)




    # ---------------------------------------------- check_shooting_mode ------------------------------------------
    def check_shooting_mode(self,arg_mode):
        if arg_mode == 'preview':
            assert (self.conf.shooting_mode == 'lcd' or self.conf.shooting_mode == 'wifi'), 'invalid shooting_mode for preview'
        elif arg_mode == 'still':
            assert ( self.conf.shooting_mode == 'spherical' or self.conf.shooting_mode == 'non_spherical' or self.conf.shooting_mode == 'dual'), 'invalid shooting_mode for still'
        elif arg_mode =='video' : #video
            assert (self.conf.shooting_mode == 'spherical' or self.conf.shooting_mode == 'non_spherical' or self.conf.shooting_mode == 'dual'), 'invalid shooting_mode for video'
        else  :
            raise Exception('{} is an invalid camera mode '.format(arg_mode))


    # ---------------------------------------------- check_params ------------------------------------------
    def check_params(self, arg_mode):

        # ---------------------------------------------- > preview
        if arg_mode == 'preview':
            # check fps
            assert (self.conf.params_mode['fps'] == '24' or self.conf.params_mode['fps'] == '25' or
                    self.conf.params_mode['fps'] == '30' or
                    self.conf.params_mode['fps'] == '50' or self.conf.params_mode['fps'] == '60'), 'invalid fps value'

            if self.conf.shooting_mode == 'wifi':
                assert (self.conf.params_mode['submode'] == 'streamed' or self.conf.params_mode[
                    'submode'] == 'encoded' or
                        self.conf.params_mode['submode'] == 'mixed'), 'invalid submode for preview {wifi} mode'
            else: #lcd
                pass
            # check stitch_mode
            assert(self.conf.params_mode['stitch_mode'] == 'EAC' or self.conf.params_mode['stitch_mode'] == 'ERP')
            # check_resolution
            assert (self.conf.params_mode['resolution'] == '5K' or self.conf.params_mode['resolution'] == '4K' or self.conf.params_mode['resolution'] == '3K'
                    or self.conf.params_mode['resolution'] == 'QXGA' or self.conf.params_mode['resolution'] == 'FHD')
        # ---------------------------------------------- > video
        #elif arg_mode == 'video':
            #spherical
            # if self.conf.shooting_mode == 'spherical':
            #     assert (self.conf.params_mode['fps'] != '50'),'fps = 50 not a valid value for video/spherical '
            #     assert (self.conf.params_mode['stitch_mode'] == 'ERP' or self.conf.params_mode['stitch_mode'] == 'EAC'), 'invalid stitch_mode'
            # # non_spherical
            # elif self.conf.shooting_mode == 'non_spherical':
            #     assert (self.conf.params_mode['resolution'] == '1080' or self.conf.params_mode[
            #         'resolution'] == '1440'), 'invalid resolution'
            # dual
            # else:
            #     pass

        # ---------------------------------------------- > still
        elif arg_mode == 'still':
            # non_spherical
            if self.conf.shooting_mode == 'non_spherical':
                assert (self.conf.params_mode['submode'] == 'PANO' or self.conf.params_mode['submode'] == 'BURST' or
                        self.conf.params_mode['submode'] == 'NORMAL'), 'invalid submode for still {non_spherical} mode'
            # spherical
            elif self.conf.shooting_mode == 'spherical':
                assert(self.conf.params_mode['stitch_mode'] == 'ERP' and self.conf.params_mode['resolution'] == '6K')
            # dual
            else : # dual
                assert ()
                pass

    # ----------------------------------------------check_options ------------------------------------------
    def check_options(self,arg_mode):
        '''
        :param arg_mode: preview ,still or video
        :return:
        '''
        # ------------------------is_number-------------------------
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        # -----------------------assert_on_off-----------------------
        def assert_on_off(**kwargs):
            for key,value  in kwargs.items() :
                assert(value == 'enable' or value== 'disable'),'{} must be equal to : "enable" or "disable"'.format(key)
        # ---------------------------------------------- >common

        # ---------------------------------------------- > video
        if  arg_mode == 'video':
            # check on/off options
            assert_on_off(
                            stab             =  self.conf.options_mode['stab'],
                            ring_high_res    =  self.conf.options_mode['ring_high_res'],
                            exposure         =  self.conf.options_mode['exposure'],
                            debug_dump       =  self.conf.options_mode['debug_dump'])
            # check value for flare
            assert( self.conf.options_mode['flare'] == '0' or self.conf.options_mode['flare'] == '1' or self.conf.options_mode['flare'] == '2')
            if self.conf.options_mode['flare'] != '0':
                assert(self.conf.options_mode['flare_art'] == 'random' or self.conf.options_mode['flare_art'] == 'identity' or
                       self.conf.options_mode['flare_art'] == 'strong' or self.conf.options_mode['flare_art'] == 'lite' )
            # check stab degree
            if self.conf.options_mode['stab'] == 'enable':
                if is_number(self.conf.options_mode['stab_degree']) == False:
                    raise Exception('invalid value for stab_degree ')
            # check rear for non_spherical
            if self.conf.shooting_mode == 'non_spherical':
                assert_on_off(rear = self.conf.options_mode['rear'])
            # check for run_time
            if is_number(self.conf.options_mode['run_time']) == False:
                raise Exception('invalid value for run_time , it must be a float')
            # check debug_dump_opt ...

        # ---------------------------------------------- > preview
        elif arg_mode == 'preview':
            # if in mode preview we precise rear ---> it must be enable or disable
            assert_on_off(eac_split   = self.conf.options_mode['eac_split']
                          ,lrv        = self.conf.options_mode['lrv'],
                           bypass     = self.conf.options_mode['bypass'])
            if self.conf.options_mode['rear'] != '' :
                assert_on_off(rear = self.conf.options_mode['rear'])
            pass
        # ---------------------------------------------- > still
        else : #still
            # check on/off options
            assert_on_off(
                          bypass        = self.conf.options_mode['bypass'],
                          ring_high_res = self.conf.options_mode['ring_high_res'],
                          dump_raw      = self.conf.options_mode['dump_raw'],
                          debug_dump    = self.conf.options_mode['debug_dump'])
            # check value for flare
            assert( self.conf.options_mode['flare'] == '0' or self.conf.options_mode['flare'] == '1' or self.conf.options_mode['flare'] == '2')
            if self.conf.options_mode['flare'] != '0':
                assert(self.conf.options_mode['flare_art'] == 'random' or self.conf.options_mode['flare_art'] == 'identity' or
                       self.conf.options_mode['flare_art'] == 'strong' or self.conf.options_mode['flare_art'] == 'lite' )
            # check rear for non_spherical
            if self.conf.shooting_mode == 'non_spherical':
                assert_on_off(rear  = self.conf.options_mode['rear'])
            # check bayer_width and raw_nbits
            if self.conf.options_mode['dump_raw'] == 'enable':
                if is_number(self.conf.options_mode['bayer_width']) == False:
                    raise Exception('invalid value for bayer_width ')
                if is_number(self.conf.options_mode['raw_nbits']) == False:
                    raise Exception('invalid value for raw_nbits  ')
            # check debug_dump_opt ...








#s_exec.execute('sleep    4')


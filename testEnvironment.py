import os

class TestEnvironment:

    def __init__(self):
        '''
        for each environment variable added :
        1- add it in the dictionary env ( self.env )
        2- add a getter and a setter
        3- add it in the setter of self.env
        '''
    # ----------------------------------------------- default config  -----------------------------------------

        self._ring_use_high_res     = 'enable'
        self._flare_fake_time       = '0'
        self._flare_id_front_corr   = '50'
        self._flare_fake            = 'disable'
        self._download_target_dir   = os.environ['HOME'] + '/Desktop/test_capt'
        self._lrv                   = ''
        self._stub                  = 'disable'
        self._verbose               = 'off'
        self._run_time              = '5'
        self._fps                   = '30'
        self._res                   = '5K'
        self._flare                 = '0'
        self._liveview              = 'on'
        self._stitch_mode           = 'EAC'
        self._sensor                = 'IMX577'
        self._encoder               = 'HEVC'


    #----------------------------------------------- getters -------------------------------------------------

    @property
    def sensor(self):
        return self._sensor

    @property
    def encoder(self):
        return self._encoder

    @property
    def download_target_dir(self):
        return self._download_target_dir

    @property
    def flare_fake_time(self):
        return self._flare_fake_time

    @property
    def flare_id_front_corr(self):
        return self._flare_id_front_corr

    @property
    def flare_fake(self):
        return self._flare_fake

    @property
    def ring_use_high_res(self):
        return self._ring_use_high_res

    @property
    def lrv(self):
        return self._lrv

    @property
    def stub(self):
        return self._stub

    @property
    def verbose(self):
        return self._verbose

    @property
    def run_time(self):
        return self._run_time

    @property
    def fps(self):
        return self._fps

    @property
    def res(self):
        return self._res

    @property
    def flare(self):
        return self._flare

    @property
    def liveview(self):
        return self._liveview

    @property
    def stitch_mode(self):
        return self._stitch_mode


    @property
    def env(self):
        self.environment = \
             {
            'fps'                   : self.fps,
            'res'                   : self.res,
            'flare'                 : self.flare,
            'liveview'              : self.liveview,
            'stitch_mode'           : self.stitch_mode,
            'run_time'              : self.run_time,
            'verbose'               : self.verbose,
            'stub'                  : self.stub,
            'lrv'                   : self.lrv,
            'flare_fake'            : self.flare_fake,
            'flare_id_front_corr'   : self.flare_id_front_corr,
            'flare_fake_time'       : self.flare_fake_time,
            'ring_use_high_res'     : self.ring_use_high_res,
            'encoder'               : self.encoder,
            'sensor'                : self.sensor
             }
        return  self.environment


    #----------------------------------------------- setters -----------------------------------------------------

    @ring_use_high_res.setter
    def ring_use_high_res(self,arg_ring_use_high_res):
        assert ( type(arg_ring_use_high_res) is str ) ,"{} must be of type str ".format(arg_ring_use_high_res)
        self._ring_use_high_res = arg_ring_use_high_res



    @flare_fake_time.setter
    def flare_fake_time(self,arg_flare_fake_time):
        assert ( type(arg_flare_fake_time) is str ) ,"{} must be of type str ".format(arg_flare_fake_time)
        self._flare_fake_time = arg_flare_fake_time

    @flare_id_front_corr.setter
    def flare_id_front_corr(self,_arg_flare_id_front_corr):
        assert ( type(_arg_flare_id_front_corr) is str ) ,"{} must be of type str ".format(_arg_flare_id_front_corr)
        self._flare_id_front_corr = _arg_flare_id_front_corr


    @flare_fake.setter
    def flare_fake(self,arg_flare_fake):
        assert ( type(arg_flare_fake) is str ) ,"{} must be of type str ".format(arg_flare_fake)
        self._flare_fake = arg_flare_fake


    @download_target_dir.setter
    def download_target_dir(self,arg_target_dir):
        assert ( type(arg_target_dir) is str ) ,"{} must be of type str ".format(arg_target_dir)
        self._download_target_dir = arg_target_dir


    @lrv.setter
    def lrv(self,arg_lrv):
        assert ( type(arg_lrv) is str ) ,"{} must be of type str ".format(arg_lrv)
        self._lrv = arg_lrv


    @stub.setter
    def stub(self,arg_stub):
        assert ( type(arg_stub) is str ) ,"{} must be of type str ".format(arg_stub)
        self._stub = arg_stub


    @verbose.setter
    def verbose(self,arg_verbose):
        assert ( type(arg_verbose) is str ) ,"{} must be of type str ".format(arg_verbose)
        self._verbose = arg_verbose


    @run_time.setter
    def run_time(self,arg_run_time):
        assert ( type(arg_run_time) is str ) ,"{} must be of type str ".format(arg_run_time)
        self._run_time = arg_run_time

    @stitch_mode.setter
    def stitch_mode(self, arg_stitch_mode):
        assert (type(arg_stitch_mode) is str), "{} must be of type str ".format(arg_stitch_mode)
        self._stitch_mode = arg_stitch_mode

    @liveview.setter
    def liveview(self, arg_liveview):
        assert (type(arg_liveview) is str), "{} must be of type str ".format(arg_liveview)
        self._liveview = arg_liveview

    @flare.setter
    def flare(self, arg_flare):
        assert (type(arg_flare) is str), "{} must be of type str ".format(arg_flare)
        self._flare = arg_flare

    @res.setter
    def res(self, arg__res):
        assert (type(arg__res) is str), "{} must be of type str ".format(arg__res)
        self._res = arg__res

    @fps.setter
    def fps(self, arg__fps):
        assert (type(arg__fps) is str), "{} must be of type str ".format(arg__fps)
        self._fps = arg__fps

    @encoder.setter
    def encoder(self, arg_encoder):
        assert (type(arg_encoder) is str), "{} must be of type str ".format(arg_encoder)
        self._encoder = arg_encoder


    @sensor.setter
    def sensor(self, arg_sensor):
        assert (type(arg_sensor) is str), "{} must be of type str ".format(arg_sensor)
        self._sensor = arg_sensor



    def get_environment(self):
        return self.env


    def set_environment(self,arg_dict):
        '''
        remove any space ( at the begining and at the end of the test env varaible , example ' fps ' -->'fps'
        :param arg_dict: dictionnary of the envirement test varaibles to set
        :return: None
        '''
        for key,value in arg_dict.items():
            key = key.strip()
            if key in self.env:
                if  key           == 'fps':
                    self.fps                    = value
                elif key          == 'res':
                    self.res                    = value
                elif key          == 'sensor':
                    self.sensor                 = value
                elif key          == 'encoder':
                    self.ecoder                 = value
                elif key          == 'flare':
                    self.flare                  = value
                elif key          == 'liveview':
                    self.liveview               = value
                elif key          == 'stitch_mode':
                    self.stitch_mode            = value
                elif key          == 'ring_use_high_res':
                    self.ring_use_high_res      = value
                elif key          == 'run_time':
                    self.run_time               = value
                elif key          == 'verbose':
                    self.verbose                = value
                elif key          == 'stub':
                    self.stub                   = value
                elif key          == 'lrv':
                    self.lrv                    = value
                elif key          == 'flare_fake':
                    self.flare_fake             = value
                elif key          == 'flare_id_front_corr':
                    self.flare_id_front_corr    = value
                elif key          == 'flare_fake_time':
                    self.flare_fake_time        = value
            else :
                print(key ,'is not a test environment variable')













#
# test_env =  TestEnvironment()
# test_env.download_target_dir = 'hell'
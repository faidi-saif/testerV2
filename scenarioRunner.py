import json
import os
from logger import Logger
from marshmallow import Schema, fields, pprint, ValidationError
# pip3 install -U marshmallow --pre
import  check.checker as checker


class ScenarioRunner :

    def __init__(self,vcamera):
        self.vcamera            = vcamera
        self.description        = ''
        self.steps              = []
        self.step_preview       = 'preview'
        self.step_still         = 'still'
        self.step_reset         = 'reset'
        self.step_video         = 'video'
        self.step_checker       = 'checker'
        self.step_flash         = 'flash'
        self.step_reboot        = 'reboot'
        self.ref_frw_type       = 'spherical'
        self.results            = []
        self.logger             = Logger()

    # ---------------------------------------------- ------------------------------------------
    def load_json(self , arg_file):
        '''
        :param arg_file: json input file
        :return:  dictionary from json file
        '''
        with open(arg_file ,'r') as f :
            sceanrio = json.load(f)
            return sceanrio

    # ---------------------------------------------- ------------------------------------------
    def check_format(self,arg_path):
        '''
        convert ~ into home directory and remove white spaces
        :param arg_path:
        :return:
        '''
        path = arg_path.strip()
        if arg_path[0] == '~':
            path = os.environ['HOME'] + arg_path[1:]
        return path

    # ---------------------------------------------- ------------------------------------------
    def run_wlog(self,arg_step,function,*args):
        '''

        :param arg_step: dictionary containing the step to be executed
        :param function: callback function associated to the step
        :param args: arguments passed to the function
        :return: None

        this function check if the user wants to keep the serial ports logs for the associated step or not
        '''
        if  'logs' in arg_step.keys():
            self.vcamera.start_acquisition()
            function(*args)
            self.vcamera.stop_acquisition()
            data = self.vcamera.get_data()
            log_path = str(self.logger.create_dir(self.check_format(arg_step['logs'])))
            rtos_path = log_path + '/rtos.txt'
            linux_path = log_path + '/linux.txt'
            self.logger.write(rtos_path, data[0])
            self.logger.write(linux_path, data[1])
        else :
            #print(*args)
            function(*args)


    # ---------------------------------------------- ------------------------------------------

    def run(self,arg_step):
        '''

        :param arg_step: step of the scenario
        :return: result of the step ( None  True or False )
        '''


        result = None
        if arg_step ['case']   == self.step_reset:
             if self.vcamera.is_ready('serial',arg_timeout=10):
                soft_hard = arg_step['params']['option']
                self.run_wlog(arg_step,self.vcamera.reset,soft_hard)
             else :
                 raise Exception('cant process step : {} camera is not ready'.format(arg_step ['case']))

        elif arg_step ['case'] ==self.step_still:
            if self.vcamera.is_ready('serial',arg_timeout=10):
                mode = arg_step['params']
                self.run_wlog(arg_step, self.vcamera.take_photo, mode)
            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))


        elif arg_step['case'] == self.step_video:
            if self.vcamera.is_ready('serial',arg_timeout=10):
                mode = arg_step['params']
                self.run_wlog(arg_step, self.vcamera.record_video, mode)
            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))

        elif arg_step['case'] == self.step_flash :
            if self.vcamera.is_ready('ssh', arg_timeout=40):
                mode     = arg_step['params']['mode']
                frw_type = arg_step['params']['frw_type']
                self.run_wlog(arg_step, self.vcamera.flash, mode,frw_type)
            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))

        elif arg_step['case'] == self.step_preview :
            if self.vcamera.is_ready('ssh', arg_timeout=40):
                mode     = arg_step['params']
                self.run_wlog(arg_step, self.vcamera.preview, mode)
            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))


        elif arg_step ['case'] == self.step_checker:
            if self.vcamera.is_ready('ssh',arg_timeout=30) :
                checker = arg_step['params']['TypeChecker']
                if checker == 'FileNotNull':
                    out_dir = self.check_format(arg_step['params']['out_directory'])
                    self.vcamera.get_results(out_dir)
                    param = out_dir
                elif checker =='FrwVersion' :
                    param = self.vcamera
                result = self.check(checker,param)
                return result
            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))




    # ---------------------------------------------- ------------------------------------------

    def check(self ,derived_checker,*args):
        '''
        instatiate the checker class based on the user input and run the check fuction
        :param derived_checker: checker
        :param args:  parametres for the checker
        :return: result of the test
        '''
        derived_checker = derived_checker.strip()
        klass = getattr(checker, derived_checker)
        instance  = klass()
        result = instance.check(*args)
        return result

    # ---------------------------------------------- ------------------------------------------
    def run_pre_step(self,arg_step):
        '''
        performed before each step
        :param arg_step:
        :return:
        '''
        pass

    # ---------------------------------------------- ------------------------------------------
    def run_post_step(self,arg_step):
        '''
        performed after each step
        :param arg_step:
        :return:
        '''
        # if firmware is not valid print results , reflash with valid firmware , exit
        if (( arg_step['case'] == self.step_flash)): #and (self.vcamera.is_ready('ssh','serial',arg_timeout=90) == False )):
            print('invalid firmware ','{} -------> {}'.format(self.description,False))
            self.vcamera.flash('arduino',self.ref_frw_type)
            if self.vcamera.is_ready('ssh','serial',arg_timeout=60):
                print('a valid firmware is installed on the platform')
                exit(1)
            else :
                raise Exception("FlashError , can't flash the platform with a valid firmware " )
        else:
            pass




    # ---------------------------------------------- ------------------------------------------
    def run_pre_scenario(self):
        '''
        performed before each scenario
        :return:
        '''
        self.vcamera.cleanup()


    # ---------------------------------------------- ------------------------------------------
    def run_post_scenario(self):
        '''
        performed after each scenario
        :return:
        '''
        # reinit virtual camera ( all the
        pass

    # ---------------------------------------------- ------------------------------------------
    def run_scenario(self,arg_scenario_file):
        '''
        :param arg_scenario_file: input file (scenario to be executed )
        :return: None
        1- load jso file
        2- find description and the steps
        3- run pre scenario actions
        4- run the different steps of the scenario
        5- get the result and append it to to the self.results list ( the list containig the results of the different
           test cases
        6- run post scenario actions
        '''
        self.run_pre_scenario()

        scenario = self.load_json(arg_scenario_file)
        self.description = scenario['description']
        self.steps       = scenario['steps']
        print("[--------------------------------------------- start running sceanrio : {} --------------------------------]".format(self.description))

        for step in self.steps :
            #print(" case --------------------------------> " + step['case'])

            self.run_pre_step(step)

            self.res = self.run(step)
            if self.res is not None :
                final_result = self.res and self.vcamera.camera.is_serial_ready(arg_timeout=10) # final result = camera alive and test ok
                ret_value = {self.description : final_result}
                self.results.append(ret_value)

            self.run_post_step(step)

        self.run_post_scenario()








# s = ScenarioRunner('camera')
# s.run_scenario('./scenarios/scenario1.json')
##if self.vcamera.camera.is_serial_ready(arg_timeout=30):


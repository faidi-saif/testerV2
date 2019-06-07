import json
import os
from logger import Logger
import  check.checker as checker
import datetime

class ScenarioRunner :

    # ---------------------------------------------- constructor ------------------------------------------
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

    # ---------------------------------------------- load_json ------------------------------------------
    def load_json(self , arg_file):
        '''
        :param arg_file: json input file
        :return:  dictionary from json file
        '''
        with open(arg_file ,'r') as f :
            sceanrio = json.load(f)
            return sceanrio

    # ---------------------------------------------- check_format ------------------------------------------
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

    # ---------------------------------------------- run_wlog ------------------------------------------
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
            self.logger.write(rtos_path, data[1])
            self.logger.write(linux_path, data[0])
        else :
            #print(*args)
            function(*args)


    # ---------------------------------------------- run ------------------------------------------

    def run(self,arg_step):
        '''
        :param arg_step: step of the scenario
        :return: result of the step ( None  True or False )
        '''
        result = None
        ret = {}
        test_result = {}

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
            if self.vcamera.is_ready('ssh',arg_timeout=120) :
                checker = arg_step['params']['TypeChecker']
                if checker == 'FileNotNull':
                    out_dir = self.check_format(arg_step['params']['out_directory'])
                    self.vcamera.get_results(out_dir)
                    param = out_dir
                    ret = self.check(checker, param) # {'result' : True or False}
                elif checker =='FrwVersion' :
                    param = self.vcamera
                    ret = self.check(checker, param) # {'result' : True or False , firmware_version : ''xxx'}
                elif checker == 'VideoStat':
                    out_dir = self.check_format(arg_step['params']['out_directory'])
                    self.vcamera.get_results(out_dir)
                    param = out_dir
                    ret = self.check(checker, param) # {'result': True, 'files': [{'name': 'GS010263', 'type': 'MP4', 'size': 18172001, 'duration': '00:00:02.75'},]}
                elif checker == 'PhotoStat':
                    out_dir = self.check_format(arg_step['params']['out_directory'])
                    self.vcamera.get_results(out_dir)
                    param = out_dir
                    ret = self.check(checker, param)  # {'result': True, 'files': [{'name': 'GS010263', 'type': 'JPG', 'size': 18172001},]}

                result = ret.pop('result') # get the value of ret['result'] and remove it from ret
                test_result.update(ret)    # copy the other fields in the final dictionary
            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))



        test_result.update({'result': result})
        return test_result




    # ----------------------------------------------check ------------------------------------------

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

    # ---------------------------------------------- run_pre_step ------------------------------------------
    def run_pre_step(self,arg_step):
        '''
        performed before each step
        :param arg_step:
        :return:
        '''
        pass

    # ---------------------------------------------- run_post_step ------------------------------------------
    def run_post_step(self,arg_step):
        '''
        performed after each step
        :param arg_step:
        :return:
        '''
        # if firmware is not valid print results , reflash with valid firmware , exit
        if (( arg_step['case'] == self.step_flash) and (self.vcamera.is_ready('ssh','serial',arg_timeout=90) == False )):
            print('invalid firmware ','{} -------> {}'.format(self.description,False))
            self.vcamera.flash('arduino',self.ref_frw_type)
            if self.vcamera.is_ready('ssh','serial',arg_timeout=120):
                print('a valid firmware is installed on the platform')
                exit(1)
            else :
                raise Exception("FlashError , can't flash the platform with a valid firmware " )
        else:
            pass


    def before_test(self):
        '''
        cleanup the camera before starting the test
        :return:None
        '''
        print('*** cleanup camera ***')
        self.vcamera.cleanup()

    # ----------------------------------------------run_pre_scenario  ------------------------------------------

    def run_pre_scenario(self,with_unique_log_index):
            now = datetime.datetime.now()
            index = str(now.isoformat())
            for step in self.steps :
                if with_unique_log_index == True:
                     self.add_log_unique_index(arg_step = step,index = index)




    # ---------------------------------------------- run_post_scenario ------------------------------------------
    def run_post_scenario(self):
        '''
        performed after each scenario
        :return:
        '''
        # reinit virtual camera ( all the
        pass

    # ---------------------------------------------- add_log_unique_index ------------------------------------------
    def add_log_unique_index(self,arg_step,index):
        if 'logs' in arg_step.keys():
            arg_step['logs'] = arg_step['logs'] + '_' + index
        if  'out_directory' in arg_step['params'].keys():
            arg_step['params']['out_directory'] =  arg_step['params']['out_directory'] + '_' + index




    # ---------------------------------------------- run_scenario ------------------------------------------
    def run_scenario(self,arg_scenario_file,with_unique_log_index = None):
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

        scenario = self.load_json(arg_scenario_file)
        self.description = scenario['description']
        self.steps       = scenario['steps']

        self.run_pre_scenario(with_unique_log_index=with_unique_log_index)

        print("[--------------------------------------------- start running sceanrio : {} --------------------------------]".format(self.description))

        for step in self.steps :
            #print(" case --------------------------------> " + step['case'])
            # add unique index for logs directories


            self.run_pre_step(step)

            self.res = self.run(step)
            if self.res['result'] is not None :
                self.res['result'] = self.res['result'] and self.vcamera.camera.is_serial_ready(arg_timeout=10) # final result = camera alive and test ok
                ret_value = {'description' : self.description}
                ret_value.update(self.res)
                self.results.append(ret_value)

            self.run_post_step(step)

        self.run_post_scenario()

    # ---------------------------------------------- run_scenario ------------------------------------------
    def get_test_result(self,result_path):
        '''
        store test results in a  json file at 'result_path'
        :param result_path: path to store test results
        :return: None
        '''
        result_path = self.check_format(result_path) # get the equivalent to ~/ in path
        for el in self.results  :
            print(json.dumps(el,indent = 4))
        with open(result_path, 'w') as outfile:
            json.dump(self.results, outfile,indent=4)









# s = ScenarioRunner('camera')
# s.run_scenario('./scenarios/scenario1.json')
##if self.vcamera.camera.is_serial_ready(arg_timeout=30):


import json
import os
from logger import Logger
from marshmallow import Schema, fields, pprint, ValidationError
import  check.checker as checker


class ScenarioRunner :

    def __init__(self,vcamera):
        self.vcamera            = vcamera
        self.description        = ''
        self.steps              = []
        self.step_take_photo    = 'take_photo'
        self.step_reset         = 'reset'
        self.step_record_video  = 'record_video'
        self.step_checker       = 'checker'
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

    def run(self,arg_step):

        '''
        :param arg_step: compound of the name of the step and it's parameters
         Examples :
    1 -----------------> take_photo
        {
        "step": "take_photo",
        "params":
        {
            "fps" : "30",
            "res" : "5K",
            "stitch_mode" : "EAC",
            "liveview"    : "off"
        }
        },
    2 -----------------> reset
      {
        "step": "reset",
        "params":
        {
          "option"  :  "soft"
        }
      },
    3 ------------------> get_result
      {
        "case": "checker",
        "params":

        {
          "out_directory"  : "~/Desktop/photo_logs",
          "TypeChecker"        : "FileNotNull"
        }
      }
    4 -----------------> record_video
      {
        "step": "record_video",
        "params":
        {
            "fps" : "30",
            "res" : "5K",
            "stitch_mode" : "EAC",
            "liveview"    : "off"
        }
      },
        :return: None
        '''
        result = None
        if arg_step ['case']   == self.step_reset:
             if self.vcamera.is_ready('serial',arg_timeout=10):
                soft_hard = arg_step['params']['option']
                self.vcamera.start_acquisition()
                self.vcamera.reset(soft_hard)
                self.vcamera.stop_acquisition()
                data = self.vcamera.get_data()
                log_path = self.logger.create_dir(self.check_format(arg_step['logs']))
                rtos_path = log_path + '/rtos.txt'
                linux_path = log_path + '/linux.txt'
                self.logger.write(rtos_path, data[0])
                self.logger.write(linux_path, data[1])


        elif arg_step ['case'] ==self.step_take_photo:
            if self.vcamera.is_ready('serial',arg_timeout=10):
                mode = arg_step['params']
                self.vcamera.take_photo(mode)


        elif arg_step['case'] == self.step_record_video:
            if self.vcamera.is_ready('serial',arg_timeout=10):
                mode = arg_step['params']
                self.vcamera.record_video(mode)


        elif arg_step ['case'] == self.step_checker:
            if self.vcamera.is_ready('ssh',arg_timeout=30) :
                out_dir = self.check_format(arg_step['params']['out_directory'])
                self.vcamera.get_results(out_dir)
                checker = arg_step['params']['TypeChecker']
                result = self.check(checker,out_dir)
                return result

    # ---------------------------------------------- ------------------------------------------

    def check(self ,derived_checker,*args):
        derived_checker = derived_checker.strip()
        klass = getattr(checker, derived_checker)
        instance  = klass()
        result = instance.check(*args)
        return result

    # ---------------------------------------------- ------------------------------------------
    def run_pre_scenario(self):
        self.vcamera.is_ready('serial','ssh',arg_timeout=30)
        self.vcamera.clean_content('/tmp/fuse_d/DCIM/100GOPRO/')
        self.vcamera.reset('soft') # before starting the scenario , make a reset

    # ---------------------------------------------- ------------------------------------------
    def run_post_scenario(self):
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
        scenario = self.load_json(arg_scenario_file)
        self.description = scenario['description']
        self.steps       = scenario['steps']
        print("[--------------------------------------------- start running sceanrio : {} --------------------------------]".format(self.description))
        self.run_pre_scenario()
        for step in self.steps :
            print(" case --------------------------------> " + step['case'])
            result = self.run(step)
            if result is not None :
                final_result = result and self.vcamera.camera.is_serial_ready(arg_timeout=10) # final result = camera alive and test ok
                ret_value = {self.description : final_result}
                self.results.append(ret_value)
        self.run_post_scenario()








# s = ScenarioRunner('camera')
# s.run_scenario('./scenarios/scenario1.json')
##if self.vcamera.camera.is_serial_ready(arg_timeout=30):


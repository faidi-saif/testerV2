
from camera import Camera
from grid import Grid
from vcamera import Vcamera
from scenarioRunner import ScenarioRunner
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-sc' , help = 'the name of the scenario , which can be : endurance ,stitching or sni' , type = str)

args = parser.parse_args()

grid= Grid(arg_host_ip = "192.168.0.1",arg_host_http_path = '/var/www/html')

hard_cam  = Camera(username = 'root',host_ip = '192.168.0.202',ssh_passwd = '',web_port = 8042,arduino_port = '/dev/ARDUINO',linux_port = '/dev/LINUX',rtos_port = '/dev/RTOS',grid = grid ,control_mode= 'complete' )

vcam = Vcamera(hard_cam,'spherical')

sce_runner = ScenarioRunner(vcam)

assert args.sc == 'sni' or args.sc =='stitching' or args.sc == 'endurance' ,'Invalid scenario argument use "sni","stitching"or"endurance"'

sce_runner.before_test()

if args.sc == 'sni':
# **------------------------------------------------- SNI sanity --------------------------------------------**
#---V0
    sce_runner.run_scenario('./scenarios/preview_5k_24.json')
    sce_runner.run_scenario('./scenarios/video24.json')
    sce_runner.run_scenario('./scenarios/preview_5k_25.json')
    sce_runner.run_scenario('./scenarios/video25.json')
    sce_runner.run_scenario('./scenarios/preview_5k_30.json')
    sce_runner.run_scenario('./scenarios/video30.json')

    #---S0
    sce_runner.run_scenario('./scenarios/preview_5k_30.json')
    sce_runner.run_scenario('./scenarios/S0.json')

    #---C0
    sce_runner.run_scenario('./scenarios/preview_5k_30.json')
    sce_runner.run_scenario('./scenarios/C0.json')

    #---V1
    sce_runner.run_scenario('./scenarios/preview_4k_24.json')
    sce_runner.run_scenario('./scenarios/video_4k_24.json')
    sce_runner.run_scenario('./scenarios/preview_4k_25.json')
    sce_runner.run_scenario('./scenarios/video_4k_25.json')
    sce_runner.run_scenario('./scenarios/preview_4k_30.json')
    sce_runner.run_scenario('./scenarios/video_4k_30.json')

elif args.sc == 'stitching':
# ------------------------------------------------- stitching sanity --------------------------------------------
    sce_runner.run_scenario('./scenarios/stitching_sanity/preview_5k_30.json')
    sce_runner.run_scenario('./scenarios/stitching_sanity/video_5k_30_30s.json')
    sce_runner.run_scenario('./scenarios/stitching_sanity/preview_5k_30.json')
    sce_runner.run_scenario('./scenarios/stitching_sanity/S0_capture.json')

elif args.sc == 'endurance':
# ------------------------------------------------- endurance sanity --------------------------------------------
# take 200 shots
    for shot in range (200):
        sce_runner.run_scenario('./scenarios/endurance_sanity/preview_5k_30.json')
        sce_runner.run_scenario('./scenarios/endurance_sanity/S0_capture.json',with_unique_log_index=True)
    # 1-hour video
    sce_runner.run_scenario('./scenarios/endurance_sanity/preview_5k_30.json')
    sce_runner.run_scenario('./scenarios/endurance_sanity/video_5k_30_1h.json')



# ------------------------------------------------- get the results --------------------------------------------
sce_runner.get_test_result(result_path='~/test_result.json')




# parser = argparse.ArgumentParser()
#
# parser.add_argument('-s' , help = 'the name of the scenario , exemple : python3 main.py -s C0,S0' , type = str)
#
# parser.add_argument('-p' , help = 'path where to save the test result' , type = str)
#
# parser.add_argument('--arduino' , help = 'run with arduino fro full control ' , action='store_true')
#
# args = parser.parse_args()
#
# control = 'partial'
#
# if args.arduino :
#
#     control = 'complete'
#
# grid= Grid(arg_host_ip = "192.168.0.1",arg_host_http_path = '/var/www/html')
#
# hard_cam  = Camera(username = 'root',host_ip = '192.168.0.202',ssh_passwd = '',web_port = 8042,arduino_port = '/dev/ARDUINO',linux_port = '/dev/LINUX',rtos_port = '/dev/RTOS',grid = grid ,control_mode= control )
#
# vcam = Vcamera(hard_cam,'spherical')
#
# sce_runner = ScenarioRunner(vcam)
#
#
# sce_runner.before_test()
#
# scenarios  = args.s.split(',')
#
#
# for sc in scenarios:
#
#     sce_runner.run_scenario('./scenarios/{}.{}'.format(sc,'json'))
#
#
#
# sce_runner.get_test_result(result_path=args.p)
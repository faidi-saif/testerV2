
from camera import Camera
from grid import Grid
from vcamera import Vcamera
from scenarioRunner import ScenarioRunner
import argparse


parser = argparse.ArgumentParser()


parser.add_argument('-s' , help = 'the name of the scenario , exemple : python3 main.py -s C0,S0' , type = str)



grid= Grid(arg_host_ip = "192.168.0.1",arg_host_http_path = '/var/www/html')

hard_cam  = Camera(username = 'root',host_ip = '192.168.0.202',ssh_passwd = '',web_port = 8042,arduino_port = '/dev/ARDUINO',linux_port = '/dev/LINUX',rtos_port = '/dev/RTOS',grid = grid)


vcam = Vcamera(hard_cam,'spherical')

sce_runner = ScenarioRunner(vcam)

args = parser.parse_args()

#sce_runner.before_test()

scenarios  = args.s.split(',')

for sc in scenarios:

    sce_runner.run_scenario('./scenarios/{}.{}'.format(sc,'json'))


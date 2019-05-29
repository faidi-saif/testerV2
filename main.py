
from camera import Camera
from grid import Grid
from vcamera import Vcamera
from scenarioRunner import ScenarioRunner
import argparse


parser = argparse.ArgumentParser()


parser.add_argument('-s' , help = 'the name of the scenario' , type = str)



grid= Grid(arg_host_ip = "192.168.0.1",arg_host_http_path = '/var/www/html')

hard_cam  = Camera(username = 'root',host_ip = '192.168.0.202',ssh_passwd = '',web_port = 8042,arduino_port = '/dev/ARDUINO',linux_port = '/dev/LINUX',rtos_port = '/dev/RTOS',grid = grid)


vcam = Vcamera(hard_cam,'spherical')

sce_runner = ScenarioRunner(vcam)

args = parser.parse_args()

scenarios  = args.s.split(',')

for sc in scenarios:
    #print('./scenarios/{}.{}'.format(sc,'json'))
    sce_runner.run_scenario('./scenarios/{}.{}'.format(sc,'json'))


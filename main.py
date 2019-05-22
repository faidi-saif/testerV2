
from camera import Camera
from grid import Grid
from vcamera import Vcamera
from scenarioRunner import ScenarioRunner


grid= Grid(arg_host_ip = "192.168.0.1",arg_host_http_path = '/var/www/html')

hard_cam  = Camera(username = 'root',host_ip = '192.168.0.202',ssh_passwd = '',web_port = 8042,arduino_port = '/dev/ARDUINO',linux_port = '/dev/LINUX',rtos_port = '/dev/RTOS',grid = grid)


vcam = Vcamera(hard_cam,'spherical')

#vcam.get_results('/home/saif/Desktop/test_capt')


sce_runner = ScenarioRunner(vcam)
#
sce_runner.run_scenario('./scenarios/flash.json')
#
print('final results :' ,sce_runner.results)











#vcam.get_files('/tmp/fuse_d/DCIM/100GOPRO/','/home/saif/Desktop/') # cammed also this way
#print(vcam.get_file_stat('/tmp/fuse_d/DCIM/100GOPRO/GH010199.MP4'))
#vcam.clean_content('/tmp/fuse_d/DCIM/100GOPRO/*')
#vcam.get_results('/home/saif/Desktop/test_capt')
#vcam.get_files('/tmp/fuse_d/DCIM/100GOPRO/','/home/saif/Dls
# esktop/test_capt')
#vcam.ls_files('/tmp/fuse_d/DCIM/100GOPRO/')
#print (vcam.get_frw_version())

# for i in range (30):
#     vcam.camera.is_serial_ready(arg_timeout=10)



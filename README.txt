to setup the tester follow these instructions : 

1- install the following packages :
     1- local machine : 
	* pip3 install bs4
	* pip3 install wget
	* pip3 install serial
	* pip3 install pyserial 
	* pip3 install paramiko
    2- for jenkins :
        *there is a requirement.txt file which install all the packages automatically 

2- setup serial ports 
	* check the {idProduct} and {idVnedor} of your arduino and edit the file '94-serials.rules'
		-to find the informations about the usb port connected to the arduino :
		'udevadm info -a -p $(udevadm info -q path -n /dev/ttyusb_connected_to_arduino'
	* save the file '94-serials.rules ' in '/etc/udev/rules.d'
	* run : 'sudo udevadm control --reload-rules && udevadm trigger'
	* replug the usb (arduino , and usb fr rtos and linux on camera )

3- setup the power control
	* installation : 
		-'sudo apt-get install libusb-1.0-0-dev '
		-'sudo apt-get install libusb-1.0-0 '
 		- In the root of the source code structure you will find the following two scripts:
    			build.sh
    			install.sh
		As the name indicates one builds the application and the other installs it.
		To build the application run: 'sudo ./build.sh '
		Finally install the hidapi shared libraries and the ykushcmd command by running the following script:
		'sudo ./install.sh' 

	* in '/etc/sudoers' add the following line : 'username  ALL=(ALL) NOPASSWD:/usr/bin/ykushcmd' with the appropriate username

	* setup the device serial_number : 
		- get the serial number using : 'sudo ykushcmd ykushxs -l' , example: {YKa1184} 
		- in ./network/arduinoSerializer edit the variable : "device_serial" to adapt it to 
		  your serial_number
 
additional instructions
to run a scenario : 
    we are based on JSON files for scenarios description :
        *in ./sceanarios you find many examples of scenarios 
        *the main.py file is structured as follow : 
            1- before_test 
            2- scenario(s) executed
            3- get_test_result ( in which we pass the file where to store the result file, this JSON is a list of test results marked by its description)
        * we have the possibility to run the tester with(out) Arduino according to the option passed as an argument, example : 
             -- python3 main.py -s preview_5k_30,video30 --arduino -p ~/Desktop/test_results.json --
            where : -s stands for scenario
                    -p stands for test_results.json path
                    --arduino means to run with Arduino ( note that without Arduino we can't make a reset on camera, so the test will fail for now)






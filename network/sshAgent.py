import paramiko
import os
import warnings
import socket
# pip install paramiko



class SshAgent:


    def __init__(self,arg_username,arg_host,arg_port=22,arg_timeout=10,arg_pkey=os.environ['HOME']+'/.ssh/id_rsa',arg_passwd=''):
        self.ssh_output = None
        self.ssh_error  = None
        self.client     = None
        self.host       = arg_host
        self.username   = arg_username
        self.password   = arg_passwd
        self.timeout    = arg_timeout
        self.pkey       = arg_pkey
        self.port       = arg_port
        warnings.filterwarnings(action='ignore', module='.*paramiko.*')
        self.connected  = False

    def execute_command(self, command):
        """Execute a command on the remote host.Return a tuple containing
        an integer status and a two strings, the first containing stdout
        and the second containing stderr from the command.
        example of a list of commands commands = ['ls;pwd'] must be in the same string
        to be considered as a unique command ( low level api is implemented this way :(
        """
        client = None
        output = None
        try:
            client = paramiko.SSHClient()

            client.load_system_host_keys()

            client.set_missing_host_key_policy(paramiko.WarningPolicy())

            client.connect(hostname=self.host, port=self.port, username=self.username, password=self.password,pkey=self.pkey,
                                    timeout = self.timeout)

            stdin, stdout, stderr = client.exec_command(command)

            output = stdout.read().decode("utf-8")

        finally:
            if client:
                client.close()

            return output





    def __del__(self):
        #self.client.close() # if you call only the constructor , there will be not a call to connect function
        # so ther is no instance of client --> no function close !
        # if i put connect in the constructor --> can't handle the time to connect to ssh which must be
        # called after the call of is_ready on the camera
        pass










#ssh_agent = SshAgent(arg_username='root',arg_host='192.168.0.202',arg_passwd='') # no password since Pkey ( public ) copied on the server
# retour = ssh_agent.execute_command(['ls /tmp/fuse_d/DCIM/100GOPRO/;pwd'])
# print(retour)
#
# call for execute command ( only one command as string )

# file= ssh_agent.execute_command('ls /tmp/fuse_d/DCIM/100GOPRO/')
# print(file)
# ssh_agent.execute_command('rm -rf /tmp/fuse_d/DCIM/100GOPRO/*')



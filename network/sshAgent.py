import paramiko
import os
import warnings
import socket
# pip install paramiko



class SshAgent:


    def __init__(self,arg_username,arg_passwd,arg_host,arg_port=22,arg_timeout=10,arg_pkey=os.environ['HOME']+'/.ssh/id_rsa'):
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






    def connect(self):
        "Login to the remote server"
        try:
            # Paramiko.SSHClient can be used to make connections to the remote server and transfer files
            print ("Establishing ssh connection")
            self.client = paramiko.SSHClient()
            # Parsing an instance of the AutoAddPolicy to set_missing_host_key_policy() changes it to allow any host.
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Connect to the server
            if (self.password == ''):
                self.pkey = paramiko.RSAKey.from_private_key_file(self.pkey)
                self.client.connect(hostname = self.host, port = self.port, username = self.username, pkey=self.pkey,
                                    timeout = self.timeout, allow_agent = False, look_for_keys = False)
                print ("Connected to the server", self.host )
            else:
                self.client.connect(hostname = self.host, port = self.port, username = self.username, password = self.password,
                                    timeout = self.timeout, allow_agent = False, look_for_keys = False)
                print ("Connected to the server", self.host )
        except paramiko.AuthenticationException:
            print ("Authentication failed, please verify your credentials")
            result_flag = False
        except paramiko.SSHException as sshException:
            print ("Could not establish SSH connection: %s" % sshException)
            result_flag = False
        except socket.timeout as e:
            print ("Connection timed out")
            result_flag = False
        except Exception as e :
            print('\nException in connecting to the server')
            print('PYTHON SAYS:', e)
            result_flag = False
            self.client.close()
        else:
            result_flag = True

        return result_flag



    def execute_command(self, command):
    #     """Execute a command on the remote host.Return a tuple containing
    #     an integer status and a two strings, the first containing stdout
    #     and the second containing stderr from the command.
    #     example of a list of commands commands = ['ls;pwd'] must be in the same string
    #     to be considered as a unique command ( low level api is implemented this way :(
    #     """
        output  = None
        self.ssh_output = None
        if self.connected == False :
            self.connected  = self.connect()
            self.connected = True
        else :
            pass
        try:
            if self.connected :
                    #print ("Executing command --> {}".format(command))
                    stdin, stdout, stderr = self.client.exec_command(command, timeout=20)
                    self.ssh_output = stdout.read()
                    self.ssh_error  = stderr.read()
                    if self.ssh_error:
                        print ("Problem occurred while running command:" + command + " The error is " + self.ssh_error )
                    else:
                        output = self.ssh_output.decode("utf-8")
                        #print('command : {} output -->'.format(command),output)
                    #self.client.close()
            else:
                print("Could not establish SSH connection")
        except socket.timeout as e:
            print ("Command timed out.", command )
            self.client.close()
        except paramiko.SSHException:
            print ("Failed to execute the command!", command )
            self.client.close()
        return output



    def __del__(self):
        #self.client.close() # if you call only the constructor , there will be not a call to connect function
        # so ther is no instance of client --> no function close !
        # if i put connect in the constructor --> can't handle the time to connect to ssh which must be
        # called after the call of is_ready on the camera
        pass




    # def execute_commands(self, commands):
    #     """Execute a command on the remote host.Return a tuple containing
    #     an integer status and a two strings, the first containing stdout
    #     and the second containing stderr from the command.
    #     example of a list of commands commands = ['ls;pwd'] must be in the same string
    #     to be considered as a unique command ( low level api is implemented this way :(
    #     """
    #
    #     self.ssh_output = None
    #     result_flag = True
    #     try:
    #         if self.connect():
    #             for command in commands:
    #                 print ("Executing command --> {}".format(command))
    #                 stdin, stdout, stderr = self.client.exec_command(command, timeout=10)
    #                 self.ssh_output = stdout.read()
    #                 self.ssh_error  = stderr.read()
    #                 if self.ssh_error:
    #                     print ("Problem occurred while running command:" + command + " The error is " + self.ssh_error )
    #                     result_flag = False
    #                 else:
    #                     #print ("Command execution completed successfully", command)
    #                     output = self.ssh_output.decode("utf-8")
    #                     #print('command : {} output -->'.format(command),output)
    #                 #self.client.close()
    #         else:
    #             print("Could not establish SSH connection")
    #             result_flag = False
    #     except socket.timeout as e:
    #         print ("Command timed out.", commands )
    #         self.client.close()
    #         result_flag = False
    #     except paramiko.SSHException:
    #         print ("Failed to execute the command!", commands )
    #         self.client.close()
    #         result_flag = False
    #     #return result_flag
    #     return output
    #


#ssh_agent = SshAgent(arg_username='root',arg_host='192.168.0.202',arg_passwd='') # no password since Pkey ( public ) copied on the server
# call for execute commands ( many commands in a string in a list
# retour = ssh_agent.execute_commands(['ls /tmp/fuse_d/DCIM/100GOPRO/;pwd'])
# print(retour)
#
# call for execute command ( only one command as string )
# file= ssh_agent.execute_command('ls /tmp/fuse_d/DCIM/100GOPRO/')
# print(file)
#
# file= ssh_agent.execute_command('ls /tmp/fuse_d/DCIM/100GOPRO/')
# print(file)

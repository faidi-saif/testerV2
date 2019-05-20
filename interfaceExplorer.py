import netifaces

# ------------------------------------------------ class to discover exixting network inerfaces  --------------------------------------------------------
class InterfaceExplorer:
    def __init__(self):
        pass

    # ------------------------------------------------ exploring all network interfaces --------------------------------------------------------
    # for "arg_type" use : 'all' or 'wireless'
    def explore(self,arg_type = 'all' ):
        network_table = []
        interfaces = (netifaces.interfaces())
        for inter in interfaces :
            interface =netifaces.ifaddresses( inter )
            if arg_type == 'wireless':
                if 2 in interface.keys():
                    # the second field of the dictionnary contains the ip adress and the netmask
                    interface_info = interface[2][0]
                    # add the name of the interface
                    interface_info.update({'name':inter})
                    # create a table f network interfaces
                    network_table.append(interface_info)
            elif arg_type == 'all':# all interfaces
                interface.update({'name':inter})
                network_table.append(interface)
        return network_table



    # ------------------------------------------------ display the table of the network interfaces --------------------------------------------------------
    def display(self,arg_table):
        for el in arg_table:
            print (el)

    # ------------------------------------------------ check if an interface exist based on it's ip adress --------------------------------------------------------
    def find_by_ip(self,arg_ip):
        wireless_interfaces = self.explore('wireless')
        exist = False
        for field in wireless_interfaces:
            if field ['addr'] == arg_ip:
                exist = True
                return field
        if exist == False:
            return exist






# m_networkexp = NetworkExplorer()
# table = m_networkexp.explore('wireless')
# interface  = m_networkexp.find_by_ip('192.168.0.1')
# print(interface)
#m_networkexp.display(table)
# ------------------------------------------------  --------------------------------------------------------

class LogParser :

    def __init__(self):
        self.myfile =None
        pass

    def __del__(self):
        pass

    def close(self,arg_file):
        arg_file.close()


    """
    make sure to close the file after reading 
    """
    def read(self,arg_file):
        mlines = []
        with open(arg_file,'r') as self.myfile:
            for myline in self.myfile :
                mlines.append(myline)
        return mlines

    def display(self,arg_file_content):
        for line in arg_file_content:
            print (line)

    """
    return a dictionnary with varaibles to be extracted and their values 
    example :
    {
     'compiled': 'Apr_30_2019,_13:45:03_git-286fc0746-dirty\x1b[0m\n',
     'Release': 'H19.03.00.07.00'
    }
    if parmas dosen't exist , the function will return -1
    """


    def extract(self,arg_file,*args):
        m_content = self.read(arg_file)
        self.display(m_content)
        if len (args) == 0:
            raise Exception ("No argument to be extracted  passed ")
        else:
            extracted ={}
            for arg in args :
                params_from_line = self.search(arg,m_content)
                if params_from_line == -1:
                    return -1
                else :
                    l_arg_index = params_from_line.index(arg)
                    arg = arg.strip()
                    arg_value = ''
                    if (arg == 'compiled'):
                        arg_value ='_'.join(params_from_line[l_arg_index+1:])
                    elif(arg =='Release'):
                        arg_value = arg_value+params_from_line[l_arg_index + 1]
                    extracted.update({arg : arg_value})

        self.myfile.close()
        return extracted


    def search(self,arg_word,arg_list_lines):
        exist_flag =False
        for line in arg_list_lines:
            if arg_word in line :
                #print(line.split(' '))
                exist_flag = True
                return line.split(' ')
        if exist_flag == False :
            return -1

















# minstance = frw_parser()
# #mlines = minstance.read('/home/saif/Logs/flashTestspherical/linux_flashTest_log.txt')
# # minstance.display(mlines)
# extracted = minstance.extract('/home/saif/Logs/flashTestspherical/linux_flashTest_log.txt','compiled','\tRelease')
# print(extracted)
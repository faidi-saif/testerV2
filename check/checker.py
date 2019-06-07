from abc import ABC, abstractmethod
import os
import subprocess


# ----------------------------------------------base class checker ------------------------------------------
class Checker (ABC):

    def __init__(self):
        self._result = False
        super().__init__()


    @ property
    def result(self):
        return self._result


    @abstractmethod
    def check(self,*args ):
        pass

 # ----------------------------------------------FileNotNull checker ------------------------------------------
class FileNotNull(Checker):


    def check(self, *args):
        resul = True
        path  = args[0]
        assert (path is not None) , " No directory for check passed "
        files = os.listdir(path)
        if files != []:
            for file in files :
                file_path = path + '/' + file
                r = os.stat(file_path)
                if r.st_size == 0:
                    res = False
                    print('file "{}" is  null'.format(file))
                else:
                    res = True
                resul = resul and res
        else :
            resul = False
        return {'result' : resul}
 # ----------------------------------------------FrwVersion checker ------------------------------------------
class FrwVersion(Checker):

    def check(self,*args ):
        cam = args[0]
        version = None
        if cam.is_ready('serial','ssh', arg_timeout=40) :
            version = cam.get_frw_version()
            if version != '':
                ret =  True
            else:
                ret =  False
        else :
            ret =  False
        return {'result' : ret ,'firmware version' : version}


# ----------------------------------------------FileStat checker ------------------------------------------

class FileStat(Checker):




    def extract_properties(self,arg_file_path,arg_file):
        file_path = arg_file_path + '/' + arg_file
        f = arg_file.split('.')
        name        = f[0]
        type        = f[1]
        ret         = os.stat(file_path)
        size        = str(ret.st_size/1000) + 'KB'
        return {'name' : name, 'type':type ,'size':size}


    def check(self,*args ):
        files_properties = []
        result           = True
        path             = args[0]
        assert (path is not None), " No directory for check passed "
        files            = os.listdir(path)
        files_number     = len(files)
        if files  != [] :
            for file in files:
                file_prop = self.extract_properties(path,file)
                files_properties.append(file_prop)
                if file_prop['size'] == 0:
                    res = False
                    print('file "{}" is  null'.format(file))
                else:
                    res = True
                result  = result and res
        else :
            result = False

        return {'result':result,'number of files':files_number,'files' : files_properties}



# ----------------------------------------------VideoStat checker ------------------------------------------
class VideoStat(FileStat):


    def get_length(self,filename):
        result = subprocess.Popen(["ffprobe", filename],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for el in result.stdout.readlines():
            pos = el.decode().find('Duration')
            if  pos >= 0:
                return ( el.decode()[pos+10 :pos+21]) # from thenposition of the word Duration to the end of the duration value

    def extract_properties(self,arg_file_path,arg_file):
        file_path = arg_file_path + '/' + arg_file
        f = arg_file.split('.')
        name        = f[0]
        type        = f[1]
        ret         = os.stat(file_path)
        size        = str(ret.st_size/1000) + 'KB'
        duration    = self.get_length(file_path)
        return {'name' : name, 'type':type ,'size':size,'duration':duration}


# ----------------------------------------------PhotoStat checker ------------------------------------------
class PhotoStat(FileStat):
    pass





# c = VideoStat()
# print(c.check('/home/saif/Desktop/test_logs/C0/photos'))
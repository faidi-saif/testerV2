from abc import ABC, abstractmethod
import os
from vcamera import Vcamera

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
        path =args[0]
        print(path)
        assert (path is not None) , " No directory for check passed "
        files = os.listdir(path)
        for file in files :
            file_path = path + '/' + file
            r = os.stat(file_path)
            if r.st_size == 0:
                res = False
                print('file "{}" is  null'.format(file))
            else:
                res = True
            resul = resul and res
            self._result = resul
        return self._result


class FrwVersion(Checker):

    def check(self,*args ):
        cam = args[0]
        if cam.is_ready('serial','ssh', arg_timeout=40) :
            result = cam.get_frw_version()
            if result != '':
                return True
            else:
                return False
        else :
            return False







        # c = FileNotNull()
# print(c.check('/home/saif/Desktop/photo_logs'))
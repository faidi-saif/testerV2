import os
import shutil

class Logger:

    def __init__(self):
        pass

    #---------------------------------------------- ------------------------------------------
    def open(self,arg_file):
        file = open(arg_file,"w+")
        return file

    # ---------------------------------------------- ------------------------------------------
    def write(self,arg_file,arg_data):
        file = self.open(arg_file)
        file.write(arg_data)
        self.close(file)

    # ---------------------------------------------- ------------------------------------------
    def close(self,arg_file):
       arg_file.close()

    # ---------------------------------------------- ------------------------------------------
    def __del__(self):
        pass

    # ---------------------------------------- remove all files in a given path -----------------------------------------------

    def clean_dir(self,arg_path):
        for the_file in os.listdir(arg_path):
            file_path = os.path.join(arg_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    # ----------------------------------- check if a given directory exists else create it ------------------------------------

    def create_dir(self,arg_path):
        if os.path.isdir(arg_path):
            pass
        else:
            os.makedirs(arg_path)
        return arg_path

    # -------------------------------------------copy files in a given path (clean before ) -----------------------
    def copy_files(self,from_path, to_path):
        if os.path.exists(to_path):
            shutil.rmtree(to_path)
        shutil.copytree(from_path, to_path)

# l = Logger()
# l.clean_dir('/home/saif/Desktop/test_logs/S0')
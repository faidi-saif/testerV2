import wget
import requests
from bs4 import BeautifulSoup
import re
#install wget


class WebServerAgent:

    class fetcher :
        def __init__(self):
            pass

        def list_content(self,url,ext=''):
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'html.parser')
            return [url  + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]




    def __init__(self):
        self.fetcher = self.fetcher()


    def list_content(self,url,ext=''):
         l_url = self.check_path_format(url)
         list_files =  self.fetcher.list_content(l_url,ext)
         for file in list_files:
             if file.endswith("/../"): # remove the .. directory
                 list_files.remove(file)
         return list_files


    # ------------------------------download(path to the remote file ,target directory)--------------------------------------------------------
    def check_path_format(self,arg_url):
        if arg_url.find('http') == -1:
            arg_url = 'http://'+arg_url
        else:
            pass
        return arg_url

    # ------------------------------download(path to the remote file ,target directory)--------------------------------------------------------
    def download(self,arg_url,arg_output_directory):
        url = self.check_path_format(arg_url)
        # no need to check for path existence , already handled by urlib
        file = wget.download(url,out = arg_output_directory)
        print('download file ------>', file)





# wb = WebServerAgent()
# print(wb.list_content('192.168.0.202:8042/DCIM/100GOPRO'))

# wb.download('192.168.0.202:8042/DCIM/100GOPRO/file1','/home/saif/Desktop/')


from GDriveUtils import GDriveUtils as gutils

class GUploadHDA:
    def __init__(self,**kwargs):
        self.__token = 'D:/github/__Secrets/token.json'
        self.__client_secret_path = 'D:/github/__Secrets'
        self.node = kwargs['node']
        self.asset_path = self.node.evalParm('filecache1_file')
        self.local_path = self.node.evalParm('localpath')
        self.GD_Folder  = self.node.evalParm('gdrfld')


    def asset_upload(self):

        data_val = gutils(self.__client_secret_path,self.__token,self.asset_path,self.GD_Folder)
        data_val.upload_file(self.local_path)


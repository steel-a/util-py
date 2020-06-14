import os

class File:

    def __init__(self, fileName:str, mode:str='r'):
        self.file = None
        self.fileName = fileName
        self.mode = mode

    def exists(self, path:str=None):
        if path is None:
            return os.path.exists(self.fileName)
        else:
            return os.path.exists(path)

    def open(self, fileName, atr):
        try:
            self.fileName = fileName
            self.mode = atr
            self.file = open(self.fileName, self.mode)
        except:
            fileName = fileName.replace('/','^').replace('\\','^').replace(':','^')
            self.file = open(f'I tried to open the file [{fileName}] here.txt','w')
            self.file.close()
            raise Exception(f'File {fileName} could not be openned.')
            

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def isClose(self):
        return self.file is None


    def write(self, text:str):
        if self.file is not None or self.fileName is not None:
            if self.mode == "r":
                if self.file != None:
                    self.file.close()
                self.open(self.fileName, "w")
            
            if(self.file is None):
                self.open(self.fileName, "w")
            self.file.write(text)



    def read(self):
        if self.file is None:
            self.open(self.fileName,'r')
        txt = self.file.read()
        self.close()
        return txt
    

    def readLines(self):
        if self.file is None:
            self.open(self.fileName,'r')
        lst = self.file.readlines()
        self.close()
        return lst

    def remove(self):
        self.close()
        if self.fileName is not None:
            os.remove(self.fileName)

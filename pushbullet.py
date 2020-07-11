from pushbullet import Pushbullet as PB

class Pushbullet:
    
    def __init__(self,key:str, deviceNickname:str=None):
        self.pb = PB(key)
        self.device = None
        if deviceNickname != None:
            for e in self.pb.devices:
                if e.nickname == deviceNickname:
                    self.device = e
                    break
        if self.device == None:
            self.device = self.pb

    def sendMessage(self, title:str, body:str, deviceNickname:str=None):
        if deviceNickname == None:
            return self.device.push_note(title, body)
        else:
            for e in self.pb.devices:
                if e.nickname == deviceNickname:
                    return e.push_note(title, body)
        return None

    def getListDevices(self):
        return self.pb.devices
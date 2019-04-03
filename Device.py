
from Statement import StatementType, Statement
import Util

class Device:
    name = ''
    nodes = []
    internalNodes = []
    additionalNodes = []
    model = ''
    instantParams = []
    errorMsg = ''
    def __init__(self):
        pass
    def AddNodes(self, globalNodes):
        pass
    @classmethod
    def CreateDevice(devType):
        if devType == None:
            return None
        if not StatementType.IsValidDeviceType(devType):
            return None
        if devType == StatementType.R:
            return Device_R()
        elif devType == StatementType.C:
            return Device_C()
        elif devType == StatementType.L:
            return Device_L()
        else:
            return None

    def ReadDevice(self, content):
        if content == None:
            return None

    def GetErrorMessage(self):
        return self.errorMsg

class Device_R(Device):
    def __init__(self):
        pass
    def ReadDevice(self, content):
        if content == None:
            self.errorMsg = "None content"
            return False
        if len(content) < 2:
            self.errorMsg = "Invalid content"
            return False
        word, content = Util.GetNextWord(content)
        self.name = word
        for i in range(2):
            word, content = Util.GetNextWord(content)
            if len(word) == 0:
                self.errorMsg = "Missing node name"
                return False
            else:
                self.nodes.append(word)
        word, content = Util.GetNextWord(content)
        

            

class Device_C(Device):
    def __init__(self):
        pass
    def ReadDevice(self, content):
        pass

class Device_L(Device):
    def __init__(self):
        pass
    def ReadDevice(self, content):
        pass
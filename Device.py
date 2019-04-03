
from Statement import StatementType, Statement

class Device:
    __name = ''
    __nodes = []
    __model = ''
    __instantParams = []
    __errorMsg = ''
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
            device = Device_R()
            return device

    def ReadDevice(self, content):
        if content == None:
            return None

    def GetErrorMessage(self):
        return self.__errorMsg

class Device_R(Device):
    def __init__(self):
        pass
    def ReadDevice(self, content):
        pass

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

class ModelCore:
    def SetParam(self, parName, parValue):
        return False
    def ReadModelCard(self, pvMap):
        return False
    def PrintModelCard(self):
        return ''
    def SetInputNodes(self, nodes):
        return False
    def GetDCDevices(self):
        return None
    def GetACDevices(self):
        return None
    def GetTranDevices(self):
        return None
    def IsModelValid(self):
        return False
    def SetInstanceName(self, devName):
        return False
    def SetInstanceParam(self, parName, parValue):
        return False


    
    
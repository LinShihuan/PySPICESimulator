

class ModelCore:
    
    def __init__(self):
        self.__instName = ''

    def SetParam(self, parName, parValue):
        return False
    def ReadModelCard(self, pvMap):
        return False
    def PrintModelCard(self):
        return ''
    def SetInputNodes(self, nodes):
        return False
    def GetDCInnerNodes(self):        
        return None
    def GetACInnerNodes(self):
        return None
    def GetTRANInnerNodes(self):
        return None
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
    
    def Copy(self):
        return None

    def Evalueate(self):
        return False

    
        
        


    
    
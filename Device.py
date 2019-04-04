
from Statement import StatementType, Statement
import Util

class Device:
    name = ''
    nodes = []
    internalNodes = []
    additionalNodes = []
    instantParams = {}
    model = ''    
    errorMsg = ''
    value = ''

    def __init__(self):
        pass
    
    def __str__(self):
        retStr = self.name
        for node in self.nodes:
            retStr += ' ' + node
        if len(self.value) > 0:
            retStr += ' ' + self.value  
        else:
            retStr += ' ' + self.model
        return retStr

    def AddNodes(self, globalNodes):
        pass
    @staticmethod
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
        elif devType == StatementType.V:
            return Device_V()
        elif devType == StatementType.I:
            return Device_I()
        else:
            return None

    def ReadDevice(self, content):
        if content == None:
            return None
    def ResetList(self):
        self.nodes = []
        self.internalNodes = []
        self.additionalNodes = []
        self.instantParams = {}


    def GetErrorMessage(self):
        return self.errorMsg
    def ReadRCL(self, content):
        if content == None:
            self.errorMsg = "None content"
            return False
        if len(content) < 2:
            self.errorMsg = "Invalid content"
            return False
        word, content = Util.GetNextWord(content)
        #resistor name
        self.name = word
        #two nodes
       
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = "Missing node name"
            return False
        else:
            self.nodes.append(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = "Missing node name"
            return False
        else:
            self.nodes.append(word)

        word, content = Util.GetNextWord(content)
        #value or model
        if Util.IsValidGlobalModel(word):
            self.model = word
        else:
            self.value = word          
        if len(content) > 0:  
            if content.find(','):
                content = content.replace(',', ' ')        
            pvPairs = content.split(' ')
            for pvPair in pvPairs:
                parName, parValue = Util.DivideNameValue(pvPair)
                self.instantParams[parName] = parValue
        return True
    def ReadSimpleVI(self, content):
        valueType = 'DC'
        if content == None:
            self.errorMsg = "None content"
            return False
        if len(content) < 2:
            self.errorMsg = "Invalid content"
            return False
        word, content = Util.GetNextWord(content)
        #resistor name
        self.name = word
        #two nodes
       
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = "Missing node name"
            return False
        else:
            self.nodes.append(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = "Missing node name"
            return False
        else:
            self.nodes.append(word)

        word, content = Util.GetNextWord(content)
        if word == 'DC' or word == 'AC' or word == 'TRAN':
            valueType = word
            word, content = Util.GetNextWord(content)
        #only support simple value source first        
        self.value = word
        if valueType == 'DC':
            self.DCValue = word
        elif valueType == 'AC':
            self.ACValue = word
        elif valueType == 'TRAN':
            self.TRANValue = word
        else:
            self.DCValue = word
        return True


class Device_R(Device):
    def __init__(self):
        self.ResetList()
    def ReadDevice(self, content):        
        return self.ReadRCL(content)               

class Device_C(Device):
    def __init__(self):
        self.ResetList()      
    def ReadDevice(self, content):        
        return self.ReadRCL(content)

class Device_L(Device):
    def __init__(self):
        self.ResetList()
    def ReadDevice(self, content):        
        return self.ReadRCL(content)

class Device_V(Device):
    def __init__(self):
        self.ResetList()
        self.ACValue = ''
        self.DCValue = ''
        self.TRANValue = ''
    def ReadDevice(self, content):
        return self.ReadSimpleVI(content)

class Device_I(Device):
    def __init__(self):
        self.ResetList()
        self.ACValue = ''
        self.DCValue = ''
        self.TRANValue = ''
    def ReadDevice(self, content):
        return self.ReadSimpleVI(content)
        

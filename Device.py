
from Statement import StatementType, Statement
import Util

class Device:
    name = ''
    __nodes = []
    dcNodes = []
    acNodes = []
    tranNodes = []
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
        for node in self.__nodes:
            retStr += ' ' + node
        if len(self.value) > 0:
            retStr += ' ' + self.value  
        else:
            retStr += ' ' + self.model
        return retStr

    def AddNode(self, node):
        if node == None:
            return False
        node = node.upper().strip()
        if node == '0':
            node = 'GND'        
        self.__nodes.append(node)
    def AddDCNode(self, dcNode):
        self.dcNodes.append(dcNode)
    def AddACNode(self, acNode):
        self.acNodes.append(acNode)

    def GetNode(self, index):
        if index > len(self.__nodes):
            return None
        return self.__nodes[index-1]        

    def GetBRNode(self):
        return 'BR.' + self.name

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
        self.__nodes = []
        self.internalNodes = []
        self.additionalNodes = []
        self.instantParams = {}
        self.dcNodes = []
        self.acNodes = []
        self.tranNodes = []


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
            self.AddNode(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = "Missing node name"
            return False
        else:
            self.AddNode(word)

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
            self.AddNode(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = "Missing node name"
            return False
        else:
            self.AddNode(word)

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
    
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        return False
        
    def CreateDCNodes(self):
        if len(self.dcNodes) > 0:
            return False
        for node in self.__nodes:            
            self.dcNodes.append(node)
        self.AddDCExtraNodes()
        return True
    def GetDCNodes(self):
        self.CreateDCNodes()
        return self.dcNodes
    def CreateACNodes(self):
        if len(self.acNodes) > 0:
            return False
        for node in self.__nodes:
            self.dcNodes.append(node)
        self.AddACExtraNodes()
        return True
    def AddDCExtraNodes(self):
        pass
    def AddACExtraNodes(self):
        pass
    def GetACNodes(self):
        return self.acNodes


class Device_R(Device):
    def __init__(self):
        self.ResetList()
    def ReadDevice(self, content):        
        return self.ReadRCL(content)              
         
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False
        dblVal = Util.EvaluateValue(self.value)
        if dblVal == 0:
            dblVal = 1.0e-15
        dblVal = 1/dblVal
        nodeOne = self.GetNode(1)
        nodeTwo = self.GetNode(2)
        if nodeOne == None or nodeTwo == None:
            return False
        idx1 = dcNodes.GetIndex(nodeOne)
        idx2 = dcNodes.GetIndex(nodeTwo)
        if idx1 < 0 or idx2 < 0:
            return False
        dcMatrix[idx1, idx1] += dblVal
        dcMatrix[idx2, idx2] += dblVal
        dcMatrix[idx1, idx2] -= dblVal
        dcMatrix[idx2, idx1] -= dblVal
        return True
     
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

    def AddDCExtraNodes(self):
        vNode = self.GetBRNode()
        self.AddDCNode(vNode)
    
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False
        dblVal = Util.EvaluateValue(self.DCValue)
        if dblVal == 0:
            dblVal = 1.0e-15

        nodeOne = self.GetNode(1)
        nodeTwo = self.GetNode(2)
        nodeBR = self.GetBRNode()

        if nodeOne == None or nodeTwo == None:
            return False
        idx1 = dcNodes.GetIndex(nodeOne)
        idx2 = dcNodes.GetIndex(nodeTwo)
        idxBR = dcNodes.GetIndex(nodeBR)
        if idx1 < 0 or idx2 < 0 or idxBR < 0:
            return False
        dcMatrix[idx1, idxBR] += 1
        dcMatrix[idx2, idxBR] += -1
        dcMatrix[idxBR, idx1] += 1
        dcMatrix[idxBR, idx2] += -1

        dcRHS[idxBR] += dblVal
        return True

class Device_I(Device):
    def __init__(self):
        self.ResetList()
        self.ACValue = ''
        self.DCValue = ''
        self.TRANValue = ''
    def ReadDevice(self, content):
        return self.ReadSimpleVI(content)

    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False
        dblVal = Util.EvaluateValue(self.DCValue)
        
        nodeOne = self.GetNode(1)
        nodeTwo = self.GetNode(2)
        if nodeOne == None or nodeTwo == None:
            return False
        idx1 = dcNodes.GetIndex(nodeOne)
        idx2 = dcNodes.GetIndex(nodeTwo)
        if idx1 < 0 or idx2 < 0:
            return False
        dcRHS[idx1] -= dblVal
        dcRHS[idx2] += dblVal
        return True

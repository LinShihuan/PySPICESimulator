
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
    __DCValue = ''
    __ACValue = ''
    __TranValue = ''

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
    def GetAllNodes(self):
        return self.__nodes

    def GetBRNode(self):
        return 'BR.' + self.name
    def GetBR2Node(self):
        return 'BR2.' + self.name

    def GetValue(self):
        return self.value
    def SetValue(self, inVal):
        if inVal == None or len(inVal.strip()) == 0:
            return False
        self.value = inVal
        return True
    def GetDCValue(self):
        return self.__DCValue
    def SetDCValue(self, inVal):
        if inVal == None or len(inVal.strip()) == 0:
            return False
        self.__DCValue = inVal
        return True
    def GetACValue(self):
        return self.__ACValue
    def SetACValue(self, inVal):
        if inVal == None or len(inVal.strip()) == 0:
            return False
        self.__ACValue = inVal
        return True    
    def GetTranValue(self):
        return self.__TranValue
    def SetTranValue(self, inVal):
        if inVal == None or len(inVal.strip()) == 0:
            return False
        self.__TranValue = inVal
        return True

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
        elif devType == StatementType.E:
            return Device_E()
        elif devType == StatementType.G:
            return Device_G()    
        elif devType == StatementType.F:
            return Device_F()
        elif devType == StatementType.H:
            return Device_H()
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
            self.SetDCValue(word)
            self.SetACValue(word)
            self.SetTranValue(word)
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
            self.__DCValue = word
        elif valueType == 'AC':
            self.__ACValue = word
        elif valueType == 'TRAN':
            self.__TranValue = word
        else:
            self.__DCValue = word
        return True
    
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        return False
        
    def CreateDCNodes(self, devices):
        if len(self.dcNodes) > 0:
            return False
        for node in self.__nodes:            
            self.dcNodes.append(node)
        self.AddDCExtraNodes(devices)
        return True
    def GetDCNodes(self, devices):
        self.CreateDCNodes(devices)
        return self.dcNodes
    def CreateACNodes(self, devices):
        if len(self.acNodes) > 0:
            return False
        for node in self.__nodes:
            self.dcNodes.append(node)
        self.AddACExtraNodes(devices)
        return True
    def AddDCExtraNodes(self, devices):
        pass
    def AddACExtraNodes(self, devices):
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
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False        
        dblVal = 1e-12
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

class Device_L(Device):
    def __init__(self):
        self.ResetList()
    def ReadDevice(self, content):        
        return self.ReadRCL(content)
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False        
        dblVal = 1e+12
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

class Device_V(Device):
    def __init__(self):
        self.ResetList()
        
    def ReadDevice(self, content):
        return self.ReadSimpleVI(content)

    def AddDCExtraNodes(self, devices):
        vNode = self.GetBRNode()
        self.AddDCNode(vNode)
    
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False
        dblVal = Util.EvaluateValue(self.GetDCValue())
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
       
    def ReadDevice(self, content):
        return self.ReadSimpleVI(content)

    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False
        dblVal = Util.EvaluateValue(self.GetDCValue())
        
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

class Device_E(Device):
    def __init__(self):
        self.ResetList()

    def AddDCExtraNodes(self, devices):
        vNode = self.GetBRNode()
        self.AddDCNode(vNode)
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False
        dblVal = Util.EvaluateValue(self.GetDCValue())
        
        nodeOne = self.GetNode(1)
        nodeTwo = self.GetNode(2)
        nodeThree = self.GetNode(3)
        nodeFour = self.GetNode(4)
        nodeBR = self.GetBRNode()
        if nodeOne == None or nodeTwo == None or nodeThree == None or nodeFour == None or nodeBR == None:
            return False
        idx1 = dcNodes.GetIndex(nodeOne)
        idx2 = dcNodes.GetIndex(nodeTwo)
        idx3 = dcNodes.GetIndex(nodeThree)
        idx4 = dcNodes.GetIndex(nodeFour)
        idxBR = dcNodes.GetIndex(nodeBR)
        if idx1 < 0 or idx2 < 0 or idx3 < 0 or idx4 < 0 or idxBR < 0:
            return False
        dcMatrix[idxBR, idx1] -= dblVal
        dcMatrix[idxBR, idx2] += dblVal
        dcMatrix[idxBR, idx3] += 1
        dcMatrix[idxBR, idx4] -= 1
        dcMatrix[idx3, idxBR] += 1
        dcMatrix[idx4, idxBR] -= 1
        return True

    def ReadDevice(self, content):
        if content == None or len(content) < 7:
            self.errorMsg = 'Invalid content'
            return False
        word, content = Util.GetNextWord(content)
        self.name = word
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
        
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid value'
            return False
        else:
            self.value = word
            self.SetDCValue(word)
            self.SetACValue(word)
            self.SetTranValue(word)

        return True

class Device_G(Device):
    def __init__(self):
        self.ResetList()
    
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False
        dblVal = Util.EvaluateValue(self.GetDCValue())
        
        nodeOne = self.GetNode(1)
        nodeTwo = self.GetNode(2)
        nodeThree = self.GetNode(3)
        nodeFour = self.GetNode(4)        
        if nodeOne == None or nodeTwo == None or nodeThree == None or nodeFour == None:
            return False
        idx1 = dcNodes.GetIndex(nodeOne)
        idx2 = dcNodes.GetIndex(nodeTwo)
        idx3 = dcNodes.GetIndex(nodeThree)
        idx4 = dcNodes.GetIndex(nodeFour)
        if idx1 < 0 or idx2 < 0 or idx3 < 0 or idx4 < 0:
            return False
        dcMatrix[idx3, idx1] += dblVal
        dcMatrix[idx3, idx2] -= dblVal
        dcMatrix[idx4, idx1] -= dblVal
        dcMatrix[idx4, idx2] += dblVal   
        return True

    def ReadDevice(self, content):
        if content == None or len(content) < 7:
            self.errorMsg = 'Invalid content'
            return False
        word, content = Util.GetNextWord(content)
        self.name = word
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
        
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid value'
            return False
        else:
            self.value = word
            self.SetDCValue(word)
            self.SetACValue(word)
            self.SetTranValue(word)
            
        return True

class Device_F(Device):
    def __init__(self):
        self.ResetList()
        self.DependentSource = ''

    def AddDCExtraNodes(self, devices):
        vNode = self.GetBRNode()
        self.AddDCNode(vNode)
        #add the node for DenpendentSource
        for dev in devices:
            if self.DependentSource == dev.name:
                self.AddNode(dev.GetNode(1))
                self.AddNode(dev.GetNode(2))
                break        

    def __str__(self):
        retStr = self.name
        for node in self.GetAllNodes():
            retStr += ' ' + node
        if len(self.DependentSource) > 0:
            retStr += ' ' + self.DependentSource
        if len(self.value) > 0:
            retStr += ' ' + self.value  
        else:
            retStr += ' ' + self.model
        return retStr
    
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False
        dblVal = Util.EvaluateValue(self.GetDCValue())
        
        nodeOne = self.GetNode(1)
        nodeTwo = self.GetNode(2)
        nodeThree = self.GetNode(3)
        nodeFour = self.GetNode(4)
        nodeBR = self.GetBRNode()
        if nodeOne == None or nodeTwo == None or nodeThree == None or nodeFour == None or nodeBR == None:
            return False
        idx1 = dcNodes.GetIndex(nodeOne)
        idx2 = dcNodes.GetIndex(nodeTwo)
        idx3 = dcNodes.GetIndex(nodeThree)
        idx4 = dcNodes.GetIndex(nodeFour)
        idxBR = dcNodes.GetIndex(nodeBR)
        if idx1 < 0 or idx2 < 0 or idx3 < 0 or idx4 < 0 or idxBR < 0:
            return False
        dcMatrix[idx1, idxBR] += 1
        dcMatrix[idx2, idxBR] -= 1
        dcMatrix[idx3, idxBR] += dblVal
        dcMatrix[idx4, idxBR] -= dblVal
        dcMatrix[idxBR, idx1] += 1
        dcMatrix[idxBR, idx2] -= 1
        return True

    def ReadDevice(self, content):
        if content == None or len(content) < 7:
            self.errorMsg = 'Invalid content'
            return False
        word, content = Util.GetNextWord(content)
        self.name = word
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
       
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid Voltage Source'
            return False
        else:
            self.DependentSource = word
        
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid value'
            return False
        else:
            self.value = word
            self.SetDCValue(word)
            self.SetACValue(word)
            self.SetTranValue(word)
            
        return True    

class Device_H(Device):
    def __init__(self):
        self.ResetList()
        self.DependentSource = ''

    def AddDCExtraNodes(self, devices):
        vNode = self.GetBRNode()
        self.AddDCNode(vNode)
        v2Node = self.GetBR2Node()
        self.AddDCNode(v2Node)
        #add the node for DenpendentSource
        for dev in devices:
            if self.DependentSource == dev.name:
                self.AddNode(dev.GetNode(1))
                self.AddNode(dev.GetNode(2))
                break    

    def __str__(self):
        retStr = self.name
        for node in self.GetAllNodes():
            retStr += ' ' + node
        if len(self.DependentSource) > 0:
            retStr += ' ' + self.DependentSource
        if len(self.value) > 0:
            retStr += ' ' + self.value  
        else:
            retStr += ' ' + self.model
        return retStr
    def FillDCMatrix(self, dcNodes, dcMatrix, dcRHS):
        if dcNodes.Size() == 0:
            return False
        dblVal = Util.EvaluateValue(self.GetDCValue())
        
        nodeOne = self.GetNode(1)
        nodeTwo = self.GetNode(2)
        nodeThree = self.GetNode(3)
        nodeFour = self.GetNode(4)
        nodeBR = self.GetBRNode()
        nodeBR2 = self.GetBR2Node()
        if nodeOne == None or nodeTwo == None or nodeThree == None or nodeFour == None or nodeBR == None or nodeBR2 == None:
            return False
        idx1 = dcNodes.GetIndex(nodeOne)
        idx2 = dcNodes.GetIndex(nodeTwo)
        idx3 = dcNodes.GetIndex(nodeThree)
        idx4 = dcNodes.GetIndex(nodeFour)
        idxBR = dcNodes.GetIndex(nodeBR)
        idxBR2 = dcNodes.GetIndex(nodeBR2)
        if idx1 < 0 or idx2 < 0 or idx3 < 0 or idx4 < 0 or idxBR < 0 or idxBR2 < 0:
            return False
        dcMatrix[idx1, idxBR] += 1
        dcMatrix[idx2, idxBR] -= 1
        dcMatrix[idx3, idxBR2] += 1
        dcMatrix[idx4, idxBR2] -= 1
        dcMatrix[idxBR, idx1] += 1
        dcMatrix[idxBR, idx2] -= 1
        dcMatrix[idxBR2, idx3] += 1
        dcMatrix[idxBR2, idxBR] -= dblVal
        return True

    def ReadDevice(self, content):
        if content == None or len(content) < 7:
            self.errorMsg = 'Invalid content'
            return False
        word, content = Util.GetNextWord(content)
        self.name = word
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid node'
            return False
        else:
            self.AddNode(word)       
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid Voltage Source'
            return False
        else:
            self.DependentSource = word        
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.errorMsg = 'Invalid value'
            return False
        else:
            self.value = word
            self.SetDCValue(word)
            self.SetACValue(word)
            self.SetTranValue(word)
            
        return True    

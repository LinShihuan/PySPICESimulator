
from Parameter import Parameter
from Util import EvaluateValue
from Util import ModelType
import numpy as np
from ModelDevice import ModelDevice
from ModelCore import ModelCore

modelType = ModelType()

class ResistorModelCore(ModelCore):
    
    def __init__(self):
        self.__L = Parameter('1.0e-6')
        self.__W = Parameter('1.0e-6')
        self.__TEMP = Parameter('27.0')
        #model parameters
        self.__TC1 = Parameter('0.0')
        self.__TC2 = Parameter('0.0')
        self.__RSH = Parameter('50')
        self.__DEFW = Parameter('1.0e-6')
        self.__NARROW = Parameter('0.0')
        self.__TNOM = Parameter('27.0')
        self.__node1 = Parameter('')
        self.__node2 = Parameter('')
        self.__resistance = 0.0
    
    def Copy(self):
        ret = ResistorModelCore()
        ret.__TC1 = self.__TC1
        ret.__TC2 = self.__TC2
        ret.__RSH = self.__RSH
        ret.__DEFW = self.__DEFW
        ret.__NARROW = self.__NARROW
        ret.__TNOM = self.__TNOM
        return ret

    def ResetInstance(self):
        self.__L.Reset()
        self.__W.Reset()
        self.__TEMP.Reset()

    def SetParam(self, parName, parValue):
        if parName == None or len(parName) == 0:
            return False
        if parValue == None or len(parValue) == 0:
            return False
        ret = True
        if parName == 'TC1':
            self.__TC1 = parValue            
        elif parName == 'TC2':
            self.__TC2 = parValue
        elif parName == 'RSH':
            self.__RSH = parValue
        elif parName == 'DEFW':
            self.__DEFW = parValue
        elif parName == 'NARROW':
            self.__NARROW = parValue
        elif parName == 'TNOM':
            self.__TNOM = parValue
        else:
            ret = False
        return ret

    def ReadModelCard(self, pvMap):
        if pvMap == None:  
            return False
        ret = True
        for key, value in pvMap.items():
            ret = (ret and self.SetParam(key, value))
        return ret

    def PrintModelCard(self):
        ret = 'TC1=' + self.__TC1 + ' TC2=' + self.__TC2 + ' RSH=' + self.__RSH + ' DEFW=' + self.__DEFW + ' NARROW=' + self.__NARROW + ' TNOM=' + self.__TNOM
        return ret 

    def SetInputNodes(self, nodes):
        if nodes == None or len(nodes) < 2:
            return False
        self.__node1 = nodes[0]
        self.__node2 = nodes[1]
        return True

    def SetInstanceName(self, devName):
        if devName == None or len(devName) < 1:
            return False
        self.__instName = devName
            
    def SetInstanceParam(self, parName, parValue):
        if parName == None or len(parName) == 0 or parValue == None or len(parValue) == 0:
            return False
        if parName == 'L':
            self.__L = parValue
        elif parName == 'W':
            self.__W = parValue
        elif parName == 'TEMP':
            self.__TEMP = parValue
        else:
            return False
        return True           

    def GetDCDevices(self):
        if not self.__L.IsGiven():
            return None
        self.Evalueate()
        retDevice = ModelDevice('mdlR1', [self.__node1, self.__node2], self.__resistance, modelType.R)
        return retDevice

    def GetACDevices(self):
        return None

    def GetTranDevices(self):
        return None

    def IsModelValid(self):
        if not self.__L.IsGiven():
            return False
        return True

    def Evalueate(self):
        rsh = EvaluateValue(self.__RSH.GetValue())
        l = EvaluateValue(self.__L.GetValue())
        if not self.__W.IsGiven():
            w = EvaluateValue(self.__DEFW.GetValue())
        else:
            w = EvaluateValue(self.__W.GetValue())
        narrow = EvaluateValue(self.__NARROW.GetValue())
        temp = EvaluateValue(self.__TEMP.GetValue())
        tnom = EvaluateValue(self.__TNOM.GetValue())
        if w - narrow < 1e-15:
            w = narrow + 1e-15
        self.__resistance = rsh * (l - narrow) / (w - narrow)
        if np.abs(temp - tnom) > 1e-3:
            tc1 = EvaluateValue(self.__TC1.GetValue())
            tc2 = EvaluateValue(self.__TC2.GetValue())
            self.__resistance = self.__resistance * (1+tc1*(temp-tnom)+tc2*((temp-tnom)**2))
        return True


    

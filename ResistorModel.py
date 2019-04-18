
from Device import Device
from Device import Device_R

class ResistorModelCore:
    
    def __init__(self):
        self.__L = '1.0'
        self.__W = '1.0'
        self.__TEMP = '27.0'
        #model parameters
        self.__TC1 = '0.0'
        self.__TC2 = '0.0'
        self.__RSH = '50'
        self.__DEFW = '1.0e-6'
        self.__NARROW = '0.0'
        self.__TNOM = '27.0'
        self.__node1 = ''
        self.__node2 = ''

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
        for key, value in pvMap.iteritems():
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

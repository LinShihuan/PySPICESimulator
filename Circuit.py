#class for the circuit
#circuit contains subcircuit, model card, device instants, parameters, options, analyses, outputs
from Nodes import Nodes
import numpy as np 
from Device import Device

class Circuit:
    __devices = []
    __modelCards = []
    __subckts = []
    __option = []
    __analyses = []
    __outputs = []
    __params = {}
    __dcMatrix = None
    __acMatrix = None
    __tranMatrix = None
    __dcNodes = Nodes()
    __acNodes = Nodes()
    __tranNodes = Nodes()
    def __init__(self):
        pass
    @property
    def Devices(self):
        return self.__devices
    @property
    def ModelCards(self):
        return self.__modelCards
    @property
    def Subckts(self):
        return self.__subckts
    @property 
    def Optios(self):
        return self.__option
    @property
    def Analyses(self):
        return self.__analyses
    @property 
    def Outputs(self):
        return self.__outputs
    @property
    def Params(self):
        return self.__params
    @property 
    def DCNodes(self):
        return self.__dcNodes

    def AddDevice(self, dev):
        if dev == None:
            return False
        else:
            self.__devices.append(dev)
        return True
    
    def BuildDCMatrix(self):
        self.CreateDCNodes()
        size = self.__dcNodes.Size()
        if size > 0:
            self.__dcMatrix = np.zero([size, size])
        print(self.__dcMatrix)

    def UpdateDCMatrix(self, device):
        pass

    def SolveDCMatrix(self):
        pass

    def CreateDCNodes(self):
        for dev in self.__devices:
            if not dev == None:
                for node in dev.GetDCNodes():
                    self.__dcNodes.AddNode(node)
    
        
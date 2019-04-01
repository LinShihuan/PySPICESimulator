#class for the circuit
#circuit contains subcircuit, model card, device instants, parameters, options, analyses, outputs

class Circuit:
    __devices = []
    __modelCards = []
    __subckts = []
    __option = []
    __analyses = []
    __outputs = []
    __params = {}
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
        
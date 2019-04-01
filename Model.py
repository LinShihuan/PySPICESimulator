#define the model card base class
class __ModelType:
    __R = 'Resistor'
    __C = 'Capacitor'
    __L = 'Inductor'
    __N = 'NMOS'
    __P = 'PMOS'
    __D = 'DIODE'
    __Q = 'BJT'
    __Unknown = 'Unknwon'
    def __init__(self):
        pass
    @property
    def R(self):
        return self.__R
     @property
    def C(self):
        return self.__C
     @property
    def L(self):
        return self.__L
     @property
    def N(self):
        return self.__N
     @property
    def P(self):
        return self.__P
     @property
    def D(self):
        return self.__D
     @property
    def Q(self):
        return self.__Q
    @property
    def Unknown(self):
        return self.__Unknown
modelType = __ModelType()

class Model:
    __name = ''
    __type = modelType.Unknown
    __level = ''
    __params = {}
    __loaded = False
    def __init__(self):
        pass
        
    def ReadModel(self, content):
        #it starts with .model
        pass

    def IsValidModel(self):
        if self.__loaded and (not self.__type == modelType.Unknown):
            return True
        return False

    def GetName(self):
        return self.__name

    def GetParams(self):
        return self.__params
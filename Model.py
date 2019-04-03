#define the model card base class
import Util

class __ModelType:
    __R = 'Resistor'
    __C = 'Capacitor'
    __L = 'Inductor'
    __N = 'NMOS'
    __P = 'PMOS'
    __D = 'DIODE'
    __Q = 'BJT'
    __Unknown = 'Unknwon'
    __SupportModel = [__R, __C, __L, __N, __P, __D, __Q]
    
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
    def IsValidType(self, mType):
        if mType in self.__SupportModel:
            return True
        return False 
    
modelType = __ModelType()

class Model:
    __name = ''
    __type = modelType.Unknown
    __level = ''
    __params = {}
    __errorMsg = ''
    def __init__(self):
        pass
        
    def ReadModel(self, content):
        #it starts with .model
        word, content = Util.GetNextWord(content)
        if not word == '.MODEL':
            self.__errorMsg = 'Not a valid model statement'
            return False
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            self.__errorMsg = 'model name is missing'
            return False
        else:
            self.__name = word
        word, content = Util.GetNextWord(content)
        if not modelType.IsValidType(word):
            self.__errorMsg = 'invalid model type'
        else:
            self.__type = word
        if len(content) == 0:
            return True
        if not (content[0] == '(' and content[-1] == ')') or len(content) < 2:
            self.__errorMsg = '() is missing'
            return False
        content = Util.RemoveSpace(content[1:-2])
        if content.find(','):
            content = content.replace(',', ' ')        
        words = content.split(' ')
        for pvPair in words:
            pName, pValue = Util.DivideNameValue(pvPair)
            if len(pName) == 0 or len(pValue) == 0:
                self.__errorMsg = 'Unknown model parameter or value'
                return False
            self.__params[pName] = pValue
        
        return True
        
    

    def IsValidModel(self):
        if  (not self.__type == modelType.Unknown) and (len(self.__errorMsg) == 0):
            return True
        return False

    def GetName(self):
        return self.__name

    def GetParams(self):
        return self.__params

    def GetErrorMessage(self):
        return self.__errorMsg
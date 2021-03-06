class __StatementType:
    __R = 'Resitor'
    __C = 'Capcitor'
    __L = 'Inductor'
    __D = 'Didoe'
    __Q = 'BJT'
    __M = 'MOS'
    __V = 'Voltage'
    __I = 'Current'
    __E = 'VCCS'
    __F = 'VCVS'
    __G = 'CCCS'
    __H = 'CCVS'
    __Model = 'Model'
    __SUBCKT_START = 'SUBCKT_START'
    __SUBCKT_END = 'SUBCKT_END'
    __Option = 'OPTION'
    __Param = 'PARAM'
    __Analyses = 'ANALYSES'
    __Output = 'OUTPUT'
    __Unknown = 'UNKNOWN'
    __End = 'END'
    __SupporttedDevice = [__R, __C, __L, __D, __Q, __M, __V, __I, __E, __F, __G, __H]

    def __init__(self):
        pass
    
    def IsValidDeviceType(self, devType):
        if devType == None:
            return False
        elif devType in self.__SupporttedDevice:
            return True
        else:
            return False
        
    @property
    def Unknown(self):
        return self.__Unknown
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
    def D(self):
        return self.__D
    @property
    def Q(self):
        return self.__Q
    @property
    def M(self):
        return self.__M
    @property
    def V(self):
        return self.__V
    @property
    def I(self):
        return self.__I
    @property
    def E(self):
        return self.__E
    @property
    def F(self):
        return self.__F
    @property
    def G(self):
        return self.__G
    @property
    def H(self):
        return self.__H
    @property
    def Model(self):
        return self.__Model
    @property
    def Subckt_Start(self):
        return self.__SUBCKT_START
    @property
    def Subckt_End(self):
        return self.__SUBCKT_END
    @property
    def Option(self):
        return self.__Option
    @property
    def Param(self):
        return self.__Param
    @property
    def Analyses(self):
        return self.__Analyses
    @property
    def Output(self):
        return self.__Output
    @property
    def End(self):
        return self.__End

StatementType = __StatementType()

class Statement:
    #Type: DEVICE.(R, C, L, D, Q, M, V, I, E, F, G, H), MODEL, SUBCKT_START, SUBCKT_END, OPTION, PARAM, ANALYSES, OUTPUT, UNKNOWN
    def __init__(self, num, content):
        self.SetContent(num, content)

    def SetContent(self, num, content):
        self.lineIndex = num
        self.content = content.strip().upper()
        self.type = self.__FindType(self.content)
    
    #for testing only
    def __str__(self):
        return str(self.lineIndex) + ' ' + self.type + ' ' + self.content

    @classmethod
    def __FindType(self, content):
        self.type = StatementType.Unknown
        content = content.upper()
        if len(content) < 1:
            self.type = 'UNKNOWN'
            return
        if content[0] == '.':
            #control, output, model, analyses, subckt
            if content.find('.MODEL ') == 0:
                self.type = StatementType.Model
            elif content.find('.SUBCKT ') == 0:
                self.type = StatementType.Subckt_Start
            elif content.find('.ENDS') == 0:
                self.type = StatementType.Subckt_End
            elif content.find('.OPTION ') == 0:
                self.type = StatementType.Option
            elif content.find('.PARAM ') == 0:
                self.type = StatementType.Param
            elif content.find('.OP') == 0:
                self.type = StatementType.Analyses
            elif content.find('.DC ') == 0:
                self.type = StatementType.Analyses
            elif content.find('.AC ') == 0:
                self.type = StatementType.Analyses
            elif content.find('.TRAN ') == 0:
                self.type = StatementType.Analyses                
            elif content.find('.NOISE ') == 0:
                self.type = StatementType.Analyses                                
            elif content.find('.PRINT ') == 0:
                self.type = StatementType.Output
            elif content.find('.PLOT ') == 0:
                self.type = StatementType.Output
        elif content[0] == 'R':
            self.type = StatementType.R
        elif content[0] == 'C':
            self.type = StatementType.C
        elif content[0] == 'L':
            self.type = StatementType.L
        elif content[0] == 'D':
            self.type = StatementType.D
        elif content[0] == 'Q':
            self.type = StatementType.Q
        elif content[0] == 'M':
            self.type = StatementType.M
        elif content[0] == 'V':
            self.type = StatementType.V
        elif content[0] == 'I':
            self.type = StatementType.I
        elif content[0] == 'E':
            self.type = StatementType.E
        elif content[0] == 'F':
            self.type = StatementType.F
        elif content[0] == 'G':
            self.type = StatementType.G
        elif content[0] == 'H':
            self.type = StatementType.H

        return self.type
        

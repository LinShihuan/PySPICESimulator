import numpy as np
from Circuit import Circuit
import Util

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

    def __init__(self):
        pass
        
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
        



class Netlist:    
    __statements = []
    __fileName = ''
    __circuit = None
    def __init__(self, inputFile):
        self.__fileName = inputFile
        self.__circuit = Circuit()

    def Preprocess(self):
        lineIndex = 0
        strLine = ""
        with open(self.__fileName, "r") as netFile:
            tmpLine = netFile.readline()
            while len(tmpLine) > 0:
                tmpLine = tmpLine.strip()
                lineIndex += 1
                if lineIndex == 1 or len(tmpLine) == 0:
                    pass
                elif tmpLine[0] == '*':
                    pass
                elif tmpLine[0] == '+':
                    strLine += ' ' + tmpLine[1:]
                else:
                    if strLine == '':
                        strLine = tmpLine
                        lastLine = lineIndex
                    else:
                        self.__statements.append(Statement(lastLine, strLine))
                        strLine = tmpLine
                        lastLine = lineIndex
                tmpLine = netFile.readline()
            else:
                if len(strLine) > 0:
                    self.__statements.append(Statement(lastLine, strLine))
    
    def ReadParameters(self):
        for statement in self.__statements:
            if statement.type == StatementType.Param:
                content = statement.content
                word, content = Util.GetWord(content)
                assert(word == '.PARAM')
                content = Util.TrimAtEuqalSign(content)
                words = content.split(',')
                for pvPair in words:
                    name, value = Util.DivideNameValue(pvPair)
                    if name == None or value == None:
                        raise "Error in parameter defination"
                    else:
                        self.__circuit.Params[name] = eval(value)

    def GetStatements(self):
        return self.__statements
    def GetCircuit(self):
        return self.__circuit
                                
                
                

            
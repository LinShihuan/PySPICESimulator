import numpy as np
from Circuit import Circuit
import Util
from Model import Model
from Device import Device
from Statement import StatementType, Statement
from GlobalVar import globalModelNames, globalParamNames, globalParamValues
from Analyse import Analyse, AnalyseDC, AnalyseOP, AnalyseAC

class Netlist:    
    __statements = []
    __fileName = ''
    __circuit = None
    def __init__(self, inputFile):
        self.__fileName = inputFile
        self.__circuit = Circuit()
        globalModelNames = []
        globalParamNames = []

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
                word, content = Util.GetNextWord(content)
                assert(word == '.PARAM')
                content = Util.TrimBeforeAfter('=', content)
                content = Util.TrimBeforeAfter(',', content)
                words = content.split(',')
                for pvPair in words:
                    name, value = Util.DivideNameValue(pvPair)
                    if name == None or value == None:
                        print("Error in parameter defination")
                        return False
                    else:
                        self.__circuit.Params[name] = eval(value)
                        globalParamNames.append(name)
                        globalParamValues.append(value)
        return True

    def ReadGlobalModel(self):
        level = 0
        for statement in self.__statements:
            if statement.type == StatementType.Subckt_Start:
                level = level + 1
            elif statement.type == StatementType.Subckt_End:
                level = level - 1
            elif statement.type == StatementType.Model and level == 0:
                content = statement.content 
                model = Model()
                if model.ReadModel(content):
                    self.__circuit.ModelCards.append(model)
                    globalModelNames.append(model)
                else:
                    print(model.GetErrorMessage())
                    return False
        return True

    def ReadGlobalDevice(self):
        level = 0
        for statement in self.__statements:
            if statement.type == StatementType.Subckt_Start:
                level = level + 1
            elif statement.type == StatementType.Subckt_End:
                level = level - 1
            elif StatementType.IsValidDeviceType(statement.type) and level == 0:
                content = statement.content 
                device = Device.CreateDevice(statement.type)
                if device == None:
                    print("Unsupport device:"+ str(statement))
                    return False

                if device.ReadDevice(content):
                    self.__circuit.AddDevice(device)
                else:
                    print(device.GetErrorMessage())
                    return False
        return True
        
    def ReadAnalyses(self):
        level = 0
        for statement in self.__statements:
            if statement.type == StatementType.Subckt_Start:
                level = level + 1
            elif statement.type == StatementType.Subckt_End:
                level = level - 1
            elif statement.type == StatementType.Analyses:
                if level > 1:
                    print("Analyse in subckt, error " + str(statement))
                    return False
                content = statement.content
                if content == None:
                    print("Error, empty content")
                    return False
                analyse = None
                if content.startswith('.OP'):
                    analyse = AnalyseOP()
                elif content.startswith('.DC'):
                    analyse = AnalyseDC()
                elif content.startswith('.AC'):
                    analyse = AnalyseAC()
                else:
                    print("Unspportted analyse " + str(statement))
                    return False

                if not analyse.ReadAnalyse(content):
                    print('Error analyse format ' + str(statement))
                    return False
                else:
                    self.__circuit.Analyses.append(analyse)

    def GetStatements(self):
        return self.__statements

    def GetCircuit(self):
        return self.__circuit
                                
                
                

            
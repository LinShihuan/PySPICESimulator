
import Util
import numpy as np

class Analyse:
    name = 'Analyse'
    def __init__(self):
        pass
    def __str__(self):
        return self.name 
    def ReadAnalyse(self, content):
        pass

class AnalyseOP(Analyse):
    def __init__(self):
        self.name = 'OP'
    def ReadAnalyse(self, content):
        if content == None:
            return False
        elif content == '.OP':
            return True
        return False

class AnalyseDC(Analyse):
    scanVars = {}
    def __init__(self):
        self.name = 'DC'
        self.scanVars = {}
    
    def __str__(self):
        retString = 'DC '
        for source in self.scanVars.keys():
            retString += ' ' + source + ' ' + str(self.scanVars[source][0]) + ' to ' + str(self.scanVars[source][-1]) 
        return retString

    def ReadAnalyse(self, content):
        if content == None or len(content) < 5:
            return False
        word, content = Util.GetNextWord(content)
        if not word == '.DC':
            return False
        while len(content) > 0:
            word, content = Util.GetNextWord(content)
            if len(word) > 0:
                source = word
            word, content = Util.GetNextWord(content)
            if len(word) == 0:
                return False
            else:
                start = Util.EvaluateValue(word)
            word, content = Util.GetNextWord(content)
            if len(word) == 0:
                return False
            else:
                stop = Util.EvaluateValue(word)
            word, content = Util.GetNextWord(content)
            if len(word) == 0:
                return False
            else:
                incr = Util.EvaluateValue(word)
                if incr == 0:
                    return False
            if start + incr >= stop:
                return False
            self.scanVars[source] = np.arange(start, stop+incr, incr)
        if len(self.scanVars) > 0:
            return True
        return False

class AnalyseAC(Analyse):
    def __init__(self):
        self.name = 'AC'
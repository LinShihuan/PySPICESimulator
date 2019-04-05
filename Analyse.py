
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
    frequencys = None
    mode = ''
    def __init__(self):
        self.name = 'AC'
        self.frequencys = None
        self.mode = ''

    def __str__(self):
        retString = 'AC '
        if len(self.frequencys) > 0:
            retString += self.mode + ' ' + str(self.frequencys[0]) + ' to ' + str(self.frequencys[-1]) 
        return retString

    def ReadAnalyse(self, content):
        if content == None or len(content) < 5:
            return False
        word, content = Util.GetNextWord(content)
        if not word == '.AC':
            return False
        
        word, content = Util.GetNextWord(content)
        if len(word) > 0:
            self.mode = word
        count = 0
        word, content = Util.GetNextWord(content)
        if len(word) == 0:
            return False
        else:
            count = Util.EvaluateValue(word)
            if count <= 0:
                return False
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
        
        if start < 0 or stop < 0 or start > stop:
            return False

        if self.mode == 'DEC':
            tmpFreq = []
            lastFreq = start            
            base = start
            res = 0
            while res < stop:
                for i in range(count):
                    res += lastFreq+i*base*10/count
                    if res <= stop:
                        tmpFreq.append(res)           
                base *= 10
            else:
                self.frequencys = np.array(tmpFreq)
                print(self.frequencys)
        elif self.mode == 'OCT':
            pass
        elif self.mode == 'LIN':
            self.frequencys = np.linspace(start, stop, count)
        else:
            return False     
        
        if len(self.frequencys) > 0:
            return True
        return False
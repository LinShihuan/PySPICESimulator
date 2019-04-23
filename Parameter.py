class Parameter:
    def __init__(self, defVal):        
        self.__defaultValue = defVal
        self.__value = defVal
        self.__given = False
    def IsGiven(self):
        return self.__given
    def GetValue(self):
        return self.__value
    def GetDefaultValue(self):
        return self.__defaultValue
    def SetValue(self, val):
        if val == None or len(val) == 0:
            return False
        self.__value = val
        self.__given = True
        return True
    def SetDefaultValue(self, defVal):
        if defVal == None or len(defVal) == 0:
            return False
        self.__defaultValue = defVal
        return True
    def Reset(self):
        self.__value = self.__defaultValue
        self.__given = False
    def __eq__(self, val):
        if self.SetValue(val):
            return self
        return None
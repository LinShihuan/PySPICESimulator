from Util import ModelType
from ResistorModel import ResistorModelCore

modelType = ModelType()
def CreateModelCore(type, level):
        if type == None or len(type) == 0:
            return False, None
        if type == modelType.R:
            return ResistorModelCore()
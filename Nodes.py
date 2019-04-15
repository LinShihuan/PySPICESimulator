
class Nodes:
    __nodes = {}
    __index = 0
    def __init__(self):
        __nodes = {}
    
    def Size(self):
        return len(self.__nodes)

    def RemoveAll(self):
        self.__nodes = {}
    
    def AddNode(self, node):
        if node == None:
            return False
        node = node.upper()
        if self.__nodes.__contains__(node):
            return False
        self.__nodes[node] = self.__index
        self.__index += 1
        return True

    def GetIndex(self, node):
        if node == None:
            return -1 

        node = node.upper()
        if not self.__nodes.__contains__(node):
            return -1
        retIdx = self.__nodes[node]
        return retIdx

    def GetAllNodes(self):
        return self.__nodes                


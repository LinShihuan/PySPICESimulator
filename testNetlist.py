from Netlist import *
import numpy as numpy
from Util import *
from Circuit import *

state = Statement(1, "R1 1 2 100")
print(state.type)
print(StatementType.D, StatementType.M, StatementType.Model)

netlist = Netlist('.\\test\\rclTest.txt')
netlist.Preprocess()
statements = netlist.GetStatements()
for line in statements:
    print(line)

words = 'one two three wordA wordB wordC'
print(GetWord(words))

myCircuit = Circuit()
myCircuit.Params['paramA'] = 1
print(myCircuit.Params)

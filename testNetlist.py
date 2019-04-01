from Netlist import Netlist, Statement, StatementType
import numpy as numpy
import Util
from Circuit import Circuit

state = Statement(1, "R1 1 2 100")
print(state.type)
print(StatementType.D, StatementType.M, StatementType.Model)

netlist = Netlist('.\\test\\rclTest.txt')
netlist.Preprocess()
statements = netlist.GetStatements()
for line in statements:
    print(line)

netlist.ReadParameters()

print(netlist.GetCircuit().Params)

 

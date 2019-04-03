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
netlist.ReadGlobalModel()

print(netlist.GetCircuit().ModelCards[0].GetName(), netlist.GetCircuit().ModelCards[0].GetParams())

strTest = ' A=  2      B = \'1+2   * 3     \''
print(Util.RemoveSpace(strTest))

print(netlist.GetCircuit().Params)


 

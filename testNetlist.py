from Netlist import *
import numpy as numpy

state = Statement(1, "R1 1 2 100")
print(state.type)
print(StatementType.D, StatementType.M, StatementType.Model)

netlist = Netlist('F:\\Code\\Python\\PySpiceSimulator\\test\\rclTest.txt')
netlist.Preprocess()
statements = netlist.GetStatements()
for line in statements:
    print(line)
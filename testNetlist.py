from Netlist import Netlist, Statement, StatementType
import numpy as numpy
import Util
from Circuit import Circuit
from Nodes import Nodes 

state = Statement(1, "R1 1 2 100")
print(state.type)
print(StatementType.D, StatementType.M, StatementType.Model)

netlist = Netlist('.\\test\\rclTest.txt')
netlist.Preprocess()
'''Test statements
statements = netlist.GetStatements()
for line in statements:
    print(line)
'''

netlist.ReadParameters()
netlist.ReadGlobalModel()
netlist.ReadGlobalDevice()
netlist.ReadAnalyses()
netlist.GetCircuit().BuildDCMatrix()

'''test Device and Analyses
for devices in netlist.GetCircuit().Devices:
    print(devices)

for analyse in netlist.GetCircuit().Analyses:
    print(analyse)
'''

'''  Test model card reading
print(netlist.GetCircuit().ModelCards[0].GetName(), netlist.GetCircuit().ModelCards[0].GetParams())

strTest = ' A=  2      B = \'1+2   * 3     \''
print(Util.RemoveSpace(strTest))

print(netlist.GetCircuit().Params)
'''


'''Test expression evaluate
print(Util.ExpandExpression('1+2*3-4/5'))
print(Util.ExpandExpression('(1+2)*3-4/5'))
print(Util.ExpandExpression('-1+2*3-4/5'))
print(Util.ExpandExpression('1+2*3-(-4/5)'))
print(Util.ExpandExpression('+1+2*3-4/5'))
'''
'''Test Evaluate Value
print(Util.EvaluateValue('123.0*2+3'))
print(Util.EvaluateValue('1k+2*3/5'))
'''
'''Nodes test
dcNodes = Nodes()
dcNodes.AddNode('GND')
dcNodes.AddNode('node1')
dcNodes.AddNode('node2')
print(dcNodes.GetAllNodes())
print(dcNodes.GetIndex('node1'))
print(dcNodes.GetIndex('node2'))
print(dcNodes.GetIndex('node3'))
'''
import lib601.le as le
import lib601.util as util

# Python 2.6.6 on Win32

class Circuit:
    def __init__(self, components):
        self.components = components

    def solve(self, gnd):
        es = le.EquationSet()
        n2c = NodeToCurrents()
        
        for c in self.components:
            es.addEquation(c.getEquation())
            n2c.addCurrents(c.getCurrents())
        es.addEquations(n2c.getKCLEquations(gnd))

        print 'Solving equations'
        print '*****************'
        for e in es.equations: print e
        print '*****************'

        return es.solve()

class NodeToCurrents:
    def __init__(self):
        self.node_currents = {}

    def addCurrent(self, current, node, sign):
        if node not in self.node_currents:
            self.node_currents[node] = [[current, sign]]
        self.node_currents[node].append([current, sign])

    def addCurrents(self, currents):
        for current, node, sign in currents:
            self.addCurrent(current, node, sign)

    def getKCLEquations(self, gnd):
        equations = []
        equations.append(le.Equation([1],[gnd],0))
        for node, currents in self.node_currents.items():
            if node == gnd:
                continue
            coefficients = [sign for _, sign in currents]
            variables = [current for current, _ in currents]
            equations.append(le.Equation(coefficients, variables, 0.0))
        return equations

class Component:
    def getCurrents(self):
        return [[self.current, self.n1, +1], [self.current, self.n2, -1]]

class VSrc(Component):
    def __init__(self, v, n1, n2):
        self.current = util.gensym('i_'+n1+'->'+n2)
        self.n1 = n1
        self.n2 = n2
        self.v = v
        
    def getEquation(self):
        return le.Equation([1.0, -1.0], [self.n1, self.n2], self.v)

    def __str__(self):
        return 'VSrc('+str(self.v)+', '+self.n1+', '+self.n2+')'

class ISrc(Component):
    def __init__(self, i, n1, n2):
        self.current = util.gensym('i_'+n1+'->'+n2)
        self.n1 = n1
        self.n2 = n2
        self.i = i
        
    def getEquation(self):
        return le.Equation([1.0], [self.current], self.i)
    def __str__(self):
        return 'ISrc('+str(self.i)+', '+self.n1+', '+self.n2+')'

class Wire(Component):
    def __init__(self, n1, n2):
        self.current = util.gensym('i_'+n1+'->'+n2)
        self.n1 = n1
        self.n2 = n2

    def getEquation(self):
        return le.Equation([1.0, -1.0], [self.n1, self.n2], 0)
    def __str__(self):
        return 'Wire('+self.n1+', '+self.n2+')'

class Resistor(Component):
    def __init__(self, r, n1, n2):
        self.current = util.gensym('i_'+n1+'->'+n2)
        self.n1 = n1
        self.n2 = n2
        self.r = r

    def getEquation(self):
        return le.Equation([1.0, -1.0, -self.r], [self.n1, self.n2, self.current], 0.0)

class OpAmp(Component):

    def __init__(self, nPlus, nMinus, nOut, K=10000):
        self.K = K
        self.nPlus = nPlus
        self.nMinus = nMinus
        self.nOut = nOut
        self.current = util.gensym('i->'+nOut)

    def getCurrents(self):
        return [[self.current, self.nOut, +1]]

    def getEquation(self):
        return le.Equation([self.K, -self.K, -1.0], [self.nPlus, self.nMinus, self.nOut], 0.0)
        
# -----

div = Circuit([
    VSrc(10, '10v', 'gnd'),
    Resistor(1000, '10v', 'vo'),
    Resistor(1000, 'vo', 'gnd'),
    Resistor(10, 'vo', 'gnd')
    ])
print div.solve('gnd')

buf = Circuit([
    VSrc(10, '10v', 'gnd'),
    Resistor(1000, '10v', 'vo'),
    Resistor(1000, 'vo', 'gnd'),
    OpAmp('vo', 'v-', 'vb'),
    Wire('vb', 'v-'),
    Resistor(10, 'vb', 'gnd')
    ])
print buf.solve('gnd')
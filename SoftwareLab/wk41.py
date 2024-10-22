import pickle
import math
import lib601.util as util
import lib601.gw as gw

graphwidth = 570
graphheight = 300

class Signal:
    __w = None
    def plot(self, start = 0, end = 100, newWindow = 'Signal value versus time', color = 'blue', parent = None, ps = None, xminlabel = 0, xmaxlabel = 0, yOrigin = None):
        samples = [self.sample(i) for i in range(start, end)]
        if len(samples) == 0:
            raise Exception, 'Plot range is empty'
        if yOrigin == None:
            minY = min(samples)
        else:
            minY = yOrigin
        maxY = max(samples)
        if maxY == minY:
            margin = 1.0
        else:
#           margin = (maxY - minY) * 0.05
            margin = 0 # override bkph
        
        if newWindow == True or newWindow == False:
            title = 'Signal value vs time'
        else:
            title = newWindow
        if parent:
            # Make a window under a different tk parent
            w = gw.GraphingWindow(\
                     graphwidth, graphheight, start, end,
                     minY-margin, maxY+margin, title, parent,
                     xminlabel = xminlabel, xmaxlabel = xmaxlabel)
        else:
            # Use this class's tk instance
            if  newWindow or Signal.__w == None:
                Signal.__w = gw.GraphingWindow(\
                     graphwidth, graphheight, start, end,
                     minY-margin, maxY+margin, title,
                     xminlabel = xminlabel, xmaxlabel = xmaxlabel)
            w = Signal.__w
            
        w.graphDiscrete(lambda n: samples[n - start], color)
        if ps:
            w.postscript(ps)

    def __add__(self, other):
        return SummedSignal(self, other)
    
    def __rmul__(self, scalar):
        return ScaledSignal(self, scalar)

    def __mul__(self, scalar):
        return ScaledSignal(self, scalar)

    def period(self, n = None, z = None):
        if n == None:
            n = self.length
        crossingsD = self.crossings(n, z)
        if len(crossingsD) < 2:
            return 'aperiodic'
        else:
            return listMean(gaps(crossingsD))*2

    def crossings(self, n = None, z = None):
        if n == None: n = self.length
        if z == None: z = self.mean(n)
        samples = self.samplesInRange(0, n)
        return [i for i in range(n-1) if \
                   samples[i] > z and samples[i+1] < z or\
                   samples[i] < z and samples[i+1] > z]

    def mean(self, n = None):
        if n == None: n = self.length
        return listMean(self.samplesInRange(0, n))

    def samplesInRange(self, lo, hi):
        return [self.sample(i) for i in range(lo, hi)]    
    

class CosineSignal(Signal):
    def __init__(self, omega = 1, phase = 0):
        self.omega = omega
        self.phase = phase
    def sample(self, n):
        return math.cos(self.omega * n + self.phase)
    def __str__(self):
        return 'CosineSignal(omega=%f,phase=%f)'%(self.omega, self.phase)

class UnitSampleSignal(Signal):
    def sample(self, n):
        if n == 0:
            return 1
        else:
            return 0
    def __str__(self):
        return 'UnitSampleSignal'

us = UnitSampleSignal()

class ConstantSignal(Signal):
    def __init__(self, c):
        self.c = c
    def sample(self, n):
        return self.c
    def __str__(self):
        return 'ConstantSignal(%f)'%(self.c)

class StepSignal(Signal):
    """
    StepSignal has value 0 at any time index less than 0 and value 1 otherwise.
    """
    def sample(self, n):
        return 0 if n < 0 else 1

    def __str__(self):
        return 'StepSignal'

class SummedSignal(Signal):
    """
    SummedSignal takes two signals, s1 and s2, and creates a new signal that is the sum of those signals.
    """
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

    def sample(self, n):
        return self.s1.sample(n) + self.s2.sample(n)

    def __str__(self):
        return 'SummedSignal(%s, %s)' % (str(self.s1), str(self.s2))

class ScaledSignal(Signal):
    """
    ScaledSignal scales a signal by a constant c.
    """
    def __init__(self, signal, scalar):
        self.signal = signal
        self.scalar = scalar

    def sample(self, n):
        return self.scalar * self.signal.sample(n)

    def __str__(self):
        return 'ScaledSignal(%s, %f)' % (str(self.signal), self.scalar)

class R(Signal):
    """
    R delays a signal by one time step.
    """
    def __init__(self, signal):
        self.signal = signal

    def sample(self, n):
        return self.signal.sample(n - 1)

    def __str__(self):
        return 'R(%s)' % str(self.signal)

class Rn(Signal):
    """
    Rn delays a signal by n time steps.
    """
    def __init__(self, signal, delay_steps):
        self.signal = signal
        self.delay_steps = delay_steps

    def sample(self, n):
        return self.signal.sample(n - self.delay_steps)

    def __str__(self):
        return 'Rn(%s, %d)' % (str(self.signal), self.delay_steps)
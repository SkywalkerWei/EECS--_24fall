import random
import operator
import copy
import lib601.util as util

print("-----Test outputs in Wk10.1.1~10.1.7-----\n")

def removeElt(items, i):
    return items[:i] + items[i+1:] if len(items) != 2 else items[1-i]

class DDist:
	def __init__(self, dictionary):
		self.d = dictionary
	def dictCopy(self):
		return self.d.copy()
	def prob(self, elt):
		if self.d.has_key(elt):
			return self.d[elt]
		else:
			return 0
	
	def marginalizeOut(self, index):
		newDict, newStates, oldStates = {}, [], []
		for state in self.d.keys():
			newStates += [s for s in [removeElt(state, 0)] if s not in newStates]
			oldStates += [s for s in [removeElt(state, 1)] if s not in oldStates]
		if index == 1:
			oldStates, newStates = newStates, oldStates
		for state in newStates:
			newDict[state] = sum(self.prob((oldState, state)) for oldState in oldStates)
		return DDist(newDict)
	
	def conditionOnVar(self, index, value):
		outDict, nonNormalizedDict = {}, {}
		for state in self.d.keys():
			if removeElt(state,abs(index-1)) == value:
				nonNormalizedDict[state] = self.d[state]
		normalizationCoefficient = sum(nonNormalizedDict.values())
		for state in nonNormalizedDict:
			outDict[state[abs(index-1)]] = nonNormalizedDict[state]/normalizationCoefficient
		return DDist(outDict)

	def support(self):
		return [k for k in self.d.keys() if self.prob(k) > 0]
	def __repr__(self):
		if len(self.d.items()) == 0:
			return "Empty DDist"
		else:
			dictRepr = reduce(operator.add, [util.prettyString(k)+": "+ util.prettyString(p)+", " for (k,p) in self.d.items()])
		return "DDist(" + dictRepr[:-2] + ")"
	__str__ = __repr__

# 10.1.1

foo = DDist({'hi':0.6,'med':0.1,'lo':0.3})
print("10.1.1\n")
print(foo)
print("-----\n")

# 10.1.2

def PTgD(diseaseValue):
	if diseaseValue == 'disease':
		return DDist({'posTest':0.98,'negTest':0.02})
	elif diseaseValue == "noDisease":
		return DDist({'posTest':0.05,'negTest':0.95})
	else:
		raise Exception, 'invalid value for D'
	
print("10.1.2\n")
print("For example: PTgD('disease').prob('posTest') should evaluate to 0.98.")
print(PTgD('disease').prob('posTest'))
print("-----\n")

# 10.1.3

Disease = DDist({'disease':0.0001,'noDisease':0.9999})

joint = DDist({('noDisease','posTest'):Disease.prob('noDisease')*PTgD('noDisease').prob('posTest'), ('disease','posTest'):Disease.prob('disease')*PTgD('disease').prob('posTest'), ('noDisease','negTest'):Disease.prob('noDisease')*PTgD('noDisease').prob('negTest'), ('disease','negTest'):Disease.prob('disease')*PTgD('disease').prob('negTest')})

print("10.1.3.1\n")
print(joint)
print("-----\n")

jointMarg = DDist({'posTest':joint.prob(('noDisease','posTest'))+joint.prob(('disease','posTest')), 'negTest':joint.prob(('noDisease','negTest'))+joint.prob(('disease','negTest'))})

print("10.1.3.2\n")
print(jointMarg)
print("-----\n")

# 10.1.4

bUpdate = DDist({'disease':1-joint.prob(('noDisease','posTest'))*Disease.prob('noDisease')/PTgD('noDisease').prob('posTest'), 'noDisease':joint.prob(('noDisease','posTest'))*Disease.prob('noDisease')/PTgD('noDisease').prob('posTest')})

print("10.1.4.1\n What is the result of conditionalizing the joint distribution P(Disease, Test) from the previous problem on Test = 'posTest'? \n")
print(bUpdate)
print("-----\n")

totProb = DDist({'posTest':Disease.prob('disease')*PTgD('disease').prob('posTest')+Disease.prob('noDisease')*PTgD('noDisease').prob('posTest'), 'negTest':Disease.prob('disease')*PTgD('disease').prob('negTest')+Disease.prob('noDisease')*PTgD('noDisease').prob('negTest')})

print("10.1.4.2\n What is the result of applying the law of total probability to get P(Test) given P(Test | Disease) and P(Disease) as given before.\n")
print(totProb)
print("-----\n")

# 10.1.5

floor = DDist({'f1':0.5,'f2':0.5})

print("10.1.5.1\n What is the DDist for P(floor)? \n")
print(floor)
print("-----\n")

def RgF(floorValue):
	if floorValue == 'f1':
		return DDist({'r1':0.25,'r2':0.25,'r3':0.25,'r4':0.25})
	elif floorValue == 'f2':
		return DDist({'r1':0.1,'r2':0.1,'r3':0.1,'r4':0.7})
	else:
		raise Exception, 'invalid floor value'
	
print("10.1.5.2\nWhat is the DDist for P(room | floor='f1')?\n")
print(RgF('f1'))
print("-----\n")

print("10.1.5.3\nWhat is the DDist for P(room | floor='f2')?\n")
print(RgF('f2'))
print("-----\n")

jointRoomFloor = DDist({'(f1,r1)':floor.prob('f1')*RgF('f1').prob('r1'), '(f1,r2)':floor.prob('f1')*RgF('f1').prob('r2'), '(f1,r3)':floor.prob('f1')*RgF('f1').prob('r3'), '(f1,r4)':floor.prob('f1')*RgF('f1').prob('r4'), '(f2,r1)':floor.prob('f2')*RgF('f2').prob('r1'), '(f2,r2)':floor.prob('f2')*RgF('f2').prob('r2'), '(f2,r3)':floor.prob('f2')*RgF('f2').prob('r3'), '(f2,r4)':floor.prob('f2')*RgF('f2').prob('r4')})

print("10.1.5.4\nWhat is the Joint Distribution over (room, floor)?\n")
print(jointRoomFloor)
print("-----\n")

FloorRoom1 = DDist({'f1':RgF('f1').prob('r1')*floor.prob('f1')/(0.35/2.), 'f2':RgF('f2').prob('r1')*floor.prob('f2')/(0.35/2.)})

print("10.1.5.5\nNow, we find out for sure that he's in room 1. What is the DDist for P(floor | room = 'r1')? \n")
print(FloorRoom1)
print("-----\n")

# 10.1.6

def PTgD(val):
    return DDist({'posTest': 0.9, 'negTest': 0.1} if val == 'disease' else {'posTest': 0.5, 'negTest': 0.5})

disease = DDist({'disease':0.1,'noDisease':0.9})

def JDist(PA, PBgA):
	dict = {}
	aCopy = PA.dictCopy()
	for state in aCopy.keys():
		jointDict = PBgA(state).dictCopy()
		for result in jointDict.keys():
			dict[(state,result)] = PA.prob(state)*PBgA(state).prob(result)
	return DDist(dict)

print("10.1.6.1\n")
print(JDist(disease, PTgD))
print("-----\n")

print("10.1.6.2\n")
print(JDist(disease,PTgD).marginalizeOut(0))
print("-----\n")

print("10.1.6.3\n")
print(JDist(disease,PTgD).conditionOnVar(1,'posTest'))
print("-----\n")

# 10.7.1

def bayesEvidence(PBgA, PA, b):
	return JDist(PA,PBgA).conditionOnVar(1,b)

print("10.1.7.1\n")
print(bayesEvidence(PTgD,disease,'posTest'))
print(bayesEvidence(PTgD,disease,'negTest'))
print("-----\n")

def totalProbability(PBgA, PA):
	return JDist(PA,PBgA).marginalizeOut(0)

print("10.1.7.2\n")
print(totalProbability(PTgD,disease))
print("-----\n")

print("-----TestSL10.txt-----\n")

def _PTgD(val):
    if val == 'disease':
        return DDist({'posTest':0.9, 'negTest':0.1})
    else:
        return DDist({'posTest':0.5, 'negTest':0.5})
	
PD = DDist({'disease':0.1, 'noDisease':0.9})

def _PRgF(val):
    if val == 'f1':
        return DDist({'r1':0.25, 'r2':0.25, 'r3':0.25, 'r4':0.25})
    else:
        return DDist({'r1':0.1, 'r2':0.1, 'r3':0.1, 'r4':0.7})
	
PF = DDist({'f1':0.5, 'f2':0.5})

print('-------WK10.1.7  Part1-------')
print(bayesEvidence(_PTgD, PD, 'posTest'))
print(bayesEvidence(_PTgD, PD, 'negTest'))
print(bayesEvidence(_PRgF, PF, 'r3'))
print(bayesEvidence(_PRgF, PF, 'r4'))

print('-------WK10.1.7  Part2-------')
print(totalProbability(_PTgD, PD))
print(totalProbability(_PRgF, PF))

#####

def incrDictEntry(d, k, v):
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v
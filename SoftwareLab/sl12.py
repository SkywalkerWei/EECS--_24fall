import lib601.dist as dist
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.util as util

### python 2.6.6

class StateEstimator(sm.SM):
    def __init__(self, model):
        self.model = model
        self.startState = model.startDistribution

    def getNextValues(self, state, inp):
        belief = self.efficientBayes(state, inp[0])
        dSPrime = self.totalProbability(belief, self.model.transitionDistribution(inp[1]))
        return (dSPrime, dSPrime)

    def efficientBayes(self,state,observation):
        state_name, p, dist_dict = state.support(), 0, {}
        for name in state_name:
            prob = self.model.observationDistribution(name).prob(observation) * state.prob(name)
            dist.incrDictEntry(dist_dict, name, prob)
            p += prob
        for i in dist_dict.keys():
            dist_dict[i] /= p
        return dist.DDist(dist_dict)
    
    def totalProbability(self, belief, transDist):
        states, total = belief.support(), {}
        for s1 in states:
            for s2 in states:
                total[s2] = total.get(s2, 0) + belief.prob(s1) * transDist(s1).prob(s2)
        for k, v in total.items():
            total[k] = v / sum(total.values())
        return dist.DDist(total)

### default test sample in swLab12.pdf

transitionTable = {'good': dist.DDist({'good' : 0.7, 'bad' : 0.3}), 'bad' : dist.DDist({'good' : 0.1, 'bad' : 0.9})}
observationTable = {'good': dist.DDist({'perfect' : 0.8, 'smudged' : 0.1, 'black' : 0.1}), 'bad': dist.DDist({'perfect' : 0.1, 'smudged' : 0.7, 'black' : 0.2})}
copyMachine = ssm.StochasticSM(dist.DDist({'good' : 0.9, 'bad' : 0.1}), lambda i: lambda s: transitionTable[s], lambda s: observationTable[s])
obs = [('perfect', 'step'), ('smudged', 'step'), ('perfect', 'step')]
cmse = StateEstimator(copyMachine)
print cmse.transduce(obs)
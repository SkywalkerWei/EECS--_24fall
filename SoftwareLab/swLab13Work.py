import lib601.search as search
import lib601.sm as sm

(farmer, goat, wolf, cabbage) = range(4)

class FarmerGoatWolfCabbage(sm.SM):
   startState = ('L','L','L','L')
   legalInputs = ['takeGoat','takeNone','takeWolf','takeCabbage']
   def __init__(self):
       self.state = self.startState
   def getNextValues(self, state, action):
       safe = {'takeNone': lambda s: s[1] != s[3] and s[1] != s[2], 'takeGoat': lambda s: s[0] == s[1], 'takeWolf': lambda s: s[0] == s[2] and s[1] != s[3], 'takeCabbage': lambda s: s[0] == s[3] and s[1] != s[2]}
       move = {'takeNone': 0, 'takeGoat': 1, 'takeWolf': 2, 'takeCabbage': 3}
       if action in safe and safe[action](state):
            state = _next(state, 0, move[action])
       return (state,state)
   def done(self, state):
       return state == ('R','R','R','R')
def _next(state, Farmer, item):
      state = list(state)
      if item:
         state[item] = 'R' if state[item] == 'L' else 'L'
      state[Farmer] = 'R' if state[Farmer] == 'L' else 'L'
      return tuple(state)

print search.smSearch(FarmerGoatWolfCabbage(),depthFirst=False, DP=True)
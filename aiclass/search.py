from aiclass.parser import parse_graph


class Problem(object):


    def actions(self, state):
        raise NotImplementedError


    def result(self, action):
        raise NotImplementedError


    def cost(self, action):
        raise NotImplementedError


    def get_initial(self):
        raise NotImplementedError


    def goal_test(self, state):
        raise NotImplementedError


    def heuristic(self, state):
        raise NotImplementedError



class Searcher(object):


    def __init__(self, problem, depth_limit=None):
        self.problem = problem
        self._frontier = []
        self.depth_limit = depth_limit
        self.goal_reached = None
        self.expand_count = 0

        self.path_to = {self.problem.get_initial(): (None, None)}
        self.add_to_frontier(self.problem.get_initial(), 0)


    def add_to_frontier(self, state, depth):
        if self.depth_limit is None or depth < self.depth_limit:
            self._frontier.append((state, depth))


    def get_next_from_frontier(self):
        raise NotImplementedError


    def is_visited(self, state):
        return state in self.path_to
        
    
    def get_visited(self):
        return self.path_to.keys()
        
    
    def get_explored(self):
        return [ s for s in self.path_to.keys() if s not in self._frontier ]


    def log_path(self, from_state, action, to_state):
        self.path_to[to_state] = from_state, action


    def path_cost(self, to_state):
        from_state, action = self.path_to[to_state]
        if from_state is None:
            return 0
        return self.path_cost(from_state) + self.problem.cost(action)


    def expand(self):
        state, depth = self.get_next_from_frontier()
        self.expand_count += 1

        if self.problem.goal_test(state):
            self.goal_reached = state
        else:
            for action in self.problem.actions(state):
                next_state = self.problem.result(action)
            
                if self.is_visited(next_state):
                    if self.path_cost(state) + self.problem.cost(action) < self.path_cost(next_state):
                        self.log_path(state, action, next_state)
                else:
                    self.add_to_frontier(next_state, depth+1)
                    self.log_path(state, action, next_state)

        return state


    def search(self):
        while self.goal_reached is None:
            if not self._frontier:
                return False
            self.expand()
        return self.goal_reached


    def get_solution_state_path(self):
        path = []
        state = self.goal_reached
        while state is not None:
            path = [state] + path
            state, action = self.path_to[state]

        return path


    def get_solution_action_path(self):
        path = []
        state = self.goal_reached
        while state is not None:
            state, action = self.path_to[state]
            path = [action] + path

        return path


class DfsSearcher(Searcher):


    def get_next_from_frontier(self):
        item = max(self._frontier, key=lambda i: i[1])
        self._frontier.remove(item)
        return item



class BfsSearcher(Searcher):


    def get_next_from_frontier(self):
        return self._frontier.pop(0)



class CfsSearcher(Searcher):


    def get_next_from_frontier(self):
        item = min(self._frontier, key=lambda i: self.path_cost(i[0]))
        self._frontier.remove(item)
        return item


class AstarSearcher(Searcher):


    def get_next_from_frontier(self):
        item = min(self._frontier, key=lambda i: self.path_cost(i[0]) + self.problem.heuristic(i[0]))
        self._frontier.remove(item)
        return item



class MapRoutingProblem(Problem):

    def __init__(self, initial, goal, path, heuristic):
        self.initial = initial
        self.goal = goal
        self.edges = self.parse_path(path)
        self.h = self.parse_heuristic(heuristic)


    def parse_path(self, data):
        edges = []
        for line in data.splitlines():
            line = line.strip()
            if line != '':
                ab, c = line.split(':', 1)
                a, b = ab.split('->', 1)
                edges.append((a.strip(),b.strip(),int(c.strip())))
        return edges


    def parse_heuristic(self, data):
        h = {}
        for line in data.splitlines():
            line = line.strip()
            if line != '':
                a, b = line.split(':', 1)
                h[a.strip()] = int(b.strip())
        return h


    def actions(self, state):
        return [ (b,c) for a,b,c in self.edges if a == state ] + [ (a,c) for a,b,c in self.edges if b == state ]


    def result(self, action):
        return action[0]

        
    def cost(self, action):
        return action[1]


    def get_initial(self):
        return self.initial


    def goal_test(self, state):
        return state == self.goal


    def heuristic(self, state):
        return self.h[state]



ROMANIA_MAP_DATA = '''
Arad -> Zerind: 75
Arad -> Timisoara: 118
Arad -> Sibiu: 140
Zerind -> Oradea: 71
Oradea -> Sibiu: 151
Timisoara -> Lugoj: 111
Lugoj -> Mehadia: 70
Mehadia -> Drobeta: 75
Drobeta -> Craiova: 120
Craiova -> Rimnicu Vilcea: 146
Craiova -> Pitesti: 138
Rimnicu Vilcea -> Sibiu: 80
Rimnicu Vilcea -> Pitesti: 97
Pitesti -> Bucharest: 101
Sibiu -> Fagaras: 99
Fagaras -> Bucharest: 211
'''



DISTANCE_TO_BUCHAREST = '''
Arad: 366
Zerind: 374
Oradea: 380
Sibiu: 253
Timisoara: 329
Lugoj: 244
Mehadia: 241
Drobeta: 242
Craiova: 160
Fagaras: 176
Rimnicu Vilcea: 193
Pitesti: 100
Bucharest: 0
'''



class RomaniaProblem(MapRoutingProblem):

    def __init__(self):
        MapRoutingProblem.__init__(
            self,
            'Arad',
            'Bucharest',
            ROMANIA_MAP_DATA,
            DISTANCE_TO_BUCHAREST)



class NodeCountProblem(Problem):


    def __init__(self, initial, goal, data):
        self.initial = initial
        self.goal = goal
        self.edges = parse_graph(data)


    def actions(self, state):
        return [ b for a,b in self.edges if a == state ]


    def result(self, action):
        return action


    def cost(self, action):
        return 0


    def get_initial(self):
        return self.initial


    def goal_test(self, state):
        return state == self.goal


        
class AstarSearchProblem(Problem):


    def __init__(self):
        self.h = {}
        for y in ['a','b','c','d']:
            for x in [1,2,3,4,5,6]:
                self.h['%s%d'%(y,x)] = min([ord('d')-ord(y)+1, 6-x+1])
        self.h['d6'] = 0


    def actions(self, state):
        y, x = state
        actions = []
        if y != 'a':
            actions.append('%s%s'%(chr(ord(y)-1), x))
        if y != 'd':
            actions.append('%s%s'%(chr(ord(y)+1), x))
        if x != '1':
            actions.append('%s%s'%(y, chr(ord(x)-1)))
        if x != '6':
            actions.append('%s%s'%(y, chr(ord(x)+1)))
        return actions


    def result(self, action):
        return action


    def cost(self, action):
        return 1


    def get_initial(self):
        return 'a1'


    def goal_test(self, state):
        return state == 'd6'


    def heuristic(self, state):
        return self.h[state]
        


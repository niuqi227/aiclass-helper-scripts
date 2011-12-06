from aiclass.command import BaseCommand
from aiclass.parser import SimpleParser, parse_graph
from aiclass.search import Problem, BfsSearcher

import itertools


class StatementParser(SimpleParser):
    t_INDEPENDENT = r'\_\|\_'
    t_VARIABLE = r'[A-Za-z]+'
    t_ignore = ' '
    literals = ['|', ',']
    
    def p_independence(self, p):
        """statement : VARIABLE INDEPENDENT VARIABLE"""
        p[0] = p[1], p[3], []
    
    def p_conditional_independence(self, p):
        """statement : VARIABLE INDEPENDENT VARIABLE '|' conditions"""
        p[0] = p[1], p[3], p[5]
    
    def p_conditions(self, p):
        """conditions : conditions ',' conditions"""
        p[0] = p[1] + p[3]
    
    def p_condition(self, p):
        """conditions : VARIABLE"""
        p[0] = [p[1]]


class PathFinding(Problem):

    def __init__(self, initial, goal, edges, skip=[], revert=False):
        self.initial = initial
        self.goal = goal
        self.edges = edges
        self.skip = skip
        self.revert = revert

    def actions(self, state):
        if self.revert:
            return [ a for a,b in self.edges if b == state and a not in self.skip and b not in self.skip ]        
        else:
            return [ b for a,b in self.edges if a == state and a not in self.skip and b not in self.skip ]

    def result(self, action):
        return action

    def cost(self, action):
        return 0

    def get_initial(self):
        return self.initial

    def goal_test(self, state):
        return state == self.goal


class BayesNetwork(object):

    def __init__(self, data):
        self.parser = StatementParser()
        self.edges = parse_graph(data)

    def parameters(self):
        vertices = set(itertools.chain(*self.edges))
        return sum(2 ** len([ a for a,b in self.edges if b == v ]) for v in vertices) 

    def validate(self, statement):
        statement = self.parser.parse(statement)
        return self._validate(*statement)

    def _validate(self, a, b, conditions):        
        if any(BfsSearcher(
                PathFinding(a,c,self.edges)
            ).search() and BfsSearcher(
                PathFinding(b,c,self.edges)).search() 
            for c in conditions):
            return False

        a2b = BfsSearcher(PathFinding(a,b, self.edges, conditions, revert=True))
        b2a = BfsSearcher(PathFinding(b,a, self.edges, conditions, revert=True))
        
        if a2b.search() or b2a.search():
            return False
        
        a2bv = a2b.get_visited()
        b2av = b2a.get_visited()

        return not any(a for a in a2bv if a in b2av)




class NetworkCommand(BaseCommand):
    name = 'network'
    description ='bayes network'
    help ='bayes network'


    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('data', help='data of network')


    @classmethod
    def create_from_args(cls, args):
        return cls(cls.get_data(args.data))


    def __init__(self, data):
        self.bayes_network = BayesNetwork(data)


    def call(self, string):
        if string == r'\q':
            return True
        elif string == 'params':
            print(self.bayes_network.parameters())
        else:
            print(self.bayes_network.validate(string))



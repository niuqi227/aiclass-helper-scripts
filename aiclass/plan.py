from aiclass.parser import SimpleParser


class Atom(object):
    def __init__(self, name):
        self.name = name

class Variable(object):
    def __init__(self, name):
        self.name = name

class Effect(object):
    def __init__(self, procedure, parameters, retract=False):
        self.procedure = procedure
        self.parameters = parameters

class Query(object):
    def __init__(self, procedure, parameters):
        self.procedure = procedure
        self.parameters = parameters

class Action(object):
    def __init__(self, name, parameters, preconditions, effects):
        self.name = name
        self.parameters = parameters
        self.preconditions = preconditions
        self.effects = effects

class Execute(object):
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

class Queries(object):
    def __init__(self, queries):
        self.queries = queries


class ClassicPlanParser(SimpleParser):
    t_ATOM = r'[a-z]+'
    t_VARIABLE = r'[A-Z][A-Za-z]*'
    t_ignore = ' \n'
    literals = ['.', ',', '~', '(', ')', '[', ']', '{', '}', ':' ]

    def p_inputs(self, p):
        """input : input input"""
        p[0] = p[1] + p[2]
    
    def p_input(self, p):
        """input : execute
                 | action
                 | user_query"""
        p[0] = [p[1]]
    
    def p_user_query(self, p):
        """user_query : query_list '.'"""
        p[0] = Queries(p[1])

    def p_execute(self, p):
        """execute : ATOM '(' atoms ')' '.' """
        p[0] = Execute(p[1], p[3])

    def p_execute_no_args(self, p):
        """execute : ATOM '.' """
        p[0] = Execute(p[1], [])

    def p_action(self, p):
        """action : ATOM '(' variable_list ')'  '[' query_list ']' '{' effect_list '}' '.'"""
        p[0] = Action(p[1], p[3], Queries(p[6]), p[9])

    def p_list(self, p):
        """variable_list : variables
                         | empty
           effect_list   : empty
                         | effects
           query_list    : empty
                         | queries"""
        p[0] = p[1]
    
    def p_comma(self, p):
        """atoms      : atoms      ',' atoms
           variables  : variables  ',' variables
           queries    : queries    ',' queries
           effects    : effects    ',' effects
           parameters : parameters ',' parameters"""
        p[0] = p[1] + p[3]

    def p_query(self, p):
        """queries : VARIABLE '(' parameters ')'"""
        p[0] = [Query(p[1], p[3])]

    def p_retract(self, p):
        """effects : '~' VARIABLE '(' parameters ')'"""
        p[0] = [Effect(p[1], p[3], retract=True)]

    def p_assert(self, p):
        """effects : VARIABLE '(' parameters ')'"""
        p[0] = [Effect(p[1], p[3])]

    def p_variable(self, p):
        """variables  : VARIABLE
           parameters : VARIABLE"""
        p[0] = [Variable(p[1])]

    def p_atom(self, p):
        """parameters : ATOM
           atoms      : ATOM"""
        p[0] = [Atom(p[1])]

    def p_empty(self, p):
        """empty : """
        p[0] = []



class Interpreter(object):
    pass






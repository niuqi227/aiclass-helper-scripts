from aiclass.parser import SimpleParser

import itertools

class Atom(str):
    pass

class Variable(str):
    pass

class Effect(list):
    def __init__(self, pred, params, retract=False):
        super(Effect, self).__init__(params)
        self.pred = pred
        self.retract = retract
    
    def bind(self, ctx):
        return Effect(self.pred, [ctx.get(param, param) for param in self], self.retract)

class Action(object):
    def __init__(self, name, params, preconditions, effects):
        self.name = name
        self.params = params
        self.preconditions = preconditions
        self.effects = effects

class Execute(list):
    def __init__(self, name, params):
        super(Execute, self).__init__(params)
        self.name = name

class Query(list):
    def __init__(self, pred, params):
        super(Query, self).__init__(params)
        self.pred = pred
    
    def bind(self, ctx):
        return Query(self.pred, [ctx.get(param, param) for param in self])

class QueryList(list):
    
    def bind(self, ctx):
        return QueryList(q.bind(ctx) for q in self)


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
        p[0] = QueryList(p[1])

    def p_execute(self, p):
        """execute : ATOM '(' atoms ')' '.'"""
        p[0] = Execute(p[1], p[3])

    def p_execute_no_args(self, p):
        """execute : ATOM '.'"""
        p[0] = Execute(p[1], [])

    def p_action(self, p):
        """action : ATOM '(' variable_list ')'  '[' query_list ']' '{' effect_list '}' '.'"""
        p[0] = Action(p[1], p[3], QueryList(p[6]), p[9])

    def p_list(self, p):
        """variable_list : empty
                         | variables
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
        p[0] = [Effect(p[2], p[4], retract=True)]

    def p_assert(self, p):
        """effects : VARIABLE '(' parameters ')'"""
        p[0] = [Effect(p[1], p[3], retract=False)]

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



class Predicates(list):
    def __init__(self, length, data=None):
        if data:
            super(Predicates, self).__init__(data)
        self.length = length


class ClassicPlanDatabase(object):
    
    def __init__(self):
        self.parser = ClassicPlanParser()
        self.actions = {}
        self.predicates = {}

    def get_predicates(self, query):
        predicates = self.predicates[query.pred]
        assert predicates.length == len(query)
        return predicates
        
    def _merge(self, results):
        if not all(results):
            return False
            
        tuples = [ r for r in results if r is not True ]
        
        if not any(tuples):
            return True
        
        results = dict(tuples).items()
        if not all(t in results for t in tuples):
            return False
            
        return results

    def _query(self, query):
        predicates = self.get_predicates(query)
        
        results = [
            self._merge(
                [ q==p if isinstance(q, Atom) else (q,p)
                  for q, p in zip(query, pred)])
                  for pred in predicates ]

        if all(isinstance(q, Atom) for q in query):
            return any(results)
        else:
            return [ result for result in results if result is not False ] or False
    
    def merge(self, results):
        if not all(results):
            return False
        
        lists = [r for r in results if r is not True]
        if not any(lists):
            return True
        
        results = [ self._merge(sum(choice, [])) for choice in itertools.product(*lists) ]
        return [ result for result in results if result is not False ] or False

    def query(self, statement):
        return self.merge([ self._query(q) for q in statement ])


    def execute(self, statement):
        action = self.actions[statement.name]
        ctx = dict(zip(action.params, statement))
        query = action.preconditions.bind(ctx)
        results = self.query(query)
        if results is False:
            return False
        
        # TODO bind results
        effects = [ e.bind(ctx) for e in action.effects ]           
        for effect in effects:
            if effect.retract:
                pred = self.get_predicates(effect)
                if list(effect) not in pred:
                    raise Exception
                pred.remove(list(effect))
                self.predicates[effect.pred] = pred
            else:
                pred = self.predicates.get(
                    effect.pred,
                    Predicates(len(effect)))
                pred.append(list(effect))
                self.predicates[effect.pred] = pred
        
        return True 



    def add_action(self, statement):
        if statement.name in self.actions:
            raise Exception
        self.actions[statement.name] = statement
        
        return True
    
    
    def _eval(self, statement):
        if isinstance(statement, Action):
            return self.add_action(statement)
        elif isinstance(statement, Execute):
            return self.execute(statement)
        elif isinstance(statement, QueryList):
            return self.query(statement)
        else:
            raise Exception

    def eval(self, statements):
        statements = self.parser.parse(statements)
        assert len(statements) == 1
        return self._eval(statements[0])
    
    def evaluate(self, statements):
        statements = self.parser.parse(statements)
        for s in statements:
            self._eval(s)    





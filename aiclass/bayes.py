from aiclass.parser import SimpleParser, parse_graph
import itertools, fractions, collections


class MaterialParser(SimpleParser):
    t_COLON = r'\:'
    t_COMMA = r'\,'
    t_DOT = r'\.'
    t_WORD = r'[A-Za-z]+'
    t_BLANK = r'\ +'
    t_ignore = '\n'

    def p_material_top(self, p):
        '''categories : categories category'''
        p[0] = Material(p[1] + [p[2]])

    def p_material_categories(self, p):
        '''categories : category'''
        p[0] = [p[1]]
    
    def p_material_category(self, p):
        '''category : WORD COLON phrases DOT'''
        p[0] = p[1], p[3]

    def p_material_phrases(self, p):
        '''phrases : phrases COMMA phrase'''
        p[0] = p[1] + [p[3]]

    def p_material_phrase(self, p):
        '''phrases : phrase'''
        p[0] = [p[1]]

    def p_material_words(self, p):
        '''phrase : phrase BLANK WORD'''
        p[0] = p[1] + [p[3]]

    def p_material_word(self, p):
        '''phrase : WORD'''
        p[0] = [p[1]]



class ExpressionParser(SimpleParser):
    t_QUOTE = r'\"'
    t_WORD = r'[A-Za-z]+'
    t_BLANK = r'\ +'
    t_VERTICAL = r'\|'
    
    def p_expression_probability(self, p):
        '''expression : event'''
        p[0] = p[1]
    
    def p_expression_conditional(self, p):
        '''expression : event VERTICAL event'''
        p[0] = p[1], p[3]

    def p_expression_events(self, p):
        '''event : QUOTE phrase QUOTE'''
        p[0] = p[2]
    
    def p_expression_event(self, p):
        '''event : WORD'''
        p[0] = p[1]

    def p_expression_words(self, p):
        '''phrase : phrase BLANK WORD'''
        p[0] = p[1] + [p[3]]
    
    def p_expression_word(self, p):
        '''phrase : WORD'''
        p[0] = [p[1]]



class Material(object):

    def __init__(self, raw):
        self.parser = ExpressionParser()
    
        self.categories = [k for k,v in raw]
        self._p = {}
        self.phrases = sum( len(v) for k,v in raw )
        self.vocabulary = set(itertools.chain(*[ itertools.chain(*v) for k,v in raw]))
        
        for category, phrases in raw:
            self._p[category] = len(phrases), self.phrases

            total = sum(map(len, phrases))
            count = collections.defaultdict(lambda: 0)
            for word in itertools.chain(*phrases):
                count[word] += 1

            for k in self.vocabulary:
                self._p[(k,category)] = count.get(k, 0), total
     
    def size_of_vocabulary(self):
        return len(self.vocabulary)

    def is_conditional(self, expression):
        return isinstance(expression, tuple)

    def is_category(self, expression):
        return isinstance(expression, str)
    
    def is_phrase(self, expression):
        return isinstance(expression, list)
    
    def p(self, expression, laplace):
        n, d = self._p[expression]
        if self.is_category(expression):
            return fractions.Fraction(n+laplace, d+laplace*len(self.categories))
        else:
            return fractions.Fraction(n+laplace, d+laplace*len(self.vocabulary))
        
    def P(self, expression, laplace):
        if self.is_category(expression):
            return self.p(expression, laplace)
        elif self.is_conditional(expression):
            a, b = expression
            if self.is_phrase(a) and self.is_category(b):
                return reduce(lambda a,b: a*b, [ self.p((w,b), laplace) for w in a ])
            elif self.is_category(a) and self.is_phrase(b):
                return fractions.Fraction(
                    self.P((b,a), laplace) * self.P(a, laplace),
                    sum(self.P((b,k), laplace) * self.P(k, laplace) for k in self.categories) )

        raise NotImplementedError
   
   
    def query(self, expression, laplace=0):
        return self.P(self.parser.parse(expression), laplace)



def parameters(data):
    edges = parse_graph(data)
    vertices = set(itertools.chain(*edges))
    return sum(2 ** len([ a for a,b in edges if b == v ]) for v in vertices) 





from aiclass.command import BaseCommand
from aiclass.parser import SimpleParser, parse_graph
import itertools, fractions, collections, functools


class MaterialParser(SimpleParser):
    t_WORD = r'[A-Za-z]+'
    t_BLANK = r'\ +'
    t_ignore = '\n'
    literals = [':', ',', '.']

    def p_material_top(self, p):
        """categories : categories categories"""
        p[0] = Material(p[1] + p[2])

    def p_material_categories(self, p):
        """categories : WORD ':' phrases '.'"""
        p[0] = [(p[1], p[3])]
    
    def p_material_phrases(self, p):
        """phrases : phrases ',' phrases"""
        p[0] = p[1] + p[3]

    def p_material_phrase(self, p):
        """phrases : phrase"""
        p[0] = [p[1]]

    def p_material_words(self, p):
        """phrase : phrase BLANK phrase"""
        p[0] = p[1] + p[3]

    def p_material_word(self, p):
        """phrase : WORD"""
        p[0] = [p[1]]



class ExpressionParser(SimpleParser):
    t_WORD = r'[A-Za-z]+'
    t_BLANK = r'\ +'
    literals = ['"', '|']
    
    def p_expression_probability(self, p):
        """expression : event"""
        p[0] = p[1]
    
    def p_expression_conditional(self, p):
        """expression : event '|' event"""
        p[0] = p[1], p[3]

    def p_expression_events(self, p):
        """event : '"' phrase '"'"""
        p[0] = p[2]
    
    def p_expression_event(self, p):
        """event : WORD"""
        p[0] = p[1]

    def p_expression_words(self, p):
        """phrase : phrase BLANK phrase"""
        p[0] = p[1] + p[3]
    
    def p_expression_word(self, p):
        """phrase : WORD"""
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
                return functools.reduce(lambda a,b: a*b, [ self.p((w,b), laplace) for w in a ])
            elif self.is_category(a) and self.is_phrase(b):
                return fractions.Fraction(
                    self.P((b,a), laplace) * self.P(a, laplace),
                    sum(self.P((b,k), laplace) * self.P(k, laplace) for k in self.categories) )

        raise NotImplementedError
   
   
    def query(self, expression, laplace=0):
        return self.P(self.parser.parse(expression), laplace)




class NaiveCommand(BaseCommand):
    """
    $ aiclass naive data:spam-ham
    >>> \size
    12
    >>> SPAM
    3/8
    >>> "SECRET"|SPAM
    1/3
    >>> "SECRET"|HAM
    1/15
    >>> SPAM|"SPORTS"
    1/6
    >>> SPAM|"SECRET IS SECRET"
    25/26
    >>> SPAM|"TODAY IS SECRET"
    0

    $ aiclass naive -l 1 data:spam-ham
    >>> SPAM
    2/5
    >>> HAM
    3/5
    >>> "TODAY"|SPAM
    1/21
    >>> "TODAY"|HAM
    1/9
    >>> SPAM|"TODAY IS SECRET"
    324/667

    $ aiclass naive -l 1 data:movie-song
    >>> MOVIE
    1/2
    >>> SONG
    1/2
    >>> "PERFECT"|MOVIE
    3/19
    >>> "PERFECT"|SONG
    2/19
    >>> "STORM"|MOVIE
    1/19
    >>> "STORM"|SONG
    2/19
    >>> MOVIE|"PERFECT STORM"
    3/7

    $ aiclass naive data:movie-song
    >>> MOVIE|"PERFECT STORM"
    0
    """


    name = 'naive'
    description = 'naive bayes'
    help = 'naive bayes'


    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('-l', '--laplace', default=0, type=int)
        parser.add_argument('material')


    @classmethod
    def create_from_args(cls, args):
        return cls(cls.get_data(args.material), args.laplace)


    def __init__(self, material, laplace):
        from aiclass import naive
        self.material = MaterialParser().parse(material)
        self.laplace = laplace


    def call(self, string):
        if string == r'\q': 
            raise SystemExit
        elif string == r'\size':
            return self.material.size_of_vocabulary()
        else:
            return self.material.query(string, self.laplace)



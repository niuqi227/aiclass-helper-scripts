from aiclass.command import BaseCommand
from aiclass.parser import SimpleParser
import itertools, operator


class BaseExpr(object):
    
    def eval(self, ctx):
        raise NotImplementedError
    
    def find_symbols(self, symbols):
        raise NotImplementedError
        
    def validate(self):
        symbols = self.find_symbols(())
        results = [ 
            self.eval(dict(zip(symbols, values)))
                for values in itertools.product(
                    (True, False),
                    repeat=len(symbols)) ]

        if all(results):
            return 'V'
        elif any(results):
            return 'S'
        else:
            return 'U'


class Symbol(BaseExpr):

    def __init__(self, name):
        self.name = name

    def eval(self, ctx):
        return ctx[self.name]
        
    def find_symbols(self, symbols):
        if self.name not in symbols:
            return symbols + (self.name,)
        else:
            return symbols


class UnOp(BaseExpr):

    def __init__(self, op, inner):
        self.op = op
        self.inner = inner
        
    def eval(self, ctx):
        return self.op(self.inner.eval(ctx))

    def find_symbols(self, symbols):
        return self.inner.find_symbols(symbols)


class BinOp(BaseExpr):
    
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, ctx):
        return self.op(self.left.eval(ctx), self.right.eval(ctx))
        
    def find_symbols(self, symbols):
        return self.right.find_symbols(self.left.find_symbols(symbols))


def CONST(regex, op):
    def wrapper(self, t):
        t.value = op
        return t
    
    wrapper.__doc__ = regex
    return wrapper


class Parser(SimpleParser):
    t_SYMBOL = r'[a-zA-Z_]\w*'
    t_NOT = CONST(r'\~', operator.__not__)
    t_AND = CONST(r'\&', operator.__and__)
    t_OR = CONST(r'\|', operator.__or__)
    t_IMPLY = CONST(r'\=\>', lambda a,b: (not a) or b)
    t_EQUAL = CONST(r'\<\=\>', operator.__eq__)
    t_ignore = ' '
    literals = ['(', ')']

    precedence = [
        ('left', 'IMPLY', 'EQUAL'),
        ('left', 'AND', 'OR'),
        ('right', 'NOT')]
        
    def p_symbol(self, p):
        """expression : SYMBOL"""
        p[0] = Symbol(p[1])

    def p_paren(self, p):
        """expression : '(' expression ')' """
        p[0] = p[2]

    def p_unary_expression(self, p):
        """expression : NOT expression"""
        p[0] = UnOp(p[1], p[2])
        
    def p_binary_expression(self, p):
        """expression : expression AND expression
                      | expression OR  expression
                      | expression IMPLY expression
                      | expression EQUAL expression"""
        p[0] = BinOp(p[2], p[1], p[3])




class ProposCommand(BaseCommand):
    """
    $ aiclass props
    >>> p|~p
    V
    >>> p&~p
    U
    >>> p|q|(p<=>q)
    V
    >>> (p=>q)|(q=>p)
    V
    >>> ((food=>party)|(drinks=>party))=>((food&drinks)=>party)
    V

    $ aiclass props
    >>> (smoke=>fire)<=>(smoke|~fire)
    S
    >>> (smoke=>fire)<=>(~smoke=>~fire)
    S
    >>> (smoke=>fire)<=>(~fire=>~smoke)
    V
    >>> big|dumb|(big=>dumb)
    V
    >>> big&dumb<=>~(~big|~dumb)
    V
    """

    
    name = 'props'
    description = 'propositional logic'
    help = 'propositional logic'

    def __init__(self):
        self.parser = Parser()

    def call(self, string):
        if string == r'\q':
            raise SystemExit

        return self.parser.parse(string).validate()


from ply import lex, yacc



class SimpleParser(object):

    def __init__(self):
        self.tokens = [ a[2:] for a in dir(self) if a[:2] == 't_' and a[2:].isupper() ]
        self.lexer = lex.lex(module=self, debug=False)
        self.parser = yacc.yacc(module=self, debug=False, write_tables=False)


    def t_error(self, t):
        raise Exception("Illegal character '%s'!" % t.value[0])

    
    def p_error(self, p):
        raise Exception("Syntax Error!")


    def parse(self, data):
        return self.parser.parse(data)



def parse_graph(data):
    edges = []

    for line in data.splitlines():
        line = line.strip()
        if line:
            a, b = line.split('->', 1)
            edges.append((a.strip(), b.strip()))
    
    return edges 


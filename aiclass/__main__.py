try:
    import readline
except ImportError:
    pass

import argparse
import traceback
import sys

def configure_search_parser(parsers):
    description='search'
    parser = parsers.add_parser(
        'search',
        description=description,
        help=description)

    parser.add_argument(
        'type',
        choices=['astar', 'bfs', 'cfs', 'dfs'],
        help='type of searcher')
    parser.add_argument('problem', help='problem to search')


def configure_network_parser(parsers):
    description='bayes network'

    parser = parsers.add_parser(
        'network',
        description=description,
        help=description)
        
    parser.add_argument('data', help='data of network')


def configure_naive_parser(parsers):
    description='naive bayes'

    parser = parsers.add_parser(
        'naive',
        description=description,
        help=description)

    parser.add_argument('-l', '--laplace', default=0, type=int)
    parser.add_argument('material')


def configure_plan_parser(parsers):
    description='classic plan'

    parser = parsers.add_parser(
        'plan',
        description=description,
        help=description)
    
    parser.add_argument('-i', '--initial', help='initialize data')


def configure_propos_parser(parsers):
    description='propositional logic'

    parser = parsers.add_parser(
        'propos',
        description=description,
        help=description)


def get_data(location):
    if location.startswith('data:'):
        from aiclass import data
        return getattr(data, location[5:].upper().replace('-', '_')+'_DATA')
    
    with open(location, 'r') as f:
        return f.read()


def enter_search(args):
    from aiclass import search
    SearcherClass = getattr(search, args.type.capitalize() + 'Searcher')

    if args.problem.startswith('data:'):
        from aiclass import data
        ProblemClass = getattr(data, args.problem[5:].upper().replace('-', '_')+'_PROBLEM')
    else:
        problem_name = args.problem.split('.')
        mod_name, class_name = '.'.join(problem_name[:-1]), problem_name[-1]
        ProblemClass = getattr(__import__(mod_name, fromlist=[class_name]), class_name)
    
    problem = ProblemClass()
    searcher = SearcherClass(problem)

    while True:
        string = raw_input('>>> ')
        if string == 'quit':
            break
        elif string == 'count':
            print searcher.expand_count
        elif string == 'expand':
            print searcher.expand()
        elif string == 'explored':
            for e in searcher.get_explored():
                print e
        elif string == 'frontier':
            for f in searcher._frontier:
                print f[0]
        elif string == 'go':
            if searcher.search():
                for s in searcher.trace_states():
                    print s
            else:
                print 'search failed'
        elif string.startswith('trace '):
            state = string[6:].strip()
            try:
                for s in searcher.trace_states(state):
                    print s
            except Exception, e:
                traceback.print_exception(*sys.exc_info())
        else:
            print 'count\texpand\texplored\tfrontier\tgo\tquit\ttrace'
    print 'quit.'


def enter_network(args):
    from aiclass import network
    bayes_network = network.BayesNetwork(get_data(args.data))
    while True:
        string = raw_input('>>> ')
        if string == r'\q':
            break
        elif string == 'params':
            print bayes_network.parameters()
        else:
            try:
                print bayes_network.validate(string)
            except Exception, e:
                traceback.print_exception(*sys.exc_info())
                print r'Enter \q to quit'
    print 'quit.'    


def enter_naive(args):
    from aiclass import naive
    material = naive.MaterialParser().parse(get_data(args.material))
    laplace = args.laplace
    while True:
        string = raw_input('>>> ')
        if string == r'\q':
            break
        elif string == r'\size':
            print material.size_of_vocabulary()
        else:
            try:
                print 'P(%s) = %s'%(string, material.query(string, laplace))
            except Exception, e:
                traceback.print_exception(*sys.exc_info())
                print r'Enter \q to quit'
    print 'quit.'    


def enter_propos(args):
    from aiclass import propositional
    parser = propositional.Parser()
    while True:
        string = raw_input('>>> ')
        if string == r'\q':
            break
        try:
            print parser.parse(string).validate()
        except Exception, e:
            traceback.print_exception(*sys.exc_info())
            print r'Enter \q to quit'
    print 'quit.'


def enter_plan(args):
    from aiclass import plan
    db = plan.ClassicPlanDatabase()
    if args.initial:
        db.evaluate(get_data(args.initial))
    while True:
        string = raw_input('>>> ')
        if string == r'\q':
            break
        try:
            print db.eval(string)
        except Exception, e:
            traceback.print_exception(*sys.exc_info())
            print r'Enter \q to quit'
    print 'quit.'    


def main():
    parser = argparse.ArgumentParser(prog='aiclass')
    subparsers = parser.add_subparsers(title='available commands', dest='command')
    configure_search_parser(subparsers)
    configure_network_parser(subparsers)
    configure_naive_parser(subparsers)
    configure_propos_parser(subparsers)
    configure_plan_parser(subparsers)

    args = parser.parse_args()

    if args.command == 'search':
        enter_search(args)
    elif args.command == 'network':
        enter_network(args)
    elif args.command == 'naive':
        enter_naive(args)
    elif args.command == 'propos':
        enter_propos(args)
    elif args.command == 'plan':
        enter_plan(args)
        


    
if __name__ == '__main__':
    main()



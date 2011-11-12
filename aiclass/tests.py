import fractions
import unittest
import itertools

from aiclass import search, bayes, propositional, plan



class TestRomania(unittest.TestCase):

    def setUp(self):
        self.problem = search.RomaniaProblem()
    

    def test_uniform_cost_search(self):
        searcher = search.CfsSearcher(self.problem)
        self.assertEqual(searcher.expand(), 'Arad')
        self.assertEqual(searcher.expand(), 'Zerind')
        self.assertEqual(searcher.expand(), 'Timisoara')
        self.assertEqual(searcher.expand(), 'Sibiu')
        self.assertEqual(searcher.expand(), 'Oradea')
        self.assertEqual(searcher.expand(), 'Rimnicu Vilcea')
        self.assertEqual(searcher.expand(), 'Lugoj')
        self.assertEqual(searcher.expand(), 'Fagaras')
        self.assertEqual(searcher.expand(), 'Mehadia')
        self.assertEqual(searcher.expand(), 'Pitesti')
        self.assertEqual(searcher.expand(), 'Craiova')
        self.assertEqual(searcher.expand(), 'Drobeta')
        self.assertEqual(searcher.expand(), 'Bucharest')
        self.assertEqual(searcher.goal_reached, 'Bucharest')
        self.assertEqual(
            searcher.get_solution_state_path(),
            ['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest'])


    def test_astar_search(self):
        searcher = search.AstarSearcher(self.problem)
        self.assertEqual(searcher.expand(), 'Arad')
        self.assertEqual(searcher.expand(), 'Sibiu')
        self.assertEqual(searcher.expand(), 'Rimnicu Vilcea')
        self.assertEqual(searcher.expand(), 'Fagaras')
        self.assertEqual(searcher.expand(), 'Pitesti')
        self.assertEqual(searcher.expand(), 'Bucharest')
        self.assertEqual(
            searcher.get_solution_state_path(),
            ['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest'])



class NodeCountProblemMixin(object):
    initial, goal, data, bfs_count, dfs_count = None, None, None, None, None

    def setUp(self):
        self.problem = search.NodeCountProblem(
            self.initial,
            self.goal,
            self.data)

    def test_bfs(self):
        searcher = search.BfsSearcher(self.problem)
        searcher.search()
        self.assertEqual(searcher.expand_count, self.bfs_count)

    def test_dfs(self):
        searcher = search.DfsSearcher(self.problem)
        searcher.search()
        self.assertEqual(searcher.expand_count, self.dfs_count)



SEARCH_TREE_DATA = '''
1 -> 2
1 -> 3
1 -> 4
2 -> 5
2 -> 6
3 -> 7
3 -> 8
4 -> 9
4 -> 10
'''



class TestSearchTree_LeftToRight(NodeCountProblemMixin, unittest.TestCase):
    initial = '1'
    goal = '6'
    data = SEARCH_TREE_DATA
    bfs_count = 6
    dfs_count = 4



class TestSearchTree_RightToLeft(NodeCountProblemMixin, unittest.TestCase):
    initial = '1'
    goal = '9'
    data = SEARCH_TREE_DATA
    bfs_count = 9
    dfs_count = 9



SEARCH_TREE2_DATA_LEFT_TO_RIGHT = '''
1 -> 2
1 -> 3
1 -> 4
2 -> 5
2 -> 6
3 -> 7
3 -> 8
4 -> 9
4 -> 10
7 -> 11
7 -> 12
8 -> 13
'''



class TestSearchTree2_LeftToRight(NodeCountProblemMixin, unittest.TestCase):
    initial = '1'
    goal = '13'
    data = SEARCH_TREE2_DATA_LEFT_TO_RIGHT
    bfs_count = 13
    dfs_count = 10



SEARCH_TREE2_DATA_RIGHT_TO_LEFT = '''
1 -> 2
1 -> 3
1 -> 4
2 -> 5
2 -> 6
3 -> 7
3 -> 8
4 -> 9
4 -> 10
7 -> 11
8 -> 12
8 -> 13
'''



class TestSearchTree2_RightToLeft(NodeCountProblemMixin, unittest.TestCase):
    initial = '1'
    goal = '11'
    data = SEARCH_TREE2_DATA_RIGHT_TO_LEFT
    bfs_count = 11
    dfs_count = 7



SEARCH_NETWORK_DATA = '''
1 -> 2
1 -> 3
2 -> 4
2 -> 5
3 -> 5
3 -> 6
4 -> 7
4 -> 8
5 -> 8
5 -> 9
6 -> 9
6 -> 10
7 -> 11
8 -> 11
8 -> 12
9 -> 12
9 -> 13
10 -> 13
11 -> 14
12 -> 14
12 -> 15
13 -> 15
14 -> 16
15 -> 16
'''



class TestSearchNetwork_LeftToRight(NodeCountProblemMixin, unittest.TestCase):
    initial = '1'
    goal = '10'
    data = SEARCH_NETWORK_DATA
    bfs_count = 10
    dfs_count = 16



class TestSearchNetwork_RightToLeft(NodeCountProblemMixin, unittest.TestCase):
    initial = '1'
    goal = '7'
    data = SEARCH_NETWORK_DATA
    bfs_count = 7
    dfs_count = 4



class TestAstarSearch(unittest.TestCase):

    def setUp(self):
        self.problem = search.AstarSearchProblem()

    def test_astar_search(self):
        searcher = search.AstarSearcher(self.problem)
        self.assertEqual(searcher.expand(), 'a1')
        self.assertEqual(searcher.expand(), 'b1')
        self.assertEqual(searcher.expand(), 'c1')
        self.assertEqual(searcher.expand(), 'd1')


GENERAL_BAYES_NET_DATA = '''
a -> b
a -> c
a -> d
b -> e
c -> f
d -> f
'''

GENERAL_BAYES_NET2_DATA = '''
a -> d
b -> d
c -> d
d -> e
d -> f
d -> g
c -> g
'''

GENERAL_BAYES_NET3_DATA = '''
BA -> BD
BD -> BM
BD -> BF
AB -> BF
FBB -> BF
BF -> L
BF -> OL
BF -> GG
BF -> CWS
NO -> OL
NO -> DS
NG -> GG
NG -> CWS
FLB -> CWS
SB -> CWS
'''

PARAMETER_COUNT_DATA = '''
a -> b
a -> d
a -> e
b -> e
d -> e
c -> d
'''


class TestBayesParameterCount(unittest.TestCase):

    def test_general_bayes_net_data(self):
        self.assertEqual(bayes.parameters(GENERAL_BAYES_NET_DATA), 13)

    def test_general_bayes_net2_data(self):
        self.assertEqual(bayes.parameters(GENERAL_BAYES_NET2_DATA), 19)

    def test_general_bayes_net3_data(self):
        self.assertEqual(bayes.parameters(GENERAL_BAYES_NET3_DATA), 47)

    def test_parameter_count(self):
        self.assertEqual(bayes.parameters(PARAMETER_COUNT_DATA), 16)


    
SPAM_HAM_DATA = '''
SPAM:
OFFER IS SECRET,
CLICK SECRET LINK,
SECRET SPORTS LINK.

HAM:
PLAY SPORTS TODAY,
WENT PLAY SPORTS,
SECRET SPORTS EVENT,
SPORTS IS TODAY,
SPORTS COSTS MONEY.
'''



class TestSpamHam(unittest.TestCase):

    def setUp(self):
        self.material = bayes.MaterialParser().parse(SPAM_HAM_DATA)
        
    def test_7_spam_detection(self):
        self.assertEqual(self.material.size_of_vocabulary(), 12)

    def test_8_question(self):
        self.assertEqual(self.material.query('''SPAM'''), fractions.Fraction(3, 8))

    def test_9_maximum_likelihood_1(self):
        self.assertEqual(self.material.query('''"SECRET"|SPAM'''), fractions.Fraction(1,3))
        self.assertEqual(self.material.query('''"SECRET"|HAM'''), fractions.Fraction(1,15))

    def test_11_question(self):
        self.assertEqual(self.material.query('''SPAM|"SPORTS"'''), fractions.Fraction(1, 6))

    def test_12_question(self):
        self.assertEqual(self.material.query('''SPAM|"SECRET IS SECRET"'''), fractions.Fraction(25, 26))

    def test_13_question(self):
        self.assertEqual(self.material.query('''SPAM|"TODAY IS SECRET"'''), 0)
        
    def test_15_question(self):
        self.assertEqual(self.material.query('''SPAM''', laplace=1), fractions.Fraction(2,5))
        self.assertEqual(self.material.query('''HAM''', laplace=1), fractions.Fraction(3,5)) 
        self.assertEqual(self.material.query('''"TODAY"|SPAM''', laplace=1), fractions.Fraction(1,21))
        self.assertEqual(self.material.query('''"TODAY"|HAM''', laplace=1), fractions.Fraction(1,9))

    def test_16_question(self):
        self.assertEqual(self.material.query('''SPAM|"TODAY IS SECRET"''', laplace=1), fractions.Fraction(324, 667))



MOVIE_SONG_DATA = '''
MOVIE:
A PERFECT WORD,
MY PERFECT WOMAN,
PRETTY WOMAN.

SONG:
A PERFECT DAY,
ELECTRIC STORM,
ANOTHER RAINY DAY.
'''



class TestMovieSong(unittest.TestCase):

    def setUp(self):
        self.material = bayes.MaterialParser().parse(MOVIE_SONG_DATA)

    def test_naive_bayes(self):
        self.assertEqual(self.material.query('''MOVIE''', laplace=1), fractions.Fraction(1, 2))
        self.assertEqual(self.material.query('''SONG''', laplace=1), fractions.Fraction(1, 2))
        self.assertEqual(self.material.query('''"PERFECT"|MOVIE''', laplace=1), fractions.Fraction(3, 19))
        self.assertEqual(self.material.query('''"PERFECT"|SONG''', laplace=1), fractions.Fraction(2, 19))
        self.assertEqual(self.material.query('''"STORM"|MOVIE''', laplace=1), fractions.Fraction(1, 19))
        self.assertEqual(self.material.query('''"STORM"|SONG''', laplace=1), fractions.Fraction(2, 19))

    def test_naive_bayes2(self):
        self.assertEqual(self.material.query('''MOVIE|"PERFECT STORM"''', laplace=1), fractions.Fraction(3, 7))
        
    def test_maximum_likelihood(self):
        self.assertEqual(self.material.query('''MOVIE|"PERFECT STORM"'''), 0)



class TestPropositional(unittest.TestCase):

    def test_terminology(self):
        self.assertEqual(propositional.Parser().parse("p|~p").validate(), 'V')
        self.assertEqual(propositional.Parser().parse("p&~p").validate(), 'U')
        self.assertEqual(propositional.Parser().parse("p|q|(p<=>q)").validate(), 'V')
        self.assertEqual(propositional.Parser().parse("(p=>q)|(q=>p)").validate(), 'V')
        self.assertEqual(propositional.Parser().parse("((food=>party)|(drinks=>party))=>((food&drinks)=>party)").validate(), 'V')

    def test_logic(self):
        self.assertEqual(propositional.Parser().parse("(smoke=>fire)<=>(smoke|~fire)").validate(), 'S')
        self.assertEqual(propositional.Parser().parse("(smoke=>fire)<=>(~smoke=>~fire)").validate(), 'S')
        self.assertEqual(propositional.Parser().parse("(smoke=>fire)<=>(~fire=>~smoke)").validate(), 'V')
        self.assertEqual(propositional.Parser().parse("big|dumb|(big=>dumb)").validate(), 'V')
        self.assertEqual(propositional.Parser().parse("big&dumb<=>~(~big|~dumb)").validate(), 'V')
    


MONKEYS_AND_BANANAS_DATA = '''
init()[]{
At(monkey,a),
At(bananas,b),
At(box,c),
Height(monkey,low),
Height(box,low),
Height(bananas,high),
Pushable(box),
Climbable(box)}.

go(X,Y)[
At(monkey,X)]{
~At(monkey,X),
At(monkey,Y)}.

push(B,X,Y)[
At(monkey,X),
Pushable(B)]{
~At(B,X),
~At(monkey,X),
At(B,Y),
At(monkey,Y)}.

climbup(B)[
At(monkey,X),
At(B,X),
Climbable(B)]{
~Height(monkey,low),
On(monkey,B),
Height(monkey,high)}.

grasp(B)[
Height(monkey,H),
Height(B,H),
At(monkey,X),
At(B,X)]{
Have(monkey,B)}.

climbdown(B)[
On(monkey,B),
Height(monkey,high)]{
~On(monkey,B),
~Height(monkey,high),
Height(monkey,low)}.

init.
At(monkey,a).
go(a,c).
push(box,c,b).
climbup(box).
grasp(bananas).
climbdown(box).'''


class TestMonkeyAndBananas(unittest.TestCase):

    def setUp(self):
        self.db = plan.ClassicPlanDatabase()
        self.db.evaluate(MONKEYS_AND_BANANAS_DATA)

    def test_monkeys_and_bananas(self):
        self.assertTrue(self.db.eval('''Have(monkey,bananas).'''))
        self.assertFalse(self.db.eval('''At(box,c).'''))
        self.assertTrue(self.db.eval('''At(monkey,b).'''))
        self.assertTrue(self.db.eval('''At(bananas,b).'''))
        self.assertFalse(self.db.eval('''Height(monkey,high).'''))
        self.assertTrue(self.db.eval('''Height(bananas,high).'''))





import fractions
import unittest
import itertools

from aiclass import search, naive, propositional, plan, network, data


class TestRomania(unittest.TestCase):

    def setUp(self):
        self.problem = data.ROMANIA_PROBLEM()

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
            searcher.trace_states(),
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
            searcher.trace_states(),
            ['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest'])


class TestNodeCount(object):

    def assertBFS(self, problem, count):
        searcher = search.BfsSearcher(problem)
        searcher.search()
        self.assertEqual(searcher.expand_count, count)
    
    def assertDFS(self, problem, count):
        searcher = search.DfsSearcher(problem)
        searcher.search()
        self.assertEqual(searcher.expand_count, count)

    def test_search_tree_ltr(self):
        problem = data.SEARCH_TREE_LTR_PROBLEM()
        self.assertBFS(problem, 6)
        self.assertDFS(problem, 4)

    def test_search_tree_rtl(self):
        problem = data.SEARCH_TREE_RTL_PROBLEM()
        self.assertBFS(problem, 9)
        self.assertDFS(problem, 9)

    def test_search_tree_2_ltr(self):
        problem = data.SEARCH_TREE_2_LTR_PROBLEM()
        self.assertBFS(problem, 13)
        self.assertDFS(problem, 10)

    def test_search_tree_2_rtl(self):
        problem = data.SEARCH_TREE_2_RTL_PROBLEM()
        self.assertBFS(problem, 11)
        self.assertDFS(problem, 7)

    def test_search_network_ltr(self):
        problem = data.SEARCH_NETWORK_LTR_PROBLEM()
        self.assertBFS(problem, 10)
        self.assertDFS(problem, 16)

    def test_search_network_rtl(self):
        problem = data.SEARCH_NETWORK_RTL_PROBLEM()
        self.assertBFS(problem, 7)
        self.assertDFS(problem, 4)


class TestAstarSearch(unittest.TestCase):

    def setUp(self):
        self.problem = data.ASTAR_SEARCH_PROBLEM()

    def test_astar_search(self):
        searcher = search.AstarSearcher(self.problem)
        self.assertEqual(searcher.expand(), 'a1')
        self.assertEqual(searcher.expand(), 'b1')
        self.assertEqual(searcher.expand(), 'c1')
        self.assertEqual(searcher.expand(), 'd1')


class TestBayesParameterCount(unittest.TestCase):

    def assertParams(self, data, params):
        self.assertEqual(network.BayesNetwork(data).parameters(), params)

    def test_bayes_network(self):
        self.assertParams(data.BAYES_NETWORK_DATA, 3)

    def test_general_bayes_net(self):
        self.assertParams(data.GENERAL_BAYES_NET_DATA, 13)

    def test_general_bayes_net_2(self):
        self.assertParams(data.GENERAL_BAYES_NET_2_DATA, 19)

    def test_general_bayes_net_3(self):
        self.assertParams(data.GENERAL_BAYES_NET_3_DATA, 47)

    def test_parameter_count(self):
        self.assertParams(data.PARAMETER_COUNT_DATA, 16)


class TestConditionIndependence(unittest.TestCase):

    def test_d_separation(self):
        validator = network.BayesNetwork(data.D_SEPARATION_DATA)
        self.assertFalse(validator.validate("C_|_A"))
        self.assertTrue(validator.validate("C_|_A|B"))
        self.assertFalse(validator.validate("C_|_D"))
        self.assertTrue(validator.validate("C_|_D|A"))
        self.assertTrue(validator.validate("E_|_C|D"))

    def test_d_separation_2(self):
        validator = network.BayesNetwork(data.D_SEPARATION_2_DATA)
        self.assertFalse(validator.validate("A_|_E"))
        self.assertFalse(validator.validate("A_|_E|B"))
        self.assertTrue(validator.validate("A_|_E|C"))
        self.assertTrue(validator.validate("A_|_B"))
        self.assertFalse(validator.validate("A_|_B|C"))

    def test_d_separation_3(self):
        validator = network.BayesNetwork(data.D_SEPARATION_3_DATA)
        self.assertTrue(validator.validate("F_|_A"))
        self.assertFalse(validator.validate("F_|_A|D"))
        self.assertFalse(validator.validate("F_|_A|G"))
        self.assertTrue(validator.validate("F_|_A|H"))
        
    def test_conditional_independence(self):
        validator = network.BayesNetwork(data.CONDITIONAL_INDEPENDENCE_DATA)
        self.assertFalse(validator.validate("B_|_C"))
        self.assertFalse(validator.validate("B_|_C|D"))
        self.assertTrue(validator.validate("B_|_C|A"))
        self.assertFalse(validator.validate("B_|_C|A,D"))

    def test_conditional_independence_2(self):
        validator = network.BayesNetwork(data.CONDITIONAL_INDEPENDENCE_2_DATA)
        self.assertFalse(validator.validate("C_|_E|A"))
        self.assertFalse(validator.validate("B_|_D|C,E"))
        self.assertFalse(validator.validate("A_|_C|E"))
        self.assertTrue(validator.validate("A_|_C|B"))


class TestNaiveBayes(unittest.TestCase):
        
    def test_spam_ham(self):
        material = naive.MaterialParser().parse(data.SPAM_HAM_DATA)
        self.assertEqual(material.size_of_vocabulary(), 12)
        self.assertEqual(material.query('''SPAM'''), fractions.Fraction(3, 8))
        self.assertEqual(material.query('''"SECRET"|SPAM'''), fractions.Fraction(1,3))
        self.assertEqual(material.query('''"SECRET"|HAM'''), fractions.Fraction(1,15))
        self.assertEqual(material.query('''SPAM|"SPORTS"'''), fractions.Fraction(1, 6))
        self.assertEqual(material.query('''SPAM|"SECRET IS SECRET"'''), fractions.Fraction(25, 26))
        self.assertEqual(material.query('''SPAM|"TODAY IS SECRET"'''), 0)
        self.assertEqual(material.query('''SPAM''', laplace=1), fractions.Fraction(2,5))
        self.assertEqual(material.query('''HAM''', laplace=1), fractions.Fraction(3,5)) 
        self.assertEqual(material.query('''"TODAY"|SPAM''', laplace=1), fractions.Fraction(1,21))
        self.assertEqual(material.query('''"TODAY"|HAM''', laplace=1), fractions.Fraction(1,9))
        self.assertEqual(material.query('''SPAM|"TODAY IS SECRET"''', laplace=1), fractions.Fraction(324, 667))

    def test_movie_song(self):
        material = naive.MaterialParser().parse(data.MOVIE_SONG_DATA)
        self.assertEqual(material.query('''MOVIE''', laplace=1), fractions.Fraction(1, 2))
        self.assertEqual(material.query('''SONG''', laplace=1), fractions.Fraction(1, 2))
        self.assertEqual(material.query('''"PERFECT"|MOVIE''', laplace=1), fractions.Fraction(3, 19))
        self.assertEqual(material.query('''"PERFECT"|SONG''', laplace=1), fractions.Fraction(2, 19))
        self.assertEqual(material.query('''"STORM"|MOVIE''', laplace=1), fractions.Fraction(1, 19))
        self.assertEqual(material.query('''"STORM"|SONG''', laplace=1), fractions.Fraction(2, 19))
        self.assertEqual(material.query('''MOVIE|"PERFECT STORM"''', laplace=1), fractions.Fraction(3, 7))
        self.assertEqual(material.query('''MOVIE|"PERFECT STORM"'''), 0)


class TestPropositional(unittest.TestCase):

    def setUp(self):
        self.parser = propositional.Parser()
        
    def assertProps(self, statement, result):
        self.assertEqual(self.parser.parse(statement).validate(), result)

    def test_terminology(self):
        self.assertProps("p|~p", 'V')
        self.assertProps("p&~p", 'U')
        self.assertProps("p|q|(p<=>q)", 'V')
        self.assertProps("(p=>q)|(q=>p)", 'V')
        self.assertProps("((food=>party)|(drinks=>party))=>((food&drinks)=>party)", 'V')

    def test_logic(self):
        self.assertProps("(smoke=>fire)<=>(smoke|~fire)", 'S')
        self.assertProps("(smoke=>fire)<=>(~smoke=>~fire)", 'S')
        self.assertProps("(smoke=>fire)<=>(~fire=>~smoke)", 'V')
        self.assertProps("big|dumb|(big=>dumb)", 'V')
        self.assertProps("big&dumb<=>~(~big|~dumb)", 'V')


class TestMonkeyAndBananas(unittest.TestCase):

    def test_monkeys_and_bananas(self):
        db = plan.ClassicPlanDatabase()
        db.evaluate(data.MONKEY_AND_BANANAS_DATA)
        self.assertTrue(db.eval('''Have(monkey,bananas).'''))
        self.assertFalse(db.eval('''At(box,c).'''))
        self.assertTrue(db.eval('''At(monkey,b).'''))
        self.assertTrue(db.eval('''At(bananas,b).'''))
        self.assertFalse(db.eval('''Height(monkey,high).'''))
        self.assertTrue(db.eval('''Height(bananas,high).'''))




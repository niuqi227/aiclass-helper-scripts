from aiclass import search


ROMANIA_MAP_DATA = '''
Arad -> Zerind: 75
Arad -> Timisoara: 118
Arad -> Sibiu: 140
Zerind -> Oradea: 71
Oradea -> Sibiu: 151
Timisoara -> Lugoj: 111
Lugoj -> Mehadia: 70
Mehadia -> Drobeta: 75
Drobeta -> Craiova: 120
Craiova -> Rimnicu Vilcea: 146
Craiova -> Pitesti: 138
Rimnicu Vilcea -> Sibiu: 80
Rimnicu Vilcea -> Pitesti: 97
Pitesti -> Bucharest: 101
Sibiu -> Fagaras: 99
Fagaras -> Bucharest: 211
Bucharest -> Urziceni: 85
Urziceni -> Vaslui: 142
Vaslui -> Iasi: 92
Iasi -> Neamt: 87
Urziceni -> Hirsova: 98
Hirsova -> Eforie: 86
'''


DISTANCE_TO_BUCHAREST = '''
Arad: 366
Zerind: 374
Oradea: 380
Sibiu: 253
Timisoara: 329
Lugoj: 244
Mehadia: 241
Drobeta: 242
Craiova: 160
Fagaras: 176
Rimnicu Vilcea: 193
Pitesti: 100
Bucharest: 0
Urziceni: 80
Vaslui: 199
Iasi: 226
Neamt: 234
Hirsova: 151
Eforie: 161
'''



class ROMANIA_PROBLEM(search.MapRoutingProblem):
    initial = 'Arad'
    goal = 'Bucharest'
    paths = ROMANIA_MAP_DATA
    heuristics = DISTANCE_TO_BUCHAREST



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

SEARCH_TREE_2_DATA_LTR = '''
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

SEARCH_TREE_2_DATA_RTL = '''
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


class SEARCH_TREE_LTR_PROBLEM(search.NodeCountProblem):
    initial = '1'
    goal = '6'
    paths = SEARCH_TREE_DATA


class SEARCH_TREE_RTL_PROBLEM(search.NodeCountProblem):
    initial = '1'
    goal = '9'
    paths = SEARCH_TREE_DATA


class SEARCH_TREE_2_LTR_PROBLEM(search.NodeCountProblem):
    initial = '1'
    goal = '13'
    paths = SEARCH_TREE_2_DATA_LTR


class SEARCH_TREE_2_RTL_PROBLEM(search.NodeCountProblem):
    initial = '1'
    goal = '11'
    paths = SEARCH_TREE_2_DATA_RTL


class SEARCH_NETWORK_LTR_PROBLEM(search.NodeCountProblem):
    initial = '1'
    goal = '10'
    paths = SEARCH_NETWORK_DATA


class SEARCH_NETWORK_RTL_PROBLEM(search.NodeCountProblem):
    initial = '1'
    goal = '7'
    paths = SEARCH_NETWORK_DATA



class ASTAR_SEARCH_PROBLEM(search.Problem):

    def __init__(self):
        self.h = {}
        for y in ['a','b','c','d']:
            for x in [1,2,3,4,5,6]:
                self.h['%s%d'%(y,x)] = min([ord('d')-ord(y)+1, 6-x+1])
        self.h['d6'] = 0


    def actions(self, state):
        y, x = state
        actions = []
        if y != 'a':
            actions.append('%s%s'%(chr(ord(y)-1), x))
        if y != 'd':
            actions.append('%s%s'%(chr(ord(y)+1), x))
        if x != '1':
            actions.append('%s%s'%(y, chr(ord(x)-1)))
        if x != '6':
            actions.append('%s%s'%(y, chr(ord(x)+1)))
        return actions


    def result(self, action):
        return action


    def cost(self, action):
        return 1


    def get_initial(self):
        return 'a1'


    def goal_test(self, state):
        return state == 'd6'


    def heuristic(self, state):
        return self.h[state]
        


BAYES_NETWORK_DATA = '''
A -> B
'''

GENERAL_BAYES_NET_DATA = '''
A -> B
A -> C
A -> D
B -> E
C -> F
D -> F
'''

GENERAL_BAYES_NET_2_DATA = '''
A -> D
B -> D
C -> D
D -> E
D -> F
D -> G
C -> G
'''

GENERAL_BAYES_NET_3_DATA = '''
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

D_SEPARATION_DATA = '''
A -> B
B -> C
A -> D
D -> E
'''

D_SEPARATION_2_DATA = '''
A -> C
B -> C
C -> D
C -> E
'''

D_SEPARATION_3_DATA = '''
A -> B
C -> B
B -> D
F -> E
E -> D
D -> G
H -> G
'''

CONDITIONAL_INDEPENDENCE_DATA = '''
A -> B
A -> C
B -> D
C -> D
'''

CONDITIONAL_INDEPENDENCE_2_DATA = PARAMETER_COUNT_DATA = '''
A -> B
A -> E
A -> D
C -> D
B -> E
D -> E
'''


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


MONKEY_AND_BANANAS_DATA = '''
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
climbdown(box).
'''



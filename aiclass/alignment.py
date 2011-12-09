#!/usr/bin  /python
# -*- coding: iso-8859-1 -*-
import pdb 

class Alignment(object):

    def __init__(self):
        A = 'RBRBRB'
        B = 'BRBRBR'        
        Occupy = 1
        Dismatch = 20
        Match = 0
        self.Costs = []
        self.set_value(A,B)
        self.set_cost(Match,Occupy,Dismatch)        
        
    def set_value(self,A,B):    
        self.A = A
        self.B = B
        self.len = (len (A),len(B))
        self.Costs = [ [{'path':(0,0) , 'value' : None ,'Type':None}  for j in range(0,self.len[0]+1)] for i in range(0,self.len[1]+1) ]
                 
            
    def set_cost(self,Match,Occupy,Dismatch):
        self.Match = Match
        self.Occupy = Occupy
        self.Dismatch = Dismatch
        
    def InBoundary(self,x,y):
        return (x>-1) and (y>-1)
        
    def _CalCost(self,x,y,Type):
        if Type == (1,1):
            if  self.A[x] == self.B[y] :
                return {'type':(Type,'Match'),'value':0}
            else:
                return {'type':(Type,'Dismatch'),'value':self.Dismatch}
        else:
            return {'type':(Type,'Occupy'),'value':self.Occupy}
    
    def CalCost(self,i,j,Match):
        if self.InBoundary(i,j) :
            dict = self._CalCost(i,j,Match)
            return {'path':(i,j),'value':self.Costs[i][j]['value'] + dict['value'],'type':dict['type']}
        else:
            return None
                 
    def run(self):
        for i in range(0,self.len[0]+1 ):
            for j in range(0,self.len[1]+1):
                if (i==j==0):
                    self.Costs[i][j] = {'path':(i,j),'value':0,'type':(None,'None')}
                    continue
                s = []
                s.append(self.CalCost(i-1,j-1,(1,1)))
                s.append(self.CalCost(i-1,j,(0,1)))
                s.append(self.CalCost(i,j-1,(1,0)))
                self.Costs[i][j] = min(filter(lambda x: x !=None,s),key=lambda x:x['value'])       

    def output(self):                    
        i,j = self.len
        print "L:%s" % self.A
        print "R:%s" % self.B
        print "Total Cost: %d " % self.Costs[i][j]['value']        
        OutPut = []
        while True:
            # print "L->[Matched:%d Cur:%s] R->[Matched:%d Cur:%s]  MatchType: %8s  Cost: %d " % (i,self.A[i-1],j,self.B[j-1],self.Costs[i][j]['type'][1],self.Costs[i][j]['value'])
            OutPut.append( self.Costs[i][j]['type'][0])
            i,j = self.Costs[i][j]['path']
            if (i==j==0 ): break
        temp = []
        t= [0,0]
        print "Match Result"
        for i,j in OutPut :            
            if i == 0:
                temp.append((" ",self.B[t[1]]))                                
            elif j==0:
                temp.append((self.A[t[0]]," "))                                
            else:
                temp.append((self.A[t[0]],self.B[t[1]]))
            t[0] = t[0] + i
            t[1] = t[1] + j
                
        print ''.join(a for (a, b) in temp)
        print ''.join(b for (a, b) in temp)        
        
if __name__ == '__main__': 
    AL = Alignment()
    # pdb.set_trace()
    AL.run()
    AL.output()

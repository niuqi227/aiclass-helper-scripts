#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import pdb

class VisionBasic(object):

    def __init__(self):
        self.dict = {'x':0,'X':0,'Z':0,'f':0}
        self.init = False
      
    def set_value(self,dict):  
        self.dict = dict 
        self.init = True

    def  ask(self):        
        if  self.init == False :
            print ' please call set_value to set initial value !!'
            return -1    
        print "\nResults:  "
        for k,v in self.dict.items() :                 
            if v == 0 :
                print "%s = %d " % ( k , self.cal(k) )
            else:
                print "%s = %d " % ( k , v )
        print " ------------------------------------ \n"
           
    def cal(self,m):
        ''' Z*dx == f*B '''
        result = {
            'x': lambda q:(q['f']  * q['X']) / q['Z'],
            'X': lambda q:(q['x']  * q['Z']) / q['f'],
            'f': lambda q:(q['x']  * q['Z']) / q['X'],
            'Z': lambda q:(q['f']  * q['X']) / q['x'],
            'self': lambda q: q,
        }
        return result[m](self.dict)  
    
if __name__ == '__main__': 
    VI = VisionBasic()
    while (True):
        x = input ("input x,X,f,Z    enter 0 for Unkown :\n x=?:\n")
        X = input (" X=?:\n")
        f = input (" f=?:\n")
        Z = input (" Z=?:\n")
        VI.set_value({'x':x,'X':X,'f':f,'Z':Z})
        VI.ask()


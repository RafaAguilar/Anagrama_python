'''
Created on 04/09/2012

@author: rafa
'''
#from threading import Semaphore
#import thread
#import threading
import multiprocessing


import Bot
import itertools

import time


class Master(object):
    '''
    classdocs
    '''


    def __init__(self,base):
        '''
        Constructor
        '''
        self.K=4 #Cantidad de bots(cpu's)
                
        self.base=base
        self.intentos=set()
        self.resultados=set()
        self.dicc=open("diccionario_venezuela")
        #self.dicc=open("alternativo")
        self.diccL=list()
        for i in range(0,71937):
        #for i in range(0,15):
            self.diccL.append(self.dicc.readline().strip())
        
        #self.lockM=thread.allocate_lock() #consola
        self.lockM=multiprocessing.Lock()
        #self.lockD=thread.allocate_lock()
        #self.lockP=thread.allocate_lock()
        #self.botsS=Semaphore(self.K)
        self.botsS=multiprocessing.Semaphore(self.K)
        self.permutaciones=list(itertools.permutations(self.base))
        
        self.bots=list()
        
        #self.local = threading.local()  
        #self.local.diccL = self.diccL  
        
    def crearBot(self,i,i2):
        self.lockD.acquire()
        bot=self.bots.pop()
        self.lockD.release()
        #print "crea Bot"
        self.lockP.acquire()          
        #bot=Bot.Bot("bot"+str(i),self.diccL,,self)
        bot.intento=self.permutaciones.pop()
        self.lockP.release()
        #print self.diccL
        #print "creo bot exitosamente"
        bot.buscar()
        
        self.lockD.acquire()
        self.bots.insert(0,bot)
        self.lockD.release()
        
        #print "Sale de buscar"
        #if (bot.buscar()):
        #    print bot.nombre+" encontro algo en " + str(time.time()-inicio)+" segs."
        #else:
        #    print bot.nombre+" no encontro nada en " + str(time.time()-inicio)+" segs."
        
        self.botsS.release()
    def alternativo(self):
        inicio=time.time()
        print "iniciar"
        
        hilo=[]
        for i in range(0,self.K):
            self.botsS.acquire()
        for i in range(0,self.K):
            self.lockM.acquire()
            print "Bot"+str(i)+": Saliendo"
            self.lockM.release() 
            #b=Bot.Bot("bot"+str(i),self.diccL,self.permutaciones.__getslice__(i*(self.permutaciones.__len__()/self.K),(self.permutaciones.__len__()/self.K)*(i+1)),self)
            
            ini=i*(self.permutaciones.__len__()/self.K)
            fini=(self.permutaciones.__len__()/self.K)*(i+1)
            
            b=Bot.Bot("bot"+str(i),self.diccL,self.permutaciones[ini:fini].__iter__(),self)
            #thread.start_new_thread(b.buscarAlt,(b.buscarAlt,("2","2")))
            b.start()
            
            #hilo.append(multiprocessing.Process(b.buscarAlt()))
            #hilo[i].start
            #hilo[i].join()
        #for i in range (0,self.K):
            
        self.lockM.acquire()
        print "todos los bots despachados"
        self.lockM.release()
        for i in range(0,self.K):
            self.botsS.acquire()
        self.lockM.acquire()
        print "termino"
        print (time.time() - inicio)
        self.lockM.release()
        self.botsS.release()
        
        
    def quedan(self):
        #self.lockP.acquire()
        if self.permutaciones.__len__()>1:
            return True
        #self.lockP.release()
    def iniciar(self):
        i=1
        inicio=time.time()
        print "iniciar"
        #print self.permutaciones
        while (self.quedan()):
            self.botsS.acquire()
            i=i+1
            #sthread.start_new_thread(self.crearBot,(i,i))
        print "termino"
        print (time.time() - inicio)*1000
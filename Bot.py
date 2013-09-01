'''
Created on 04/09/2012

@author: rafa
'''
#import threading
from multiprocessing import Process

class Bot(Process):
    '''
    classdocs
    '''

    def __init__(self,nombre,diccL,intento,master):
        #threading.Thread.__init__(self)
        Process.__init__(self) 
        self.nombre=nombre
        self.diccL=diccL
        self.intento=intento
        #self.ini=ini
        #self.fini=fini        
        
        self.master=master
        self.lockM=self.master.lockM
    def buscarAlt(self):
        #self.master.lockM.acquire()
        #print self.intento.__len__()
        #self.master.lockM.release()
        #for inten in self.intento:
        while (self.intento.__length_hint__()>0):
            inten=self.intento.next()
            inten=inten.__str__().replace('\'','').replace(',','').replace(' ','').strip('()').strip()
            
            #self.master.lockM.acquire()
            
            #print self.nombre+":"+inten
            #print inten
            #self.master.lockM.release()
            for palabra in self.diccL:
                if palabra==(inten):
                    self.master.lockM.acquire()
                    print "Anagrama-> " + self.nombre+":"+palabra
                    self.master.lockM.release()
            del inten        
        self.master.lockM.acquire()
            
        print self.nombre+":Finalize"
        
        self.master.lockM.release()
        
        self.master.botsS.release()
               
    def buscar(self):
        consiguio=False
        
        #print "Empieza a buscar"
        #sprint self.intento
        intento=self.intento.__str__().replace('\'','').replace(',','').replace(' ','').strip('()').strip()
        #self.master.lockM.acquire()
        #print self.nombre + ":" + intento
        #self.master.lockM.release()
        for palabra in self.diccL:                        
            #print palabra + ":" + intento
            if palabra==intento:
                print "Anagrama-> " + self.nombre+":"+palabra
                consiguio=True
                #self.master.guardaCoincidencia(palabra)
            
        return consiguio
    
    
    def pedirIntento(self):
        self.intento = self.master.genIntento()
        
    def run(self):
        self.buscarAlt()
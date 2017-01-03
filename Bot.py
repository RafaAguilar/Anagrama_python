'''
Created on 04/09/2012

@author: rafa
'''
import copy
from multiprocessing import Process


class Bot(Process):
    '''
    classdocs
    '''

    def __init__(self, nombre, diccL, intento, master):
        Process.__init__(self)
        self.nombre = nombre
        self.diccL = diccL
        self.intento = intento
        self.master = master
        self.lockM = self.master.lockM

    def buscarAlt(self):
        first = True
        i = 0
        try:
            while (True):
                i += 1
                inten = self.intento.__next__()
                if first:
                    #print('{}: Nuevo slice desde {}'.format(self.name, ''.join(inten)))
                    first = False
                if ''.join(inten) == "luciernaga":
                        print(''.join(inten).strip())
                intent = ''.join(inten)
                #for palabra in self.diccL:
                if intent in self.diccL:
                    self.master.lockM.acquire()
                    print("Anagrama-> " + self.nombre + ":" + intent + ' en el intento {}'.format(i))
                    self.master.lockM.release()
                del inten
        except StopIteration:
            pass
        self.master.lockM.acquire()
        print(self.nombre + ":Finalize")
        self.master.lockM.release()
        self.master.botsS.release()

    def buscar(self):
        consiguio = False
        intento = self.intento.__str__().replace('\'', '').replace(
            ',', '').replace(' ', '').strip('()').strip()
        for palabra in self.diccL:
            if palabra == intento:
                print("Anagrama-> " + self.nombre + ":" + palabra)
                consiguio = True
        return consiguio

    def pedirIntento(self):
        self.intento = self.master.genIntento()

    def run(self):
        self.buscarAlt()

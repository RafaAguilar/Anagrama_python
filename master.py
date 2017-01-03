'''
Created on 04/09/2012

@author: rafa
'''
import multiprocessing
import operator
from collections import Counter
from math import factorial
from functools import reduce

import Bot
import itertools

import time


def npermutations(l):
    return factorial(len(l))


class Master(object):
    '''
    classdocs
    '''

    def __init__(self, base):
        '''
        Constructor
        '''
        self.cores = 4
        self.base = base
        self.intentos = set()
        self.resultados = set()
        self.dicc = open("diccionario_venezuela")
        self.diccL = set()
        for i in range(0, 71937):
            self.diccL.add(self.dicc.readline().strip())
        self.lockM = multiprocessing.Lock()
        self.botsS = multiprocessing.Semaphore(self.cores)
        self.permutaciones = itertools.permutations(self.base)
        self.lenght = int(npermutations(base))
        self.bots = list()

    def crearBot(self, i, i2):
        self.lockD.acquire()
        bot = self.bots.pop()
        self.lockD.release()
        self.lockP.acquire()
        bot.intento = self.permutaciones.pop()
        self.lockP.release()
        bot.buscar()
        self.lockD.acquire()
        self.bots.insert(0, bot)
        self.lockD.release()
        self.botsS.release()

    def alternativo(self):
        inicio = time.time()
        print("iniciar")
        hilo = []
        for i in range(0, self.cores):
            self.botsS.acquire()
        for i in range(0, self.cores):
            self.lockM.acquire()
            print("Bot" + str(i) + ": Saliendo")
            self.lockM.release()
            ini = int((i * self.lenght) / self.cores)
            fini = int((self.lenght / self.cores) * (i + 1))
            #print(ini, fini, fini - ini, self.lenght)
            b = Bot.Bot("bot" + str(i), self.diccL,
                        itertools.islice(self.permutaciones, ini, fini), self)
            b.start()

        self.lockM.acquire()
        print("todos los bots despachados")
        self.lockM.release()
        for i in range(0, self.cores):
            self.botsS.acquire()
        self.lockM.acquire()
        print("termino")
        print (time.time() - inicio)
        self.lockM.release()
        self.botsS.release()

    def quedan(self):
        if self.permutaciones.__len__() > 1:
            return True

    def iniciar(self):
        i = 1
        inicio = time.time()
        print("iniciar")
        while (self.quedan()):
            self.botsS.acquire()
            i = i + 1
        print("termino")
        print((time.time() - inicio) * 1000)

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


import itertools

# Unique permutations algorithms http://stackoverflow.com/a/6571976/2399397

def cmp(a, b):
    return (a > b) - (a < b)

def next_permutationS(l):
    '''Changes a list to its next permutation, in place.
    Returns true unless wrapped around so result is lexicographically smaller. '''
    n = len(l)
    #Step 1: Find tail
    last = n-1 #tail is from `last` to end
    while last>0:
        if l[last-1] < l[last]: break
        last -= 1
    #Step 2: Increase the number just before tail
    if last>0:
        small = l[last-1]
        big = n-1
        while l[big] <= small: big -= 1
        l[last-1], l[big] = l[big], small
    #Step 3: Reverse tail
    i = last
    j = n-1
    while i < j:
        l[i], l[j] = l[j], l[i]
        i += 1
        j -= 1
    return last>0

def next_permutationB(seq, pred=cmp):
    """
    This function is taken from this blog post:
    http://blog.bjrn.se/2008/04/lexicographic-permutations-using.html

    Like C++ std::next_permutation() but implemented as
    generator. Yields copies of seq."""
    def reverse(seq, start, end):
        # seq = seq[:start] + reversed(seq[start:end]) + \
        #       seq[end:]
        end -= 1
        if end <= start:
            return
        while True:
            seq[start], seq[end] = seq[end], seq[start]
            if start == end or start+1 == end:
                return
            start += 1
            end -= 1
    if not seq:
        raise StopIteration
    try:
        seq[0]
    except TypeError:
        raise TypeError("seq must allow random access.")
    first = 0
    last = len(seq)
    seq = seq[:]
    # Yield input sequence as the STL version is often
    # used inside do {} while.
    yield seq
    if last == 1:
        raise StopIteration
    while True:
        next = last - 1
        while True:
            # Step 1.
            next1 = next
            next -= 1
            if pred(seq[next], seq[next1]) < 0:
                # Step 2.
                mid = last - 1
                while not (pred(seq[next], seq[mid]) < 0):
                    mid -= 1
                seq[next], seq[mid] = seq[mid], seq[next]
                # Step 3.
                reverse(seq, next1, last)
                # Change to yield references to get rid of
                # (at worst) |seq|! copy operations.
                yield seq[:]
                break
            if next == first:
                raise StopIteration
    raise StopIteration

def unique(iterable):
    seen = set()
    for x in iterable:
        if x in seen: continue
        seen.add(x)
        yield x

def npermutations(word):
    # How to calculate unique permutations of a word http://math.stackexchange.com/a/391835
    letters = {}
    for letter in word:
        try:
            letters[letter] += 1
        except KeyError:
            letters[letter] = 1
    divisor = 1
    for k, v in letters.items():
        if v > 1:
            divisor *= factorial(v)
    return factorial(len(word)) / divisor

class Master(object):
    '''
    classdocs
    '''

    def __init__(self, base):
        '''
        Constructor
        '''
        self.cores = 8
        self.base = base
        self.intentos = set()
        self.resultados = set()
        self.dicc = open("diccionario_venezuela")
        #self.dicc = open("alternativo")
        self.diccL = set()
        for i in range(0, 71937):
            self.diccL.add(self.dicc.readline().strip())
        self.lockM = multiprocessing.Lock()
        self.botsS = multiprocessing.Semaphore(self.cores)
        self.permutaciones = next_permutationB(list(self.base))
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

import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer


class Node:
    def __init__(self, id):
        self.id = id
        self.d = 0
        self.f = 0
        self.color = None


class Graph:

    def __init__(self, n, prob):
        self.A = np.zeros((n, n), dtype=int)
        self.nodes = []
        self.order = []
        self.SCC = []
        self.SCCcounter = 0
        self.time = 0
        for i in range(n):
            for j in range(n):
                if np.random.random() > 1 - prob:
                    self.A[i, j] = 1
        for i in range(n):
            node = Node(i)
            self.nodes.append(node)


def DFS(G):
    for u in G.nodes:
        u.color = "White"
    G.time = 0
    for u in G.nodes:
        if u.color is "White":
            DFS_visit(G, u)
    G.order.reverse()


def DFS_visit(G, u):
    G.time += 1
    u.d = G.time
    u.color = "Grey"
    for v in G.nodes:
        if G.A[u.id, v.id] == 1 and v.color is "White":
            DFS_visit(G, v)
            G.order.append(v)
            G.SCC.append(v.id)
    u.color = "Black"
    G.time += 1
    u.f = G.time


def SCC(G):
    DFS(G)
    for u in G.nodes:
        u.color = "White"
    G.time = 0
    Gt = G
    Gt.A = np.transpose(G.A)
    for u in G.order:
        if u.color is "White":
            G.SCC = []
            DFS_visit(Gt, u)
            G.SCC.append(u.id)
            G.SCCcounter += 1
            # print()
            # print("componente fortemente connessa , elementi:   ")
            # for i in range(len(G.SCC)):
            #   print(G.SCC[i])

    G.order = []


def testProb():
    nsamples = 10
    size = 100
    totAvgTimes = []
    totSCCount = []
    prob = np.arange(0, 1, 0.01)
    for i in prob:
        avgTime = 0
        SCCount = 0
        for j in range(nsamples):
            G = Graph(size, i)
            start = timer()
            SCC(G)
            avgTime += timer() - start
            SCCount += G.SCCcounter
        totSCCount.append(SCCount / nsamples)
        totAvgTimes.append(avgTime / nsamples * 1000)
    plt.plot(prob, totSCCount)
    plt.xlabel("Probabilità")
    plt.ylabel("Numero di SCC")
    plt.show()
    plt.plot(prob, totAvgTimes)
    plt.xlabel("Probabilità")
    plt.ylabel("tempo impiegato im ms")
    plt.show()


def testSize():
    nsamples = 50
    size = np.arange(20, 220, 20)
    totAvgTimes = []
    totSCCount = []
    prob = 0.1
    for i in size:
        avgTime = 0
        SCCount = 0
        for j in range(nsamples):
            G = Graph(i, prob)
            start = timer()
            SCC(G)
            avgTime += timer() - start
            SCCount += G.SCCcounter
        totSCCount.append(SCCount / nsamples)
        totAvgTimes.append(avgTime / nsamples * 1000)
    plt.plot(size, totSCCount)
    plt.xlabel("Size")
    plt.ylabel("Numero SCC")
    plt.show()
    plt.plot(size, totAvgTimes)
    plt.xlabel("Size")
    plt.ylabel("tempo impiegato im ms")
    plt.show()


def main():
    testProb()
    testSize()

if __name__ == '__main__':
    main()
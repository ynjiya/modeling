import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

PRECISION = 1e-5
TIME_DELTA = 5
GRAPH_OX = 1.5


def repeated_mult(tm, n):
    tm_n = tm
    stable_time = [0 for i in range(n)]
    probs = [[] for i in range(n)]
    max_stable_time = -1

    i = 0
    while i != int(max_stable_time*GRAPH_OX) or not all(s != 0 for s in stable_time):
        cur_tm = np.matmul(tm_n, tm)

        for state in range(n):
            probs[state].append(tm_n[0][state])
            if stable_time[state]==0 and abs(cur_tm[0][state] - tm_n[0][state]) < PRECISION:
                stable_time[state] = i
                if i > max_stable_time:
                    max_stable_time = i     
        tm_n = cur_tm
        i += 1
    return tm_n[0], probs, stable_time


def left_eigenvector(tm, n):
    start_state = 0
    pi = np.array([0 for i in range(n)])
    pi[start_state] = 1
    max_stable_time = -1
    pi_n = pi
    stable_time = [0 for i in range(n)]
    probs = [[] for i in range(n)]

    i = 0
    while not all(s != 0 for s in stable_time) or i != int(max_stable_time*GRAPH_OX):
        cur_pi = np.matmul(pi_n, tm)

        for state in range(n):
            probs[state].append(pi_n[state])
            if stable_time[state]==0 and abs(cur_pi[state] - pi_n[state]) < PRECISION:
                stable_time[state] = i
                if i > max_stable_time:
                    max_stable_time = i 
        i += 1
        pi_n = cur_pi
    return cur_pi, probs, stable_time



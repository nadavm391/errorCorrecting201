#!/usr/bin/env sage

from math import sqrt
from Field import wrap
from sage.all import *
import sys


def decode_msg(xValues, encodedMsg, q, n, k):
    degX = int(sqrt(n * k));
    degY = int(sqrt(n / k))
    matrix = []
    for i in range(n):
        matrix.append(get_matrx_row(xValues[i], encodedMsg[i], degX, degY, q))
    A = Matrix(GF(q), matrix)
    Qopts = A.right_kernel()
    R = GF(q)['x, y'].gens()
    Q = buildQ(R, Qopts, q, degX, degY)
    print("Q(x,y)=" + str(Q))
    factors = Q.factor()
    print("factors(without constants) - ")
    i = 1
    for q in factors:
        print("Q" + str(i) + "- " + str(q[0]))
        i = i + 1
    correctfactors = findCorrectFactors(factors, k, R)
    print("factors with the correct form -")
    for factor in correctfactors:
        print(factor)
    for i in range(len(correctfactors)):
        correctfactors[i]=-1 * correctfactors[i].coefficient({R[1]: 0})
    return correctfactors


def get_matrx_row(xValue, Yvalue, degX, degY, q):
    matrixRow = []
    for i in range(degX + 1):
        for j in range(degY + 1):
            matrixRow.append(wrap((xValue ** i) * (Yvalue ** j), q))
    return matrixRow


def buildQ(R, Qopts, q, degX, degY):
    QcoEfficients = list(Qopts[1])
    f = 0
    for i in range(degX + 1):
        for j in range(degY + 1):
            f = f + QcoEfficients[i * (degY + 1) + j] * (R[0] ** i) * (R[1] ** j)
    return f


def findCorrectFactors(factors, k, R):
    correctfactorsList = []
    for factor in factors:
        if (factor[0].degree(R[1]) == 1) and (factor[0].degree(R[0]) == (k - 1)):
            correctfactorsList.append(factor[0])
    if len(correctfactorsList) == 0:
        print("algorithm failed!")
        sys.exit(0)
    return correctfactorsList

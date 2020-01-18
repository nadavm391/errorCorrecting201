import Encoder
import Decoder
#!/usr/bin/env sage

import sys
from sage.all import *
from math import sqrt,floor
from sympy import nextprime
import random
import sys

def reed_solomon(kcoefficients, e, n, q, k ):
    (alphaValues, encodedMsg) = Encoder.encode_msg(kcoefficients, n, q)
    print("encoded msg -" + str(encodedMsg))
    indexes = inject_errors(encodedMsg, n, k, q, e)
    print("encoded msg with errors -" + str(encodedMsg))
    print("error indices -" + str(indexes))
    results = Decoder.decode_msg(alphaValues, encodedMsg, q, n, k)
    reconstructedlist=[]
    for result in results:
        coefficentList= result.coefficients()
        coefficentList.reverse()
        chars=list(map(chr,coefficentList))
        reconstructed=""
        for x in chars:
            reconstructed+=x
        reconstructedlist.append(reconstructed)
    return reconstructedlist


def inject_errors(encodedMsg,n,k,q,error_numIn):
    error_num = error_numIn
    print("number of errors the algorithm can 'officialy' handle - " + str(int(n-(2*sqrt(n*k)))))
    print("number of errors we're injecting - " + str(error_num))
    error_count=0
    error_idx_list=[]
    error_idx = random.randint(0, n - 1)
    while error_count<error_num:
        while error_idx in error_idx_list:
            #print(error_idx_list)
            #print(error_idx)
            error_idx = random.randint(0,n-1)
        error = random.randint(0,q-1)
        while encodedMsg[error_idx]==error:
            error = random.randint(0, q - 1)
        encodedMsg[error_idx] = error
        error_count = error_count+1
        error_idx_list.append(error_idx)
    error_idx_list.sort()
    return error_idx_list

def calculate_n(k, e):
    return int(e+2*k+(sqrt(4*((e+2*k)**2)+4*(e**2)))/2)
def calculate_q(n,kcoefficients):
    maxK = max(kcoefficients)
    maximum = max(n, maxK)
    q = nextprime(maximum)
    return q

print("original msg - " + sys.argv[1])
L = list(sys.argv[1])
kcoefficients = list(map(ord, L))
k = len(kcoefficients)
e = int(sys.argv[2])
n = int(sys.argv[3])
q = int(sys.argv[4])
if e==0:
    if n==0:
        print ("Error - e can't be calculated without n!")
        sys.exit(0)
    e = int(n-(2*sqrt(n*k)))
if n==0:
    if e==0:
        print("Error - n can't be calculated without e!")
        sys.exit(0)
    n = calculate_n(k, e)
if q==0:
    q = calculate_q(n, kcoefficients)

print("running reed solomon with parameters msgCoefficients:" + str(kcoefficients) +
      ", n: % 2d , k: % 2d, error: % 2d, field: % 2d" %(n, k, e, q))
results = reed_solomon(kcoefficients, e, n, q, k)
print("after reconstructing the msg the list is:")
print(results)


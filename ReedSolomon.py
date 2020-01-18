import Encoder
import Decoder
#!/usr/bin/env sage

import sys
from sage.all import *
from math import sqrt,floor
import random
import sys

def reed_solomon(kcoefficients, n, q , e):
    (alphaValues, encodedMsg) = Encoder.encode_msg(kcoefficients, n, q)
    k = len(kcoefficients)
    print("encoded msg -" + str(encodedMsg))
    calculate=False
    if e==0:
        calculate = True
    indexes = inject_errors(encodedMsg, n, k, q, e, calculate)
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


def inject_errors(encodedMsg,n,k,q,error_numIn,calculate):
    if calculate:
        error_num = int(n-(2*sqrt(n*k)))
    else:
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

print("original msg - " + sys.argv[1])
L = list(sys.argv[1])
kcoefficients = list(map(ord, L))
results = reed_solomon(kcoefficients, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
#results = reed_solomon("Alice&Bob", 45, 929, 6)
print("after reconstructing the msg the list is:")
print(results)


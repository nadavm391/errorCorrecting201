import numpy.polynomial.polynomial as np
import sympy as S

field = 0

def wrap(x):
    return x % field


def encode_msg(kcoefficients, n):
    alphaValues = []
    encodedMsg = []
    k = len(kcoefficients)
    p = np.Polynomial(kcoefficients)
    for i in range(n):
        alphaValues.append(i)
    for i in range(n):
        curr = 0
        for j in range(k):
            curr = wrap(curr+wrap(wrap((i**j))*kcoefficients[j]))
        encodedMsg.append(curr)
    return alphaValues, encodedMsg


msg = "Test"
field = 151
L = list(msg)
kcoefficients = list(map(ord, L))
print(kcoefficients)
kcoefficients = list(map(wrap, kcoefficients))
(alphaValues, encodedMsg) = encode_msg(kcoefficients, 20)
print(encodedMsg)

import numpy.polynomial.polynomial as np
from Field import wrap



def encode_msg(kcoefficients, n, q):
    alphaValues = []
    encodedMsg = []
    k = len(kcoefficients)
    p = np.Polynomial(kcoefficients)
    for i in range(n):
        alphaValues.append(i)
    for i in range(n):
        curr = 0
        for j in range(k):
            curr = wrap(curr + (i ** j) * kcoefficients[j], q)
        encodedMsg.append(curr)
    return alphaValues, encodedMsg


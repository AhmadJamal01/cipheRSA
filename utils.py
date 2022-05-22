import numpy as np
import random
import time
import matplotlib.pyplot as plt
import math


def GCD(a, b):
    if b == 0:
        return a
    return GCD(b, a % b)


def extendedEuclid(a, b):
    if b == 0:
        return (1, 0)
    (x, y) = extendedEuclid(b, a % b)
    k = a // b
    return (y, x - k * y)


def modularExponentiate(a, n, mod):
    if n == 0:
        return 1 % mod
    elif n == 1:
        return a % mod
    f = 1
    binaryB = bin(n)[2:]
    for i in range(len(binaryB)):
        f = (f*f) % mod
        if binaryB[i] == '1':
            f = (f * a) % mod
    return f


def modularInverse(a, n):
    (b, x) = extendedEuclid(a, n)
    if b < 0:
        b = (b % n + n) % n
    return b


def ConvertToInt(message_str):
    res = 0
    for i in range(len(message_str)):
        res = res * 256 + ord(message_str[i])
    return res


def ConvertToStr(n):
    res = ""
    while n > 0:
        res += chr(n % 256)
        n //= 256
    return res[::-1]


def Encrypt(m, e, n):
    m = ConvertToInt(m)
    c = modularExponentiate(m, e, n)
    return c


def Decrypt(c, d, p, q):
    m = modularExponentiate(c, d, p * q)
    m = ConvertToStr(m)
    return m


def divideMsg(msg, n):
    msg_blocks = []
    begin = 0
    msg_len = len(msg)
    step = math.floor(math.log(n, 256))
    if(msg_len > math.log(n, 256)):  # need to divide
        for start in range(begin, len(msg), step):
            if(start + step > len(msg)-1):
                msg_blocks.append(msg[start:])
            else:
                msg_blocks.append(msg[start:start+step])
    else:
        msg_blocks = msg
    return msg_blocks


def encryptEncompass(msg, exponent, modulo):
    msg_blocks = divideMsg(msg, modulo)
    cipher_blocks = [Encrypt(chunk, exponent, modulo) for chunk in msg_blocks]
    return cipher_blocks


def decryptEncompass(cipher_blocks, d, p, q):
    message = [Decrypt(chunk, d, p, q) for chunk in cipher_blocks]
    message = "".join(message)
    return message


def getPublicKey(phi_n):
    e = random.randrange(1, phi_n)
    while e < 1 or GCD(e, phi_n) != 1:
        e = random.randrange(1, phi_n)
    return e


def getPrivateKey(e, p, q):
    phi_n = (p - 1) * (q - 1)
    d = modularInverse(e, phi_n)
    return d


def nBitRandom(n):
    return random.getrandbits(n) + (2**(n-1)+1)


def fermatPrimalityTest(p):
    """
    a:random integer
    p:the number to test if prime or not
    """
    if p <= 1:
        return False
    for _ in range(1, 102):
        # a=np.random.randint(1,p,dtype=np.int64)
        a = random.randint(1, p+1)
        aPowP = modularExponentiate(a, p, p)
        if (aPowP - a) % p != 0:
            return False
    return True


def generatePrime(n):
    if n == 1:
        return -1
    number = 1
    while not fermatPrimalityTest(number):
        number = nBitRandom(n)
    return number


def generatePrimeModuli(n):
    p = 1
    q = 1
    nArray = []
    for i in range(2, int(n/2)+1):
        # for _ in range(2):
        # while (not fermatPrimalityTest(p)):
        #     p = nBitRandom(i)
        # while (not fermatPrimalityTest(q)):
        #     q = nBitRandom(i)
        p = generatePrime(i)
        q = generatePrime(i)
        while p == q:
            q = generatePrime(i)
        nArray.append(p*q)
    return nArray

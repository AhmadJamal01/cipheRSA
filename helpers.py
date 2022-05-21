import sys, threading
import numpy as np
import random
import math
from ast import literal_eval
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
        b = (b % n + n) % n  # we don't want -ve integers
    return b

#TODO: change the implementation
#look up ways to change strings to ints for encryption
def ConvertToInt(message_str):  
    res = 0
    for i in range(len(message_str)):
        res = res * 256 + ord(message_str[i])
    return res

#TODO: change the implementation
#look up ways to change strings to ints for encryption
def ConvertToStr(n):
    res = ""
    while n > 0:
        res += chr(n % 256)
        n //= 256
    return res[::-1]

def getPrivateKey(e,p,q):
    phi_n = (p - 1) * (q - 1)
    d = modularInverse(e, phi_n)
    return d


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

def Encrypt(m, e, n):
    msg_blocks = divideMsg(m, n)
    msg_blocks_in_int = [ConvertToInt(block) for block in msg_blocks]
    c = [modularExponentiate(block, e, n) for block in msg_blocks_in_int]
    return c

def Decrypt(c, d, p, q):
    decrypted_blocks = [modularExponentiate(block, d, p * q) for block in c]
    m = [ConvertToStr(block) for block in decrypted_blocks]
    m = "".join(m)
    return m

def nBitRandom(n):
    return random.getrandbits(n) + (2**(n-1)+1)

def fermatPrimalityTest(p):
    """
    a:random integer
    p:the number to test if prime or not
    """
    if p <= 1: return False
    for _ in range(1,102):
        # a=np.random.randint(1,p,dtype=np.int64)
        a=random.randint(1,p+1)
        aPowP = modularExponentiate(a,p,p)
        if (aPowP - a) % p != 0: return False
    return True

def  testexponent(e,p,q):
    phi_n = (p - 1) * (q - 1)
    if e > phi_n or e < 1:
        return False
    if GCD(e,phi_n) != 1:
        return False
    return True

# c = Encrypt("hello",7,367*373)
# print(Decrypt(c , 19556 , 367 , 373))


def use_encrypt(msg ,exponent  ,n):
    msg_chunks = divideMsg(msg,n)
    cipher = [Encrypt(msg,exponent,n) for msg in msg_chunks]
    return cipher
def use_decrypt(c, d ,p ,q):
    message = [Decrypt(chunk,d,p,q) for chunk in c]
    message = "".join(message)
    return message

def convrt(inp):
    lis = literal_eval(inp)
    print(lis)

convrt("[[80532, 46558], [77326, 46558]]")


def generatePrime(n):
    if n == 1: return -1
    number = 1 
    while not fermatPrimalityTest(number):
        number = nBitRandom(n)
    return number
import numpy as np
import const_variables as var
import math
import random
import re

m = var.m
n = var.n
q = var.q
t = var.t
ρq = var.ρq


class Apon:

    # Generate random number(pseudo) in the bit width of "bits"
    def generate_random(self, bits):
        a = 0
        for i in range(bits):
            a = 2 * a + np.random.choice([0, 1])
        return a;

    def Enc(self, r, s):
        B = np.random.randint(-q / 2, q / 2, (m, n))
        variance = ρq * ρq / (2 * math.pi)  # 误差向量正态分布方差
        e = np.random.normal(loc=0.0, scale=variance, size=(m, 1))  # 生成随机正态分布数。
        # e = np.random.randint(-q/2, q/2, (m, 1))

        h = np.matmul(B, s) + e + q / 2 * r
        return B, h

    def Dec(self, B, h, s):
        temp = h - np.matmul(B, s)
        r = np.zeros((m, 1))
        for i in range(m):
            if (temp[i, 0] >= 3 * q / 8 and temp[i, 0] <= 5 * q / 8):
                r[i, 0] = 1
            else:
                r[i, 0] = 0
        return r

    # Generate Procedure
    def Gen(self, w):

        A = np.random.randint(-q / 2, q / 2, (m, n))
        s = np.random.randint(-q / 2, q / 2, (n, 1))
        # b = As + w
        c = np.matmul(A, s) + w
        r = np.random.randint(0, 2, (m, 1))
        B, h = self.Enc(r,s)

        pub = []
        pub.append(A)
        pub.append(c)
        pub.append(B)
        pub.append(h)
       # self.pub = pub
        return r, pub

    def Decode(self, A, b):
        seq = []
        for i in range(m):
            seq.append(i)
        limit = var.limit

        while limit > 0:
            tempI = random.sample(seq, n)
            tempA = A[tempI]  # A'

            if (np.linalg.matrix_rank(tempA) == n):
                tempb = b[tempI]  # b'
                temps = np.around(np.matmul(np.linalg.inv(tempA), tempb)).astype(int)
                sm = np.matmul(A, temps)
                # If b − As' has ≤ t nonzero coordinates then output s'.
                Y = b - sm
                cnt = 0
                flag = 0
                for i in range(m):
                    if (Y[i, 0] != 0):
                        cnt = cnt + 1
                if (cnt < t):
                    flag = 1
                    break
            limit = limit - 1

        return temps, flag

    def Rep(self, w, pub):
        A = pub[0]
        c = pub[1]
        B = pub[2]
        h = pub[3]

        b = c - w
        s, flag = self.Decode(A, b)
        r = np.zeros((m, 1))
        if (flag == 1):
            r = self.Dec(B, h, s)
        return r, flag

def test_Apon(w1,w2):
    apon = Apon();
    hashr = 0
    p=[]
    for j in range(4):
        r, pub = apon.Gen(w1[j*768 : m+j*768])
        p.append(pub)
        for i in range(m):
            hashr = (hashr * 2 + r[i, 0]) % 10000007
    print(hashr)
    '''r.resize(r.shape[0])
    list_r = r.tolist()
    str1 = "".join('%s' % id for id in list_r)
    res = hex(int(str1, 2))[2:]
    print(res)
    '''

    flag = 1
    hashr = 0

    for j in range(4):
        r, flag = apon.Rep(w2[j*768 : m+j*768] ,p[j])
        if(flag==0):
            break
        for i in range(m):
            hashr = (hashr * 2 + r[i, 0]) % 10000007
    if(flag==0):
        print(0)
    else:
        print(hashr.astype(int))


def get_Source(path='./wwrgray/1.pgm'):
    img = cv2.imread(path, 0)
    res = ""
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            b = bin(img[i][j])[2:]
            for k in range(8-len(b)):
                b = '0'+b
            res = res + b
    fill = 92160 - len(res)
    for i in range(fill):
        res = res + '0'
    list_s = re.findall(r'.{30}', res)

    for i in range(len(list_s)):
        if (list_s[i][0] == "1"):
            list_s[i] = (-1) * int(list_s[i][1:], 2)
        else:
            list_s[i] = int(list_s[i][1:], 2)
    return list_s


img = cv2.imread('./wwrgray/4.pgm', 0)
for i in range(4):
    for j in range(8):
        img[i+15][j]=255
cv2.imwrite('alter.pgm', img);
for i in range(8):
    for j in range(int(img.shape[1]/2)):
        img[i+15][j]=255
cv2.imwrite('alter1.pgm', img);


w1 = get_Source('./wwrgray/4.pgm')
w2 = get_Source('alter1.pgm')

'''
w = np.random.randint(-ρq, ρq, (m, 1))
w1 = w
w2 = w
# Alter the coordinates of w
for i in range(10):
    w2[i, 0] = 0
'''
test_Apon(w1,w2)

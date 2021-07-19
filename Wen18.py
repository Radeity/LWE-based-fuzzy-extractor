import numpy as np
import const_variables as var
import math
import hashlib
import re

m = var.m
n = var.n
q = var.q
ρq = var.ρq
l = var.l
bit_width_x = var.bit_width_x


class WenLWE:

    def toBin(self, string):
        res = ""
        str_zero = "0000"
        for i in range(len(string)):
            temp = int(string[i], 16)
            tbin = bin(temp)[2:]
            tbin = str_zero[len(tbin):] + tbin
            res = res + tbin

        return res

    def Hash(self, w):
        # 特征向量为10个整数，Hash结果为 n * l（256 * 100）的矩阵

        temp = ""
        ori = 1
        salt = []
        for i in range(len(w)):
            ori = (ori * w[i]) % 100000007

            string = str(w[i])
            sha512 = hashlib.sha512()
            sha512.update(string.encode('utf-8'))
            hash_res = sha512.hexdigest()
            temp = temp + hash_res

        salt = re.findall(r'.{6}', temp)    # len(salt) = 213
        temp = ""
        for i in range(len(salt)):
            sha512 = hashlib.sha512()
            sha512.update(salt[i].encode('utf-8'))
            hash_res = sha512.hexdigest()
            temp = temp + self.toBin(hash_res)
        a = len(temp)
        c = int(512 / bit_width_x)
        b = math.ceil(n*l / int(512 / bit_width_x))

        num = int(len(temp) / math.ceil(n*l / int(512 / bit_width_x)))
        salt = re.findall(r'.{'+str(num)+'}', temp)

        temp = ""
        for i in range(b):
            final_salt = hex(int(salt[i],2))[:2]
            sha512 = hashlib.sha512()
            sha512.update((str(ori)+final_salt).encode('utf-8'))
            hash_res = sha512.hexdigest()
            temp = temp + self.toBin(hash_res)

        z = len(temp)
        list_s = re.findall(r'.{'+str(bit_width_x)+'}', temp)
        for i in range(len(list_s)):
            if(list_s[i][0]=="1"): list_s[i] = (-1)*int(list_s[i][1:],2)
            else: list_s[i] = int(list_s[i][1:],2)

        s = np.array(list_s[0:n*l])
        s.resize(n,l)
        return s

    def Gen(self, w):
        s = self.Hash(w)
        #s = np.random.randint(-q / 2, q / 2, (n, l))

        #variance = ρq * ρq / (2 * math.pi)  # 误差向量正态分布方差
        A = np.random.randint(-q/2, q/2, (m,n))
        E = np.random.normal(loc=0.0, scale=0, size=(m,l))
        B = np.hstack((A, np.matmul(A, s)+E))   # 水平拼接
        x = np.random.randint(0, 2, (m, 1))
        m1 = np.random.randint(0, 2, (l, 1))
        c = np.matmul(x.T, B) + np.hstack((np.expand_dims(np.zeros(n),axis=0), m1.T * np.round(q/2)))

        pub = []
        pub.append(c.T)
        #pub.append(s)
        self.pub = pub

        r = m1
        r.resize(r.shape[0])
        list_r = r.tolist()
        str1 = "".join('%s' % id for id in list_r)
        res = hex(int(str1, 2))[2:]

        #print(res)
        return res

    def Rec(self, w1):
        c = self.pub[0]
        s = self.Hash(w1)
        #s = self.pub[1]
        d = np.matmul(c.T, np.vstack((-s, np.identity(l))))

        m = np.zeros((l,1))
        for i in range(l):
            if (d[0, i] >= q / 4 and d[0, i] <= 3 * q / 4):
                m[i, 0] = 1
            else:
                m[i, 0] = 0
        r = m.astype(int)
        r.resize(r.shape[0])
        list_r = r.tolist()
        str1 = "".join('%s' % id for id in list_r)
        res = hex(int(str1, 2))[2:]

        #print(res)
        return res


if __name__ == '__main__':
    w = np.random.randint(0, 10000, (10, 1))
    lwefe = WenLWE()
    res = lwefe.Gen(w)
    print(res)

    r = lwefe.Rec(w)
    r.resize(r.shape[0])
    list_r = r.tolist()
    str1 = "".join('%s' % id for id in list_r)
    res = hex(int(str1, 2))[2:]
    print(res)




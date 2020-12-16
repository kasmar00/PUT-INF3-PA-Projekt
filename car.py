import matplotlib.pyplot as plt
import math

class car:
    def __init__(self, v0, vzad):
        self.Cd = 0.24
        self.rho = 1.225
        self.A = 5.0
        self.Fp = 10000
        self.alfa = 2
        self.g = 9.8
        self.m = 1000
        self.tsim =  1 * 3600
        self.Tp = 0.1
        self.N = int(self.tsim / self.Tp)
        self.kp = 0.0015
        self.Ti = 0.25
        self.Td = 0.01
        self.vzad = vzad
        self.v0 = v0
        self.v = [v0, ]
        self.e = [0.0, ]
        self.u = [0.0, ]
        self.x = [0.0, ]
        self.umin = 0
        self.umax = 1
        self.vmax = 200
        self.vmin = 0
        self.u_pierwotne = [0.0, ]

        # wyznaczenie prostej do obliczania współczynnika % pedału
        self.prosta_a = 1 / self.umax

    def sim(self):
        for i in range(self.N):
            if i % 1000 == 0:
                print(i, '/', self.N)

            e = self.vzad - self.v[-1]
            self.e.append(e)

            u = self.kp*(self.e[-1] + (self.Tp/self.Ti)*sum(self.e) + (self.Td/self.Tp)*(self.e[-1]-self.e[-2]))
            self.u_pierwotne.append(u)
            if u >= self.umax:
                u = self.umax
            elif u <= self.umin:
                u = self.umin
            self.u.append(u)
            self.x.append(self.prosta_a * u)

            v = self.v[-1] + (self.Tp/self.m)*(self.Fp*self.x[-1]-0.5*self.rho*self.A*self.Cd*self.v[-1]*self.v[-1] - self.m*self.g*math.sin(math.radians(self.alfa)))
            if v >= self.vmax:
                v = self.vmax
            if v <= self.vmin:
                v = self.vmin
            self.v.append(v) 

    def plots(self):
        t = [i * self.Tp for i in range(self.N + 1)]

        plt.subplot(3, 1, 1)
        plt.plot(t, self.v, label="v")
        plt.axhline(y=self.vzad, color='r', linestyle='--', label="vzad")
        plt.xlabel("t [s]")
        plt.ylabel("v [m/s^2]")
        plt.xscale('log')
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.plot(t, self.u, label="u")
        plt.plot(t, self.u_pierwotne, label = "u_pierwotne")    
        plt.xlabel("t [s]")
        plt.ylabel("u [V]")
        plt.xscale('log')
        plt.legend()

        plt.subplot(3, 1, 3)
        plt.plot(t, self.x, label="Procent gas")
        plt.xlabel("t [s]")
        plt.xscale('log')
        plt.ylabel("gas [%]")
        plt.legend()


        plt.show()

a = car(20, 70)
a.sim()

print(a.u[:30])
print(a.v[:30])
print(a.e[:30])
print(a.x[:30])

a.plots()

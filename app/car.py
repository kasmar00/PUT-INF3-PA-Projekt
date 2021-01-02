import io
import math
from typing import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
# https://stackoverflow.com/questions/49921721/runtimeerror-main-thread-is-not-in-main-loop-with-matplotlib-and-flask


class Car:
    def __init__(self, v0, vzad):
        # stałe dla regulatora PID
        self.kp: float = 0.0015                 # wzmocznienie regulatora
        self.Td: float = 0.01                   # czas wyprzedzenia [s]
        self.Ti: float = 0.25                   # czas zdwojenia [s]

        self.tsim: float = 1 * 500              # czas symulacji [s]
        self.Tp: float = 0.1                    # czas próbkowania [s]
        self.N: int = int(self.tsim / self.Tp)  # ilość iteracji

        # stałe dla siły ciągu silnika (Fd)
        self.Fdmax: float = 10000               # ograniczenie siły ciągu [N]

        # stałe dla siły oporu aerodynamicznego (Fp)
        self.rho: float = 1.225                 # gęstość powietrza [kg/m^3]
        # powierzchnia przekroju poprzecznego pojazdu [m^2]
        self.A: float = 5.0
        self.Ca: float = 0.24                   # współczynnik oporu aerodynamicznego

        # stałe dla siły spychającej (Fs)
        self.m: float = 1000                    # masa samochodu [kg]
        # przyspieszenie ziemskie [m/s^2]
        self.g: float = 9.8
        self.alfa: float = 2                    # kąt nachylenia podłoża [°]

        self.vzad: float = vzad                 # prędkość zadana [m/s]
        self.v0: float = v0                     # prędkość początkowa [m/s]

        # tablice wraz z ograniczeniami
        self.e: List[float] = [0.0, ]           # wartości uchybu regulacji
        # wartości wielkości sterującej bez ograniczeń
        self.u_pierwotne: List[float] = [0.0, ]
        # wartości wielkości sterującej z ograniczeniami
        self.u: List[float] = [0.0, ]
        self.x: List[float] = [0.0, ]           # gaz
        # wartości prędkości pojazdu [m/s]
        self.v: List[float] = [v0, ]
        self.umin: float = -20
        self.umax: float = 20
        self.vmax: float = 200
        self.vmin: float = -200

        # tablica sil do wykresow
        self.Fcar: List[float] = [0.0]
        self.Fg: List[float] = [0.0]
        self.Fop: List[float] = [0.0]

        # wyznaczenie prostej do obliczania współczynnika % wciśnięcia pedału gazu
        self.prosta_a: float = 1 / self.umax

    def sim(self):
        for i in range(self.N):
            if i % 1000 == 0:
                print(i, '/', self.N)

            e = self.vzad - self.v[-1]
            self.e.append(e)

            u = self.kp*(self.e[-1] + (self.Tp/self.Ti)*sum(self.e) +
                         (self.Td/self.Tp)*(self.e[-1]-self.e[-2]))
            self.u_pierwotne.append(u)
            if u >= self.umax:
                u = self.umax
            elif u <= self.umin:
                u = self.umin
            self.u.append(u)
            self.x.append(self.prosta_a * u)

            Fcar = self.Fdmax*self.x[-1]
            Fg = self.m*self.g*math.sin(abs(math.radians(self.alfa)))
            Fop = 0.5*self.rho*self.A * self.Ca*self.v[-1]*self.v[-1]

            sgnFop = 1
            sgnFg = 1
            if math.radians(self.alfa) > 0:
                if self.v[-1] > 0:
                    sgnFop = -1
                    sgnFg = -1
                else:
                    sgnFop = 1
                    sgnFg = -1
            else:
                if self.v[-1] > 0:
                    sgnFop = -1
                    sgnFg = 1
                else:
                    sgnFop = 1
                    sgnFg = 1
            v = self.v[-1] + (self.Tp/self.m)*(Fcar+sgnFop*Fop+sgnFg*Fg)

            # zapamietanie sil
            self.Fcar.append(Fcar)
            self.Fg.append(sgnFg*Fg)
            self.Fop.append(sgnFop*Fop)

            if v >= self.vmax:
                v = self.vmax
            if v <= self.vmin:
                v = self.vmin
            self.v.append(v)

    def plots(self):
        t = [i * self.Tp for i in range(self.N + 1)]
        plt.close()

        plt.subplot(3, 1, 1)
        plt.plot(t, self.v, label="v")
        plt.axhline(y=self.vzad, color='r', linestyle='--', label="vzad")
        plt.xlabel("t [s]")
        plt.ylabel("v [m/s]")
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.plot(t, self.u, label="u")
        plt.plot(t, self.u_pierwotne, label="u_pierwotne")
        plt.xlabel("t [s]")
        plt.ylabel("u [V]")
        plt.legend()

        # plt.subplot(4, 1, 3)
        # plt.plot(t, self.x, label="Procent gas")
        # plt.xlabel("t [s]")
        # plt.ylabel("gas [%]")
        # plt.legend()

        plt.subplot(3, 1, 3)
        plt.plot(t, self.Fcar, label="Siła samochodu")
        plt.plot(t[1:], self.Fop[1:], label="Siła oporu")
        plt.plot(t[1:], self.Fg[1:], label="Siła spychająca")
        plt.xlabel("t [s]")
        plt.ylabel("F [N]")
        plt.legend(framealpha=.2, loc='upper right')

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=200)
        buf.seek(0)
        plt.close()
        # plt.clf()
        return buf

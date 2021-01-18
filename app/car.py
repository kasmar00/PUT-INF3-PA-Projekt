from bokeh.plotting import figure
from bokeh.layouts import column

import math
from typing import *


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
        p_h = 250
        p_w = 800
        s1 = figure(title="", sizing_mode="fixed",
                    plot_width=p_w, plot_height=p_h)
        s2 = figure(title="", sizing_mode="fixed", plot_width=p_w,
                    plot_height=p_h, x_range=s1.x_range, x_scale=s1.x_scale)
        s3 = figure(title="", sizing_mode="fixed", plot_width=p_w,
                    plot_height=p_h, x_range=s1.x_range, x_scale=s1.x_scale)

        s1.xaxis.axis_label = "t [s]"
        s1.yaxis.axis_label = "v [ᵏᵐ/ₕ]"
        s1.yaxis.axis_label_text_font_style = 'normal'
        s1.xaxis.axis_label_text_font_style = 'normal'
        s1.line(t, [3.6*x for x in self.v],
                color="blue", width=3, legend_label="v")
        s1.line(t, self.vzad*3.6, color="red", line_dash="dashed",
                width=3, legend_label="v_zad")

        s2.xaxis.axis_label = "t [s]"
        s2.yaxis.axis_label = "u [V]"
        s2.yaxis.axis_label_text_font_style = 'normal'
        s2.xaxis.axis_label_text_font_style = 'normal'
        s2.line(t, self.u_pierwotne, color="orange",
                width=5, legend_label="u_pierwotne")
        s2.line(t, self.u, color="blue", width=2, legend_label="u")

        s3.xaxis.axis_label = "t [s]"
        s3.yaxis.axis_label = "F [N]"
        s3.yaxis.axis_label_text_font_style = 'normal'
        s3.xaxis.axis_label_text_font_style = 'normal'
        s3.line(t, self.Fcar, color="blue", width=3,
                legend_label="Siła samochodu")
        s3.line(t[1:], self.Fg[1:], color="green",
                width=3, legend_label="Siła spychająca")
        s3.line(t[1:], self.Fop[1:], color="red",
                width=3, legend_label="Siła oporu")

        s3.legend.location = "top_right"
        p = column(s1, s2, s3)
        return p

import math
import time
import threading
import matplotlib.pyplot as plt

# A - pole powierzchni - usr def
# S - wydzelane ciepło w kelwinach/s __ usr def
# e - emitancja - usr def
# sigma - stała Stefana-Boltzmanna - const
# W - konwersja Jouli na Kelwiny

# Tp - okres próbkowania - usr def
# kp - wzmocnienie regulatora - usr def
# Td - czas wyprzedzenia - usr def
# Ti - czas zdwojenia - usr def

# e(n) - uchyb regulacji -> regulator -> u(n) (uchyb od wartości T_star (może być ujemny albo dodatni)(T_star(n)-h(n)))
# u(n) - wielkość sterująca

# T_n - następna temperatura

# T_star - temperatura docelowa - usr def
# T_zero - temperatura początkowa - usr def
# T_amb - temperatura otoczenia - usr def

# n - liczba kroków - diagnostyczne


class UAR():
    def __init__(self, n, T_star, T_zero, T_amb, kp, Tp, Ti, Td, A, e, W, S):
        self.T_star = T_star
        self.T_zero = T_zero
        self.T_amb = T_amb
        self.kp = kp
        self.Tp = Tp
        self.Ti = Ti
        self.Td = Td
        self.A = A
        self.e = e
        self.T_historic = [T_zero, T_zero]                  # tymczasowa "baza danych" - wartości początkowe muszą być dostępne
        self.e_historic = [T_star-T_zero, T_star-T_zero]    # tymczasowa "baza danych" - wartości początkowe muszą być dostępne
        self.S = S
        self.W = W
        self.sigma = 5.6704*(10**(-8))
        self.pause = threading.Event()                      # pauza - po uruchomieniu trzeba najpierw ustawić żeby rozpocząć (.set()). Żeby wstrzymać .clear()
        self.terminate = False                              # ustawienie terminate na true zatrzymuje program
        self.uMin = 0.5                                     # minimalne wzmocnienie
        self.uMax = 2                                       # maksymalne wzmocnienie
        self.n = n           # diagnostyczne
        self.__start__()

    def __T_n__(self):
        return self.T_historic[-1] + self.Tp*(self.S * self.__u_n__() - (self.sigma * self.e * self.A * ((self.T_historic[-1]**4) - (self.T_amb**4)) * self.W))

    def __e_n__(self):
        return self.T_star - self.T_historic[-1]

    def __u_n__(self):
        temp = self.kp*(self.e_historic[-2] + (self.Tp/self.Ti) * sum(self.e_historic) + self.Td/self.Tp*(self.e_historic[-1] - self.e_historic[-2]))
        if (temp < self.uMin):
            return self.uMin
        elif (temp > self.uMax):
            return self.uMax
        else:
            return temp

    def __build_data__(self):
        val = 0 #diagnostyczne

        while val < self.n: # do celów diagnostycznych
        # while True:        # odkomentować gdy będą przyciski do wznowienia i stopu (sprawdzić i wykorzystać ich implementację)
            self.e_historic.append(self.__e_n__())

            #self.S = 0.05 * self.__u_n__()
            temp = self.__T_n__()
            # print(temp)
            self.T_historic.append(temp)
            self.pause.wait()
            if (self.terminate):
                T_historic.clear()
                e_historic.clear()
                break
            val += 1 # diagnostyczne

    def __start__(self):
        t = threading.Thread(name="process", target=self.__build_data__)
        t.start()

    # poniższa funkcja ma przedewszystkim zastosowanie diagnostyczne
    def plot(self, show, save):
        pl = plt.plot(self.T_historic)
        plt.ylabel('T[stC')
        plt.xlabel('n')
        if save:
            plt.savefig("static/images/plot.png", dpi=250)
        if show:
            plt.show()

    def get_step(self):
        temp = self.__T_n__()
        self.T_historic.append(temp)
        return temp

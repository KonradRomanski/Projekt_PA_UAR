import math
import time
import threading
#import matplotlib.pyplot as plt

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

# n - krok obecny


class UAR():
    def __init__(self, T_star, T_zero, kp, Tp, Ti, Td, A, e, W, S):
        self.T_star = T_star
        self.T_zero = T_zero
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
        self.terminate = false                              # ustawienie terminate na true zatrzymuje program
        self.uMin = 0.5                                     # minimalne wzmocnienie
        self.uMax = 2                                       # maksymalne wzmocnienie
        #self.__build_data__()

    def __T_n__(self):
        return self.T_historic[-1] + self.Tp*(self.S * self.__u_n__() - (self.sigma * self.e * self.A * ((self.T_historic[-1]**4) - (self.T_zero**4)) * W))

    def __e_n__(self):
        return self.T_star - self.T_historic[-1]

    def __u_n__(self):
        temp = self.kp*(self.e_historic[-2] + (self.Tp/self.Ti) * sum(self.e_historic) + self.Td/self.Tp*(self.e_historic[-1] - self.e_historic[-2]))
        if (temp < uMin):
            return uMin
        elif (temp > uMax):
            return uMax
        else:
            return temp

    # # uwaga, opieram się tutaj na wysokości h bardziej historycznej (n-2 i n-1)
    # def __S_n__(self):
    #     return self.A/self.Tp * (self.T_historic[-1] - self.T_historic[-2]) + self.beta * self.math.sqrt(self.T_historic[-1])

    def __build_data__(self):

        while True:
            self.e_historic.append(self.__e_n__())
            # print(u)
            # S = S_n(A, T_historic, Tp, beta, n)

            #self.S = 0.05 * self.__u_n__()
            temp = self.__T_n__()
            # print(temp)
            self.T_historic.append(temp)
            self.pause.wait()
            if (terminate):
                h_historic.clear()
                e_historic.clear()
                break
            
    def __start__(self):
        t = threading.Thread(name="process", target=self.__build_data__, args=(self,))
        t.start()


    # def plot(self, show, save):
    #     pl = plt.plot(self.T_historic)
    #     plt.ylabel('h')
    #     plt.xlabel('n')
    #     if save:
    #         plt.savefig("static/images/plot.png", dpi=250)
    #     if show:
    #         plt.show()

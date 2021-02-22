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
    def __init__(self, n, T_star, T_zero, T_amb, kp, Tp, Ti, Td, A, e, W, S): # n do usunięcia po zakończeniu diagnozowania czegokolwiek - ewentualnie po prostu wstawić tam domyślnie jakąś useless zmienną albo stałą np. 0
        self.TEST = 0
        self.T_star = T_star
        self.T_zero = T_zero
        self.T_amb = T_amb
        self.kp = kp
        self.Tp = Tp
        self.Ti = Ti
        self.Td = Td
        self.A = A
        self.e = e
        self.T_historic = [T_zero, T_zero]  # tymczasowa "baza danych" - wartości początkowe muszą być dostępne
        self.e_historic = [T_star - T_zero,
                           T_star - T_zero]  # tymczasowa "baza danych" - wartości początkowe muszą być dostępne
        self.S = S
        self.W = W
        self.sigma = 5.6704 * (10 ** (-8))
        self.pause = threading.Event()  # pauza - po uruchomieniu trzeba najpierw ustawić żeby rozpocząć (.set()). Żeby wstrzymać .clear()
        self.terminate = False  # ustawienie terminate na true zatrzymuje program
        self.uMin = 0.5  # minimalne wzmocnienie
        self.uMax = 2  # maksymalne wzmocnienie
        self.n = n  # diagnostyczne
        # self.__start__()

        # ----------WSKAŹNIKI JAKOŚCI----
        self.L_czasRegObl = 0  # do funkcji CzasRegulacji
        self.L_paramtetrRegulacji = 0.05  # parametr o wartości pomiędzy 0,01 do 0,05, aby obliczyć deltaT, możnaby dodać kontrolkę na stronie, żeby user def
        self.u_historic = []

    def update_values(self, n, T_star, T_zero, T_amb, kp, Tp, Ti, Td, A, e, W, S):
        self.TEST = 0
        self.T_star = T_star
        self.T_zero = T_zero
        self.T_amb = T_amb
        self.kp = kp
        self.Tp = Tp
        self.Ti = Ti
        self.Td = Td
        self.A = A
        self.e = e
        self.T_historic = [T_zero, T_zero]  # tymczasowa "baza danych" - wartości początkowe muszą być dostępne
        self.e_historic = [T_star - T_zero,
                           T_star - T_zero]  # tymczasowa "baza danych" - wartości początkowe muszą być dostępne
        self.S = S
        self.W = W
        self.sigma = 5.6704 * (10 ** (-8))
        self.pause = threading.Event()  # pauza - po uruchomieniu trzeba najpierw ustawić żeby rozpocząć (.set()). Żeby wstrzymać .clear()
        self.terminate = False  # ustawienie terminate na true zatrzymuje program
        self.uMin = 0.5  # minimalne wzmocnienie
        self.uMax = 2  # maksymalne wzmocnienie
        self.n = n

    def __T_n__(self):
        return self.T_historic[-1] + self.Tp * (self.S * self.__u_n__() - (
                    self.sigma * self.e * self.A * ((self.T_historic[-1] ** 4) - (self.T_amb ** 4)) * self.W))

    def __e_n__(self):
        return self.T_star - self.T_historic[-1]

    def __u_n__(self):
        temp = self.kp * (self.e_historic[-2] + (self.Tp / self.Ti) * sum(self.e_historic) + self.Td / self.Tp * (
                    self.e_historic[-1] - self.e_historic[-2]))
        if (temp < self.uMin):
            return self.uMin
        elif (temp > self.uMax):
            return self.uMax
        else:
            return temp

    def __build_data__(self):
        val = 0  # diagnostyczne

        while val < self.n:  # do celów diagnostycznych
            # while True:        # odkomentować gdy będą przyciski do wznowienia i stopu (sprawdzić i wykorzystać ich implementację)
            self.e_historic.append(self.__e_n__())

            # self.S = 0.05 * self.__u_n__()
            temp = self.__T_n__()
            # print(temp)
            self.T_historic.append(temp)
            self.pause.wait()
            if (self.terminate):
                self.T_historic.clear()
                self.e_historic.clear()
                break
            val += 1  # diagnostyczne

    def __start__(self):
        t = threading.Thread(name="process", target=self.__build_data__)
        t.start()

    # poniższa funkcja ma przedewszystkim zastosowanie diagnostyczne
    def plot(self, show, save):
        pl = plt.plot(self.T_historic)
        plt.ylabel('T[stC]')
        plt.xlabel('n')
        if save:
            plt.savefig("static/images/plot.png", dpi=250)
        if show:
            plt.show()

    def get_step(self):
        self.e_historic.append(self.__e_n__())
        self.u_historic.append(self.__u_n__())
        temp = self.__T_n__()
        self.T_historic.append(temp)
        return temp

    def get_test(self):
        self.TEST += 1
        return self.TEST

    # --------WSKAŹNIKI JAKOŚCI---------------------------------------------------------------------------------------

    # Funkcja zwraca uchyb ustalony w momencie, kiedy już się ustali. Przed tym nie zwraca nic.
    # Uchyb ustalony mamy wtedy, kiedy temp przyjmuje wartości <= o dany % T_star
    def uchybUstalony(self, licznik):
        ileProcent = 5  # granica
        granica = abs(ileProcent * (self.T_zero - self.T_star) / 100)
        if licznik > 1:
            # sprawdzamy, czy jest przełamanie fali
            if abs((self.T_star - self.T_historic[licznik - 1])) > abs((self.T_star - self.T_historic[licznik])) > abs(
                    (self.T_star - self.T_historic[licznik - 2])):
                if abs((self.T_star - self.T_historic[licznik - 1])) < granica:
                    return abs(self.T_star - self.T_historic[licznik - 1])

    # stała wartość, teoretycznie powinna być w %, więc można return pomnożyć razy 100
    def przeregulowanie(self, licznik):
        if licznik > 1:
            # sprawdzamy, czy jest przełamanie fali
            if abs((self.T_star - self.T_historic[licznik - 1])) > abs((self.T_star - self.T_historic[licznik])) > abs(
                    (self.T_star - self.T_historic[licznik - 2])):
                return abs((max(self.T_historic) - self.T_star) / self.T_star)

    # stała wartość, zwraca n*okres próbkowania
    def czasRegulacji(self, licznik):
        if self.L_czasRegObl == 0:
            deltaT = self.L_paramtetrRegulacji * self.T_star
            if licznik > 1:
                # sprawdzamy, czy jest przełamanie fali
                if abs((self.T_star - self.T_historic[licznik - 1])) > abs(
                        (self.T_star - self.T_historic[licznik])) > abs((self.T_star - self.T_historic[licznik - 2])):
                    # Czy musi być and tutaj?
                    if (self.T_star - deltaT) <= self.T_historic[licznik] <= (self.T_star + deltaT):
                        self.L_czasRegObl = licznik * self.Tp
                        return self.L_czasRegObl

    def dokladnoscRegulacji_e(self):
        suma = 0
        for n in self.e_historic:
            suma += abs(n)
        return self.Tp * suma

    def dokladnoscRegulacji_e2(self):
        suma = 0
        for n in self.e_historic:
            suma += n ** 2
        return self.Tp * suma

    def kosztyRegulacji_u(self):
        suma = 0
        for n in self.u_historic:
            suma += abs(n)
        return self.Tp * suma

    def kosztyRegulacji_u2(self):
        suma = 0
        for n in self.u_historic:
            suma += n ** 2
        return self.Tp * suma
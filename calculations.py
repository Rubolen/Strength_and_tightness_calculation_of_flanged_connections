from body_units import Flange
import math
from math import sqrt

class Calculations:

    def __init__(self, flange1, flange2, gasket, bolt, washer1, washer2):
        self.flange1 = flange1
        self.flange2 = flange2
        self.gasket = gasket
        self.bolt = bolt
        self.washer1 = washer1
        self.washer2 = washer2


    # 5 Усилия, необходимые для смятия прокладки и обеспечения
    # герметичности фланцевого соединения
    def forces_to_compress_gasket(self, p):

        #Усилие, необходимое для смятия прокладки при затяжке
        p_compress = 0.5 * math.pi * self.gasket.get_gasket_params()[0] * self.gasket.get_gasket_params()[1] * self.gasket.q_compress

        #Усилие на прокладке в рабочих условиях
        r_g = math.pi * self.gasket.get_gasket_params()[0] * self.gasket.get_gasket_params()[1] * self.gasket.m * abs(p)

        return p_compress, r_g


    def get_force_moment_arms(self):
        # Плечи действия сил в болтах
        if self.flange1.type == '11':
            b = 0.5 * (self.flange1.D_1 - self.gasket.get_gasket_params()[0])
        elif self.flange1.type == 'loose_rings':
            a = 0.5 * (self.flange1.D_1 - self.flange1.D_s)
            b = 0.5 * (self.flange1.D_s - self.gasket.get_gasket_params()[0])

        if self.flange1.type == '11':
            beta = self.flange1.S_1 / self.flange1.S_0
            x = self.flange1.l / (self.flange1.d_1 * self.flange1.S_0)
            dzeta = 1 + (beta - 1) * x / (x + (1 + beta) / 4)
            S_e = dzeta * self.flange1.S_0
        else:
            S_e = self.flange1.S_0
        # Плечо усилия от действия давления на фланец
        e = 0.5 * (self.gasket.get_gasket_params()[0] - self.flange1.d_1 - S_e)

        return b, e

    def get_flange_connection_stiffness(self):

        print(self.flange1.type)

        if self.flange1.type == '11':
            gamma = 1 / (
                        self.gasket.get_gasket_stiffness() + self.bolt.get_bolt_stiffness(self.flange1, self.flange2) * self.bolt.E20 / self.bolt.E +
                        (self.flange1.get_angular_flange_compliance() * self.flange1.E20 / self.flange1.E +
                         self.flange2.get_angular_flange_compliance() * self.flange2.E20 / self.flange2.E) *
                        self.get_force_moment_arms()[0] ** 2)
            return gamma

        return None

    # 6 Усилия в болтах(шпильках) фланцевого соединения
    # при затяжке и в рабочих условиях
    def forces_bolt_tension(self, p, F, M):

        # 6.1 Суммарная площадь сечения болтов(шпилек)
        A_b = self.flange1.n * self.bolt.f_b

        # 6.2 Равнодействующая нагрузка от давления
        Q_p = 0.785 * self.gasket.get_gasket_params()[0] * self.gasket.get_gasket_params()[0] * p

        # 6.3 Приведенная нагрузка, вызванная воздействием внешней силы и изгибающего момента
        Q_FM = (F + 4 * abs(M) / self.gasket.get_gasket_params()[0], F - 4 * abs(M) / self.gasket.get_gasket_params()[0])

        # 6.4 Нагрузка, вызванная стесненностью температурных деформаций
        if self.flange1.type == '11':
            Q_t = (self.get_flange_connection_stiffness() * ((self.flange1.alpha * self.flange1.b + self.washer1.alpha * self.washer1.s) * (self.flange1.temperature - 20) +
                                                            (self.flange2.alpha * self.flange2.b + self.washer2.alpha * self.washer2.s) * (self.flange2.temperature - 20) -
                                                            self.bolt.alpha*(self.flange1.b + self.flange2.b) * (self.bolt.temperature - 20)))

        return(A_b, Q_p, Q_FM, float(Q_t))



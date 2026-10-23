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

        #Усилие на прокладке в рабочих условиях (R_п)
        r_g = math.pi * self.gasket.get_gasket_params()[0] * self.gasket.get_gasket_params()[1] * self.gasket.m * abs(p)

        return p_compress, r_g


    def get_force_moment_arms(self, flange: object, gasket: object):
        # Плечи действия сил в болтах
        if flange.type == '11':
            b = 0.5 * (flange.D_1 - gasket.get_gasket_params()[0])
        elif flange.type == 'loose_rings':
            a = 0.5 * (flange.D_1 - flange.D_s)
            b = 0.5 * (flange.D_s - gasket.get_gasket_params()[0])

        if flange.type == '11':
            beta = flange.S_1 / flange.S_0
            x = flange.l / (flange.d_1 * flange.S_0)
            dzeta = 1 + (beta - 1) * x / (x + (1 + beta) / 4)
            S_e = dzeta * flange.S_0
        else:
            S_e = flange.S_0
        # Плечо усилия от действия давления на фланец
        e = 0.5 * (gasket.get_gasket_params()[0] - flange.d_1 - S_e)

        return b, e

    # Приложение Е гамма
    def get_flange_connection_stiffness(self):

        if self.flange1.type == '11':
            gamma = 1 / (
                        self.gasket.get_gasket_compliance() + self.bolt.get_bolt_compliance(self.flange1, self.flange2) * self.bolt.E20 / self.bolt.E +
                        (self.flange1.get_angular_flange_compliance() * self.flange1.E20 / self.flange1.E +
                         self.flange2.get_angular_flange_compliance() * self.flange2.E20 / self.flange2.E) *
                        self.get_force_moment_arms(self.flange1, self.gasket)[0] ** 2)
            return gamma

        return None

    # Коэффициент жесткости фланцевого соединения (альфа)
    def get_stiffness_coefficient_flanged_connection_force(self):
        if self.flange1.type == '11':
            alpha = (1 - (self.gasket.get_gasket_compliance() - (self.flange1.get_angular_flange_compliance() *
                                                                 self.get_force_moment_arms(self.flange1, self.gasket)[1] +
                                                                 (self.flange2.get_angular_flange_compliance()) *
                                                                 self.get_force_moment_arms(self.flange2, self.gasket)[1]) *
                          self.get_force_moment_arms(self.flange1, self.gasket)[0]) /
                     (self.gasket.get_gasket_compliance() + self.bolt.get_bolt_compliance(self.flange1, self.flange2) +
                      (self.flange1.get_angular_flange_compliance() + self.flange2.get_angular_flange_compliance()) *
                      self.get_force_moment_arms(self.flange1, self.gasket)[0]**2))

            return alpha

        return None

    #Коэффициент жесткости фланцевого соединения, нагруженного внешним изгибающим моментом (альфа_м)
    def get_stiffness_coefficient_flanged_connection_moment(self):

        if self.flange1.type == '11':
            alpha_m = ((self.bolt.get_bolt_compliance(self.flange1, self.flange2) +
                       2 * self.flange1.get_angular_flange_compliance_ext_bend_moment(self.flange1.D_1, self.flange1.capD,  self.flange1.E20) *
                       self.get_force_moment_arms(self.flange1, self.gasket)[0] * (self.get_force_moment_arms(self.flange1, self.gasket)[0] +
                                                                                   self.get_force_moment_arms(self.flange1, self.gasket)[1]) -
                       (self.get_force_moment_arms(self.flange1, self.gasket)[0]**2) / self.gasket.get_gasket_params()[0]) /
                       ((self.bolt.get_bolt_compliance(self.flange1, self.flange2)) + self.gasket.get_gasket_compliance() *
                        ((self.flange1.D_1 / self.gasket.get_gasket_params()[0])**2) +
                        2 * self.flange1.get_angular_flange_compliance_ext_bend_moment(self.flange1.D_1, self.flange1.capD,  self.flange1.E20) *
                        self.get_force_moment_arms(self.flange1, self.gasket)[0]))
            return alpha_m

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
        elif self.flange1.type == 'свободными фланцами':
            pass

        elif self.flange1.type == 'в соединении с крышкой':
            pass

        elif self.flange1.type == ' в случае, если между фланцами зажата трубная решетка или иная закладная деталь':
            pass

        # 6.5 Расчетная нагрузка на болты (шпильки) фланцевых соединений при затяжке

        Pb1_1 = self.get_stiffness_coefficient_flanged_connection_force() * (Q_p + F) + self.forces_to_compress_gasket(p)[1]
        + 4 * self.get_stiffness_coefficient_flanged_connection_moment() * abs(M) / self.gasket.get_gasket_params()[0]

        Pb1_2 = self.get_stiffness_coefficient_flanged_connection_force() * (Q_p + F) + self.forces_to_compress_gasket(p)[1]
        + 4 * self.get_stiffness_coefficient_flanged_connection_moment() * abs(M) / self.gasket.get_gasket_params()[0] - Q_t

        # Расчетная нагрузка на болты(шпильки) при затяжке, необходимая для обеспечения в рабочих условиях давления на прокладку, достаточного для герметизации фланцевого соединения
        Pb1 = max(Pb1_1, Pb1_2)

        Pb2_1 = self.forces_to_compress_gasket(p)[0]

        Pb2_2 = 0.4 * A_b * self.bolt.allowable_bolt_stress
        # Расчетная нагрузка на болты(шпильки) при затяжке, необходимая для обеспечения обжатия прокладки и минимального начального натяжения болтов(шпилек)
        Pb2 = max(Pb2_1, Pb2_2)

        Pbm = max(Pb1, Pb2)

        #6.6 Расчетная нагрузка на болты(шпильки) фланцевых соединений в рабочих условиях
        Pbp = (Pbm + (1.0 - self.get_stiffness_coefficient_flanged_connection_force()) * (Q_p + F) + Q_t +
               (4.0 * (1 - self.get_stiffness_coefficient_flanged_connection_moment()) * abs(M)) /
               (self.gasket.get_gasket_params()[0]))

        return A_b, Q_p, Q_FM, float(Q_t), float(Pbm), float(Pbp)



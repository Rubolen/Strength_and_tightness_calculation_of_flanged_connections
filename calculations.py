from body_units import Flange
import math
from math import sqrt

class Calculations:

    def __init__(self, flange1, flange2, gasket, bolt):
        self.flange1 = flange1
        self.flange2 = flange2
        self.gasket = gasket
        self.bolt = bolt


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
        if self.flange1.type == 'weld_neck' or 'slip_on':
            b = 0.5 * (self.flange1.D_1 - self.gasket.get_gasket_params()[0])
        elif self.flange1.type == 'loose_rings':
            a = 0.5 * (self.flange1.D_1 - self.flange1.D_s)
            b = 0.5 * (self.flange1.D_s - self.gasket.get_gasket_params()[0])

        if self.flange1.type == 'weld_neck':
            beta = self.flange1.S_1 / self.flange1.S_0
            x = self.flange1.l / (self.flange1.d_r1 * self.flange1.S_0)
            dzeta = 1 + (beta - 1) * x / (x + (1 + beta) / 4)
            S_e = dzeta * self.flange1.S_0
        else:
            S_e = self.flange1.S_0
        # Плечо усилия от действия давления на фланец
        e = 0.5 * (self.gasket.get_gasket_params()[0] - self.flange1.d_r1 - S_e)

        return b, e

    def get_flange_connection_stiffness(self):

        if self.flange1.type == 'weld_neck' or 'slip_on':

            gamma = 1 / (self.gasket.get_gasket_stiffness() + self.bolt.get_bolt_stiffness(self.flange1, self.flange2)*
                         self.bolt.E_20/self.bolt.E + (y_f1*E1_20/E_1 + y_f2*E2_20/E_2) * b * b)

    # 6 Усилия в болтах(шпильках) фланцевого соединения
    # при затяжке и в рабочих условиях
    def forces_bolt_tension(self, p, F, M):

        # 6.1 Суммарная площадь сечения болтов(шпилек)
        A_b = self.flange.n_r1 * self.bolt.f_b

        # 6.2 Равнодействующая нагрузка от давления
        Q_p = 0.785 * self.gasket.get_gasket_params()[0] * self.gasket.get_gasket_params()[0] * p

        # 6.3 Приведенная нагрузка, вызванная воздействием внешней силы и изгибающего момента
        Q_FM = (F + 4 * abs(M) / self.gasket.get_gasket_params()[0], F - 4 * abs(M) / self.gasket.get_gasket_params()[0])

        # 6.4 Нагрузка, вызванная стесненностью температурных деформаций
        if self.flange.type == 'weld-neck' or 'slip-on':
            Q_t = gamma * ((alpha_f * h_1 + alpha_w * h_w) * (t_f - 20) + (alpha_f * h_1 + alpha_w * h_w) * (t_f - 20) -
                   alpha_b*(h_1 + h_2) * (t_b - 20))
from db_sqlite3 import DatabaseConnection
import math


db = DatabaseConnection()
class Flange:

    def __init__(self, type, params = None):

        self.type = type
        self.DN = params[0]
        self.PN = params[1]
        if self.type == 'weld_neck' or 'slip_on':
            self.D_m_r1 = db.get_element_from_table('Table6', 'D_m_r1', ['DN', 'PN'], [str(self.DN), str(self.PN)])[0][0]
            # self.D_m_r2 = D_m_r2
            self.D_n_r1 = db.get_element_from_table('Table6', 'D_n_r1', ['DN', 'PN'], [str(self.DN), str(self.PN)])[0][0]
            # self.D_n_r2 = D_n_r2
            self.d_1_r1 = db.get_element_from_table('Table6', 'd_1_r1', ['DN', 'PN'], [str(self.DN), str(self.PN)])[0][0]
            # self.d_1_r2 = d_1_r2
            self.b_r1 = db.get_element_from_table('Table6', 'b_r1', ['DN', 'PN'], [str(self.DN), str(self.PN)])[0][0]
            # self.b_r2 = b_r2
            self.H_r1 = db.get_element_from_table('Table6', 'H_r1', ['DN', 'PN'], [str(self.DN), str(self.PN)])[0][0]
            # self.H_r2 = H_r2
            # self.H_1 = H_1
            self.capD_r1 = db.get_element_from_table('Table6', 'capD_r1', ['DN', 'PN'], [str(self.DN), str(self.PN)])[0][0]
            # self.capD_r2 = capD_r2
            self.D_1 = db.get_element_from_table('Table6', 'D_1', ['DN', 'PN'], [str(self.DN), str(self.PN)])[0][0]
            self.d_r1 = db.get_element_from_table('Table6', 'd_r1', ['DN', 'PN'], [str(self.DN), str(self.PN)])[0][0]
            # self.d_r2 = d_r2
            self.n_r1 = db.get_element_from_table('Table6', 'n_r1', ['DN', 'PN'], [str(self.DN), str(self.PN)])[0][0]
            # self.n_r2 = n_r2
            self.Nom_bolt_diam_r1 = db.get_element_from_table('Table6', 'Nom_bolt_diam_r1', ['DN', 'PN'], [str(self.DN), str(self.PN)])[0][0]
            # self.Nom_bolt_diam_r2 = Nom_bolt_diam_r2

            # толщина втулки приварного встык фланца в месте приварки к обечайке(трубе)
            self.S_0 = (self.D_n_r1 - self.d_r1) / 2

            # толщина втулки приварного встык фланца в месте присоединения к тарелке
            self.S_1 = (self.D_m_r1 - self.d_r1) / 2

            # длина конической втулки приварного встык фланца, мм
            self.l = self.H_r1 - self.b_r1

    def get_flange_plate_coefficients(self):

        K = self.capD_r1 / self.d_1_r1
        beta_T = (K*K*(1 + 8.55*math.log(K, 10)) - 1) / ((1.05 + 1.945*K*K) * (K - 1))
        beta_U = (K*K*(1 + 8.55*math.log(K, 10)) - 1) / (1.36 * (K*K - 1) * (K - 1))
        beta_Y = (0.69 + 5.72 * (K*K*math.log(K, 10)) / (K*K - 1)) / (K - 1)
        beta_Z = (K*K + 1) / (K*K - 1)

        return beta_T, beta_U, beta_Y, beta_Z



    # def get_flange_stiffness(self):


class Gasket:

    def __init__(self, type, params = None):
        self.type = type
        if self.type == 'flat':
            self.D_cap = params[0]
            self.d = params[1]
            self.b_g = (self.D_cap - self.d) / 2
            self.q_compress = params[2]
            self.m = params[3]
            self.E_g = db.get_element_from_table('Table_и1', 'E_g',
                                                        ['type_and_material'],
                                                        ['Плоская неметаллическая прокладка из:паронита по ГОСТ 481 при толщине не более 2—3 мм'])[0][0]
            self.K_compress = db.get_element_from_table('Table_и1', 'K_compress',
                                                        ['type_and_material'],
                                                        ['Плоская неметаллическая прокладка из:паронита по ГОСТ 481 при толщине не более 2—3 мм'])[0][0]
            self.h_g = db.get_element_from_table('GOST_15180_86_table_4', 'h',['DN', 'PN'], ['40', '1_16'])[0][0]


    def get_gasket_params(self):
        if self.type == 'flat':
            if self.b_g >= 15:
                b_0 = self.b_g
            else:
                b_0 = 3.8 * math.sqrt(self.b_g)
            D_mg = self.D_cap - b_0

        elif self.type == 'oval':
            b_0 = self.b_g / 4
            D_mg = (self.D_cap + self.d) / 2

        else:
            D_mg, b_0 = None, None

        return D_mg, b_0


    def get_gasket_stiffness(self):
        # Податливость прокладки ( для металических и асбометаллических y_g = 0 )
        y_g = (self.h_g * self.K_compress) / (self.E_g * math.pi * self.get_gasket_params()[0] * self.b_g)
        return y_g


class Bolt:

    def __init__(self, isgrooved, type, flange1):
        self.isgrooved = isgrooved
        self.type = type
        self.diam = flange1.Nom_bolt_diam_r1
        self.n = flange1.n_r1
        self.E20 = db.get_element_from_table('GOST_34233_4_2017_table_г1', '[25X1МФ]',
                                             ['[Расчетная температура болтов (шпилек)]'], ['20'])[0][0]
        self.E = db.get_element_from_table('GOST_34233_4_2017_table_г1', '[25X1МФ]',
                                             ['[Расчетная температура болтов (шпилек)]'], ['100'])[0][0]
        if self.isgrooved == True:
            self.f_b = db.get_element_from_table('GOST_34233_4_2017_table_д1', self.diam, ['ID'], ['1'])[0][0]
        else:
            self.f_b = db.get_element_from_table('GOST_34233_4_2017_table_д1', self.diam, ['ID'], ['0'])[0][0]


    def get_distance_between_the_bearing_surfaces(self, flange1, flange2):
        if flange1.type == 'weld-neck' and flange2.type == 'weld-neck':
            L_b0 = flange1.b_r1 + flange2.b_r1

        return L_b0

    def get_bolt_stiffness(self, flange1, flange2):
        if self.type == 'bolt':
            L_b = self.get_distance_between_the_bearing_surfaces(flange1, flange2) + 0.28 * int(self.diam[1:])
        elif self.type == 'pin':
            L_b = self.get_distance_between_the_bearing_surfaces(flange1, flange2) + 0.56 * int(self.diam[1:])

        y_b = L_b / (self.E20 * self.f_b * self.n)

        return y_b

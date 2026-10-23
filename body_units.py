from db_sqlite3 import DatabaseConnection
import math
from function_approximation import Approximation


db = DatabaseConnection()
db1 = DatabaseConnection('GOST_33259—2015.db')


class Part:

    def __init__(self, material_id: int, temperature: int):
        self.material_id = material_id
        self.temperature = temperature




class Flange(Part):

    def __init__(self, type: str, material_id: int, temperature: int, dn, pn, params = None):

        super().__init__(material_id, temperature)
        self.type = db.get_element_from_table('flange_types', 'code', ['name_ru'], [type])[0][0]
        self.DN = dn
        self.PN = pn
        # self.temperature = params[2]
        if self.type == '11':
            self.D_m = db.get_element_from_table('flange_type11_dimensions', 'Dm_mm', ['dn', 'pn'], [str(self.DN), str(self.PN)])[0][0]
            # self.D_m_r2 = D_m_r2
            self.D_n = db.get_element_from_table('flange_type11_dimensions', 'Dn_mm', ['dn', 'pn'], [str(self.DN), str(self.PN)])[0][0]
            # self.D_n_r2 = D_n_r2
            self.d_1 = db.get_element_from_table('flange_type11_dimensions', 'neck_d1_mm', ['dn', 'pn'], [str(self.DN), str(self.PN)])[0][0]
            # self.d_1_r2 = d_1_r2
            self.b = db.get_element_from_table('flange_type11_dimensions', 'b_mm', ['dn', 'pn'], [str(self.DN), str(self.PN)])[0][0]
            # self.b_r2 = b_r2
            self.H = db.get_element_from_table('flange_type11_dimensions', 'H_mm', ['dn', 'pn'], [str(self.DN), str(self.PN)])[0][0]
            # self.H_r2 = H_r2
            # self.H_1 = H_1
            #Наружный диаметр фланца (D_н)
            self.capD = db.get_element_from_table('flange_type11_dimensions', 'D_mm', ['dn', 'pn'], [str(self.DN), str(self.PN)])[0][0]
            # self.capD_r2 = capD_r2
            #Диаметр окружности расположения болтов (D_б)
            self.D_1 = db.get_element_from_table('flange_type11_dimensions', 'D1_mm', ['dn', 'pn'], [str(self.DN), str(self.PN)])[0][0]
            self.d = db.get_element_from_table('flange_type11_dimensions', 'bolt_hole_d_mm', ['dn', 'pn'], [str(self.DN), str(self.PN)])[0][0]
            # self.d_r2 = d_r2
            self.n = db.get_element_from_table('flange_type11_dimensions', 'bolt_count', ['dn', 'pn'], [str(self.DN), str(self.PN)])[0][0]
            # self.n_r2 = n_r2
            self.Nom_bolt_diam = db.get_element_from_table('flange_type11_dimensions', 'bolt_thread', ['dn', 'pn'], [str(self.DN), str(self.PN)])[0][0]

            self.E20 = db.get_element_from_table('steel_elastic_modulus', 'temp_20', ['id'], [str(self.material_id)])[0][0]

            self.E = db.get_element_from_table('steel_elastic_modulus', 'temp_' + str(self.temperature), ['id'], [str(self.material_id)])[0][0]

            # self.Nom_bolt_diam_r2 = Nom_bolt_diam_r2

            # толщина втулки приварного встык фланца в месте приварки к обечайке(трубе)
            self.S_0 = (self.D_n - self.d) / 2

            # толщина втулки приварного встык фланца в месте присоединения к тарелке
            self.S_1 = (self.D_m - self.d) / 2

            # длина конической втулки приварного встык фланца, мм
            self.l = self.H - self.b

            # параметр длины втулки, мм
            self.l0 = math.sqrt(self.d_1 * self.S_0)

            self.x = self.l / self.l0

            self.alpha = db.get_element_from_table('linear_expansion_coefficients', 'temp_20_' + str(self.temperature), ['id'], [str(16)])[0][0]



    def get_flange_plate_coefficients(self):

        K = self.capD / self.d_1
        beta_T = (K*K*(1 + 8.55*math.log(K, 10)) - 1) / ((1.05 + 1.945*K*K) * (K - 1))
        beta_U = (K*K*(1 + 8.55*math.log(K, 10)) - 1) / (1.36 * (K*K - 1) * (K - 1))
        beta_Y = (0.69 + 5.72 * (K*K*math.log(K, 10)) / (K*K - 1)) / (K - 1)
        beta_Z = (K*K + 1) / (K*K - 1)
        beta_F = Approximation( self.x, 'T')
        beta_V = Approximation(self.x, 'V')

        return beta_T, beta_U, beta_Y, beta_Z, beta_F.func_fit()( self.S_1/ self.S_0), beta_V.func_fit()( self.S_1/ self.S_0)


    def get_lambda_coef(self):
        lambd = ((self.get_flange_plate_coefficients()[4] * self.b + self.l0) / (self.get_flange_plate_coefficients()[0] * self.l0) +
                 (self.get_flange_plate_coefficients()[5] * self.b * self.b * self.b) / (self.get_flange_plate_coefficients()[1] * self.l0 * self.S_0 * self.S_0))

        return lambd


    #Угловая податливость фланца при затяжке (y_ф)
    def get_angular_flange_compliance(self):
        return 0.91 * self.get_flange_plate_coefficients()[5] / (self.E20 * self.get_lambda_coef() * self.S_0 * self.S_0 * self.l0)

    # def get_psi_coef(self):
    #     return 1.28 * math.log()

    # def get_angular_loose_flange_ring_compliance(self):
    #     return

    #Угловая податливость фланца, нагруженного внешним изгибающим моментом (y_ф.н)
    def get_angular_flange_compliance_ext_bend_moment(self, D1, D2, E):
        y_fn = ((math.pi / 4)**3) * D1 / (E * D2 * self.b**3)
        return y_fn



    # def get_flange_stiffness(self):


class Gasket:

    def __init__(self, type_obj:str, execution:str, material_id:int, flange:object):
        self.type = type_obj
        self.execution = execution
        if self.type == 'flat':
            gasket_ids = db.get_element_from_table('gasket_'+ self.execution,'id', ['dn'], [str(flange.DN)])
            gasket_id = 0
            for id in gasket_ids:

                if (float(db.get_element_from_table('gasket_'+ self.execution, 'pn_min_kgf', ['id'], [str(id[0])])[0][0]) < flange.DN
                <=  float(db.get_element_from_table('gasket_'+ self.execution, 'pn_max_kgf', ['id'], [str(id[0])])[0][0])):
                    gasket_id = id[0]

            self.D_cap = db.get_element_from_table('gasket_'+execution, 'outer_d', ['id'], [str(gasket_id)])[0][0]
            self.d = db.get_element_from_table('gasket_'+execution, 'inner_d', ['id'], [str(gasket_id)])[0][0]
            self.b_g = (self.D_cap - self.d) / 2
            self.q_compress = db.get_element_from_table('gasket_materials', 'q_obzh', ['id'], [str(material_id)])[0][0]
            self.m = db.get_element_from_table('gasket_materials', 'm', ['id'], [str(material_id)])[0][0]
            if self.execution == 'a' or 'b' or 'v':
                if flange.DN < 1400:
                    self.h_g = 2
                else:
                    self.h_g = 3
            else:
                self.h_g = db.get_element_from_table('gasket_'+execution, 'thickness_s', ['id'], [str(gasket_id)])[0][0]

            if material_id == 1:
                self.E_g = 0.3 * 10**(-4) * (1 + self.b_g/ (2 * self.h_g))
            elif material_id == 2:
                self.E_g = 0.4 * 10 ** (-4) * (1 + self.b_g / (2 * self.h_g))
            else:
                self.E_g = db.get_element_from_table('gasket_materials', 'e_p',['id'],[str(material_id)])[0][0]


            self.K_compress = db.get_element_from_table('gasket_materials', 'k_obzh',['id'],[str(material_id)])[0][0]

            if self.execution == 'a' or 'b' or 'v':
                if flange.DN < 1400:
                    self.h_g = 2
                else:
                    self.h_g = 3
            else:
                self.h_g = db.get_element_from_table('gasket_'+ self.execution,'thickness_s', ['dn'], [str(flange.DN)])[0][0]

    #Эффективная ширина и расчетный диаметр прокладки
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


    def get_gasket_compliance(self):
        # Податливость прокладки ( для металических и асбометаллических y_g = 0 )
        y_g = (self.h_g * self.K_compress) / (float(self.E_g) * math.pi * self.get_gasket_params()[0] * self.b_g)
        return y_g


class Bolt(Part):

    def __init__(self, isgrooved: bool, type: str, flange1: object, material_id: int, temperature: int):
        super().__init__(material_id, temperature)
        self.isgrooved = isgrooved
        self.type = type
        self.diam = flange1.Nom_bolt_diam
        self.n = flange1.n
        self.E20 = db1.get_element_from_table('GOST_34233_4_2017_table_г1', '[25X1МФ]',
                                             ['[Расчетная температура болтов (шпилек)]'], ['20'])[0][0]
        self.E = db1.get_element_from_table('GOST_34233_4_2017_table_г1', '[25X1МФ]',
                                             ['[Расчетная температура болтов (шпилек)]'], [str(self.temperature)])[0][0]
        if self.isgrooved == True:
            self.f_b = db.get_element_from_table('Areas_of_bolts', self.diam, ['ID'], ['1'])[0][0]
        else:
            self.f_b = db.get_element_from_table('Areas_of_bolts', self.diam, ['ID'], ['0'])[0][0]

        self.alpha = db.get_element_from_table('linear_expansion_coefficients', 'temp_20_' + str(self.temperature), ['id'],
                                  [str(material_id)])[0][0]

        allowable_bolt_stress_mapping =  int(db.get_element_from_table('materials_bolts', 'mapping_nominal_allowable_stresses', ['id'],
                                  [str(self.material_id)])[0][0])

        self.allowable_bolt_stress = db.get_element_from_table('nominal_allowable_stresses', 'mat_' + str(allowable_bolt_stress_mapping), ['temperature'],
                                  [str(self.temperature)])[0][0]

        print(allowable_bolt_stress_mapping)


    def get_distance_between_the_bearing_surfaces(self, flange1, flange2):
        if flange1.type == '11' and flange2.type == '11':
            L_b0 = flange1.b + flange2.b

        return L_b0

    def get_bolt_compliance(self, flange1, flange2):
        if self.type == 'bolt':
            L_b = self.get_distance_between_the_bearing_surfaces(flange1, flange2) + 0.28 * int(self.diam[1:])
        elif self.type == 'pin':
            L_b = self.get_distance_between_the_bearing_surfaces(flange1, flange2) + 0.56 * int(self.diam[1:])

        y_b = L_b / (self.E20 * self.f_b * self.n)

        return y_b


class Washer(Part):

    def __init__(self, bolt, material_id: int, temperature: int,  params = None):
        super().__init__(material_id, temperature)
        self.d1 = db.get_element_from_table('gost_1371_78', 'd1_a', ['d_thread'], [str(bolt.diam)])[0][0]
        self.d2 = db.get_element_from_table('gost_1371_78', 'd1', ['d_thread'], [str(bolt.diam)])[0][0]
        self.s = db.get_element_from_table('gost_1371_78', 's', ['d_thread'], [str(bolt.diam)])[0][0]
        self.alpha = db.get_element_from_table('linear_expansion_coefficients', 'temp_20_' + str(self.temperature), ['id'], [str(material_id)])[0][0]







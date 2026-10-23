import sqlite3
from logging import raiseExceptions


class DatabaseConnection:


    def __init__(self, db_name='gost_pipe_db.sqlite'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # self.cursor.execute('''
        #
        #
        #                     ''')
        #
        # self.conn.commit()









        # self.cursor.execute(''' CREATE TABLE IF NOT EXISTS steel_elastic_modulus (
#                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                 steel_grade TEXT NOT NULL,
#                                 temp_20 REAL,
#                                 temp_100 REAL,
#                                 temp_200 REAL,
#                                 temp_300 REAL,
#                                 temp_400 REAL,
#                                 temp_450 REAL,
#                                 temp_500 REAL,
#                                 temp_550 REAL,
#                                 temp_600 REAL,
#                                 temp_650 REAL);
#         ''')
#         self.conn.commit()
#
#         self.cursor.execute(''' INSERT INTO steel_elastic_modulus
# (steel_grade, temp_20, temp_100, temp_200, temp_300, temp_400, temp_450, temp_500, temp_550, temp_600, temp_650)
# VALUES
# ('10, 20, 25, 30, 35, 40', 2.13, 2.10, 1.98, 1.90, 1.85, 1.82, 1.79, NULL, NULL, NULL),
# ('35Х, 40Х, 15ХМ, 30ХМА, 35ХМ', 2.18, 2.15, 2.08, 2.01, 1.92, 1.86, 1.79, NULL, NULL, NULL),
# ('12Х1МФ, 25Х1МФ, 25Х2М1Ф, 20Х1М1Ф1ТР, 20Х1М1Ф1БР, 20ХН3А', 2.15, 2.12, 2.08, 2.02, 1.94, 1.89, 1.83, 1.77, 1.70, NULL),
# ('20Х13, 15Х11МФ, 20Х12ВНМФ, 18Х11МНФБ, 1Х12Н2ВМФ, 18Х12ВМБФР', 2.28, 2.22, 2.13, 2.05, 1.93, 1.89, 1.84, 1.75, 1.70, NULL),
# ('12Х18Н10Т, 08Х18Н10Т, 08Х16Н13М2Б, 31Х19Н9МВБТ, ХН35ВТ', 2.05, 2.02, 1.97, 1.90, 1.81, 1.80, 1.73, 1.70, 1.65, 1.60),
# ('07Х16Н6', 2.08, 2.01, 1.92, 1.83, 1.73, 1.68, 1.62, NULL, NULL, NULL),
# ('07Х21Г7АН5', 2.13, 2.00, 1.93, 1.89, 1.83, NULL, NULL, NULL, NULL, NULL),
# ('10Х11Н22Т3МР (ЭИ696М)', 1.90, 1.81, 1.69, 1.58, 1.48, 1.42, 1.37, 1.33, 1.31, 1.30),
# ('Д16', 0.71, 0.67, 0.59, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
#         ''')
#         self.conn.commit()
        # self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
        #         Table6(DN TEXT, PN TEXT, D_m_r1 REAL, D_m_r2 REAL, D_n_r1 REAL, D_n_r2 REAL, d_1_r1 REAL, d_1_r2 REAL,
        #         b_r1 REAL, b_r2 REAL, H_r1 REAL, H_r2 REAL, H_1 REAL, capD_r1 REAL, capD_r2 REAL, D_1 REAL, d_r1 REAL, d_r2 REAL,
        #         n_r1 REAL, n_r2 REAL, Nom_bolt_diam_r1 TEXT, Nom_bolt_diam_r2 TEXT);''')
        # self.conn.commit()
        #
        # self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
        #         Table_и1(ID INTEGER PRIMARY KEY AUTOINCREMENT, type_and_material TEXT, m REAL, q_compress REAL, q_Allowed REAL, K_compress REAL, E_g REAL);''')
        # self.conn.commit()
        #
        #
        # # self.cursor.execute(''' DROP TABLE GOST_15180_86_table_4;''')
        # # self.conn.commit()
        #
        # self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
        #         GOST_15180_86_table_4(ID INTEGER PRIMARY KEY AUTOINCREMENT, DN TEXT, PN TEXT, D_cap INTEGER, d INTEGER, h INTEGER);''')
        # self.conn.commit()
        #
        # self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
        #         GOST_34233_4_2017_table_д1(ID INTEGER PRIMARY KEY AUTOINCREMENT, Bolt_type TEXT, M10 REAL, M12 REAL, M16 REAL, M20 REAL, M22 REAL, M24 REAL
        #                         , M27 REAL, M30 REAL, M36 REAL, M42 REAL, M48 REAL, M52 REAL, M56 REAL, M60 REAL, M64 REAL, M68 REAL);''')
        # self.conn.commit()
        #
        # self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
        #         Areas_of_bolts(ID INTEGER PRIMARY KEY AUTOINCREMENT, Bolt_type INTEGER, Description TEXT,  М10 REAL, М12 REAL, М16 REAL, М20 REAL, М22 REAL, М24 REAL
        #                         , М27 REAL, М30 REAL, М36 REAL, М42 REAL, М48 REAL, М52 REAL, М56 REAL, М60 REAL, М64 REAL, М68 REAL);''')
        # self.conn.commit()
        #
        # self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
        #         GOST_34233_4_2017_table_г1(ID INTEGER PRIMARY KEY AUTOINCREMENT, [Расчетная температура болтов (шпилек)] INTEGER,
        #     [35 40] INTEGER, [12Х18Н10Т, 10Х17Н13М2Т] INTEGER, [45Х14Н14В2М] INTEGER, [20X13] INTEGER, [35Х, 40Х ,38ХА ,37X12Н8Г8МБФ ,20ХНЗА] INTEGER,
        #     [30ХМА] INTEGER, [25X1МФ] INTEGER, [Алюминиевый сплав Д16] INTEGER);''')
        # self.conn.commit()

        # self.cursor.execute('''INSERT INTO GOST_34233_4_2017_table_г1([Расчетная температура болтов (шпилек)],
        #     [35 40], [12Х18Н10Т, 10Х17Н13М2Т], [45Х14Н14В2М], [20X13], [35Х, 40Х ,38ХА ,37X12Н8Г8МБФ ,20ХНЗА],
        #     [30ХМА], [25X1МФ], [Алюминиевый сплав Д16])
        #                        VALUES (20, 130, 110, 160, 195, 230, 230, 238, 83);''')
        # self.conn.commit()

        # self.cursor.execute('''INSERT INTO GOST_34233_4_2017_table_г1([Расчетная температура болтов (шпилек)],
        #     [35 40], [12Х18Н10Т, 10Х17Н13М2Т], [45Х14Н14В2М], [20X13], [35Х, 40Х ,38ХА ,37X12Н8Г8МБФ ,20ХНЗА],
        #     [30ХМА], [25X1МФ], [Алюминиевый сплав Д16])
        #                        VALUES (100, 126, 105, 150, 182, 230, 230, 227, 80);''')
        # self.conn.commit()

        # self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
        #         Categories_storage(CategoryID INTEGER PRIMARY
        #         KEY AUTOINCREMENT, Category TEXT)''')
        # self.conn.commit()
        # self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
        #         Budget_limitation(LimitPerDay REAL, LimitPerWeek REAL, LimitPerMonth REAL)''')
        # self.conn.commit()
        # self.cursor.execute('''INSERT INTO Table6(DN, PN, D_m_r1, D_m_r2, D_n_r1, D_n_r2, d_1_r1, d_1_r2, b_r1, b_r2,
        #                                           H_r1, H_r2, H_1, capD_r1, capD_r2, D_1, d_r1, d_r2,
        #         n_r1, n_r2, Nom_bolt_diam_r1, Nom_bolt_diam_r2)
        #                        VALUES ('DN_50', 'PN_40', 76,75,58,60.3,48,54.5,20,20,48,48,8,160,165,125,18,18,4,4,'M16','M16');''')
        # self.conn.commit()

        # self.cursor.execute('''INSERT INTO Table_и1(type_and_material, m, q_compress, q_allowed, K_compress, E_g)
        #                        VALUES ('Плоская неметаллическая прокладка из:паронита по ГОСТ 481 при толщине не более 2—3 мм',2.5, 20000000, 130000000,0.9,0.2);''')
        # self.conn.commit()

        # self.cursor.execute('''DELETE FROM GOST_15180_86_table_4;''')
        # self.conn.commit()
        #
        # self.cursor.execute('''INSERT INTO GOST_15180_86_table_4(DN, PN, D_cap, d, h)
        #                        VALUES ('40', '1_16', 75, 45, 2);''')
        # self.conn.commit()

        # self.cursor.execute('''INSERT INTO Areas_of_bolts(Bolt_type, Description, М10, М12, М16, М20, М22, М24,
        #                                                               М27 ,М30 ,М36 ,М42 ,М48 ,М52 ,М56 ,М60 ,М64 ,М68)
        #                        VALUES (1, 'Без проточки, мм2', 52.2, 76.2,144.0,
        #                                255, 281.5, 324, 430, 520, 760, 1045, 1376, 1652, 1905, 2227, 2520, 2888);''')
        # self.conn.commit()
        # #
        # self.cursor.execute('''INSERT INTO Areas_of_bolts(Bolt_type, Description,М10, М12, М16, М20, М22, М24,
        #                                                               М27 ,М30 ,М36 ,М42 ,М48 ,М52 ,М56 ,М60 ,М64 ,М68)
        #                        VALUES (2, 'С проточкой, мм2', 47.8, 70.9,133.0,
        #                                201, 254.5, 314, 380, 452, 707, 962, 1257, 1521, 1810, 2124, 2290, 2463);''')
        # self.conn.commit()


    def execute_request(self, request, params=None):
        if params is not None:
            self.cursor.execute(request, params)
            self.conn.commit()
        else:
            self.cursor.execute(request)
            self.conn.commit()
        return self.cursor.fetchall()

    def execute_request_many(self, request, params=None):
        if params is not None:
            self.cursor.executemany(request, params)
            self.conn.commit()
        else:
            self.cursor.executemany(request)
            self.conn.commit()
        return self.cursor.fetchall()

    def get_element_from_table(self, table_name: str, element_name: str, filters: list, filters_vals: list):

        request = '''SELECT ''' + element_name + ''' FROM '''+ table_name +''' WHERE '''

        for filter in filters:

            if filters[-1] != filter:
                request = request + filter + " = " + "'" + filters_vals[filters.index(filter)] + "'" + ' AND '
            else:
                request = request + filter + " = " + "'" + filters_vals[filters.index(filter)] + "'" + ' ;'

        result = self.execute_request(request)
        return result if result else None

    def close_connection(self):
        self.conn.close()

x = DatabaseConnection()
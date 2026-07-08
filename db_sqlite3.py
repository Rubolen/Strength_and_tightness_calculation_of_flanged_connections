import sqlite3
from logging import raiseExceptions


class DatabaseConnection:
    def __init__(self, db_name='GOST_33259—2015.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
                Table6(DN TEXT, PN TEXT, D_m_r1 REAL, D_m_r2 REAL, D_n_r1 REAL, D_n_r2 REAL, d_1_r1 REAL, d_1_r2 REAL,
                b_r1 REAL, b_r2 REAL, H_r1 REAL, H_r2 REAL, H_1 REAL, capD_r1 REAL, capD_r2 REAL, D_1 REAL, d_r1 REAL, d_r2 REAL,
                n_r1 REAL, n_r2 REAL, Nom_bolt_diam_r1 TEXT, Nom_bolt_diam_r2 TEXT);''')
        self.conn.commit()

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
                Table_и1(ID INTEGER PRIMARY KEY AUTOINCREMENT, type_and_material TEXT, m REAL, q_compress REAL, q_Allowed REAL, K_compress REAL, E_g REAL);''')
        self.conn.commit()


        # self.cursor.execute(''' DROP TABLE GOST_15180_86_table_4;''')
        # self.conn.commit()

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
                GOST_15180_86_table_4(ID INTEGER PRIMARY KEY AUTOINCREMENT, DN TEXT, PN TEXT, D_cap INTEGER, d INTEGER, h INTEGER);''')
        self.conn.commit()

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
                GOST_34233_4_2017_table_д1(ID INTEGER PRIMARY KEY AUTOINCREMENT, Bolt_type TEXT, M10 REAL, M12 REAL, M16 REAL, M20 REAL, M22 REAL, M24 REAL
                                , M27 REAL, M30 REAL, M36 REAL, M42 REAL, M48 REAL, M52 REAL, M56 REAL, M60 REAL, M64 REAL, M68 REAL);''')
        self.conn.commit()

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS
                GOST_34233_4_2017_table_д1(ID INTEGER PRIMARY KEY AUTOINCREMENT, Bolt_type TEXT, M10 REAL, M12 REAL, M16 REAL, M20 REAL, M22 REAL, M24 REAL
                                , M27 REAL, M30 REAL, M36 REAL, M42 REAL, M48 REAL, M52 REAL, M56 REAL, M60 REAL, M64 REAL, M68 REAL);''')
        self.conn.commit()
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

        # self.cursor.execute('''INSERT INTO GOST_34233_4_2017_table_д1(Bolt_type, M10, M12, M16, M20, M22, M24,
        #                                                               M27 ,M30 ,M36 ,M42 ,M48 ,M52 ,M56 ,M60 ,M64 ,M68)
        #                        VALUES ('Площадь поперечного сечения болтов (шпилек) без проточки, мм2', 52.2, 76.2,144.0,
        #                                255, 281.5, 324, 430, 520, 760, 1045, 1376, 1652, 1905, 2227, 2520, 2888);''')
        # self.conn.commit()
        #
        # self.cursor.execute('''INSERT INTO GOST_34233_4_2017_table_д1(Bolt_type, M10, M12, M16, M20, M22, M24,
        #                                                               M27 ,M30 ,M36 ,M42 ,M48 ,M52 ,M56 ,M60 ,M64 ,M68)
        #                        VALUES ('Площадь поперечного сечения болтов (шпилек) с проточкой, мм2', 47.8, 70.9,133.0,
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
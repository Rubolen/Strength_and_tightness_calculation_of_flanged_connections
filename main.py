from db_sqlite3 import DatabaseConnection
from calculations import Calculations
from body_units import Gasket, Flange, Bolt, Washer

# db = DatabaseConnection()
# db1 = DatabaseConnection('GOST_33259—2015.db')
# gs1 = Gasket('flat', (db.get_element_from_table('GOST_15180_86_table_4', 'D_cap', ['DN', 'PN'], ['40', '1_16'])[0][0],
#                                 db.get_element_from_table('GOST_15180_86_table_4', 'd', ['DN', 'PN'],['40', '1_16'])[0][0],
#                                 db.get_element_from_table('Table_и1', 'q_compress', ['type_and_material'],
#                                 ['Плоская неметаллическая прокладка из:паронита по ГОСТ 481 при толщине не более 2—3 мм'])[0][0],
#                                 db.get_element_from_table('Table_и1', 'm', ['type_and_material'],
#                                 ['Плоская неметаллическая прокладка из:паронита по ГОСТ 481 при толщине не более 2—3 мм'])[0][0]
#                       )
#              )

flange1 = Flange('Фланец стальной приварной встык', 6, 100, 50,40,)
flange2 = Flange('Фланец стальной приварной встык', 6, 100, 50,40,)
bolt = Bolt(True, 'bolt', flange1, 8, 100)
gasket = Gasket('flat', 'b', 3, flange1)
washer1 = Washer(bolt,1, [100])
washer2 = Washer(bolt,1, [100])



# bolt.get_bolt_stiffness(flange1, flange2)
# print(bolt.get_bolt_stiffness(flange1, flange2))


calc = Calculations(flange1, flange2, gasket, bolt, washer1, washer2)


print(calc.get_flange_connection_stiffness())
print(calc.forces_bolt_tension(100,100,100))

# print(bolt.f_b)
# print(gs1.get_gasket_stiffness())
# calc = Calculations(gasket = gs1)

# print(calc.forces_to_compress_gasket(10000))


# print(db.get_element_from_table('table6', 'H_1', ['DN', 'PN'], ['DN_50','PN_40'])
#       )
#
# print(db.get_element_from_table('Table_и1', 'm', ['type_and_material'],
#                                 ['Плоская неметаллическая прокладка из:паронита по ГОСТ 481 при толщине не более 2—3 мм'])
#       )
#
# print(db.get_element_from_table('GOST_15180_86_table_4', 'D_cap', ['DN', 'PN'],
#                                 ['40', '1_16'])
#       )
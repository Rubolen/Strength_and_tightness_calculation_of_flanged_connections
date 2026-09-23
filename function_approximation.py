import numpy as np
import csv
import matplotlib.pyplot as plt

class Approximation:


    def __init__(self, x, coef_type):
        self.x = x
        self.coef_type = coef_type
        self.graph_res_dict_T = self.get_graph_res(coef_type)


    def get_nearest_var(self):
        if self.coef_type == 'V':
            val_list = [0.1, 0.12, 0.14 , 0.16 ,0.18, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.25, 1.5, 2.0]
        else:
            val_list = [0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.25, 1.5, 2.0]

        delta_list = []
        for val in val_list:
            delta = abs(val - self.x)
            delta_list.append(delta)
        return str(val_list[np.argmin(delta_list)])

    def get_graph_res(self, coef_type):

        if coef_type == 'V':
            file_name = 'beta_V_values.csv'
        else:
            file_name = 'gost_graphs_T.csv'
        graph_res_dict = {
            'beta': (1.0, 1.1, 1.2, 1.25, 1.4, 1.6, 1.7, 1.8, 1.9, 2.2, 2.4, 2.5, 2.6, 3.0, 3.4, 3.7, 4.2, 4.7, 5.0)}

        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                temp_val = ''
                first_sep = True
                for str in row[0]:
                    if str != ';':
                        temp_val += str
                        row[0] = row[0][1:]
                    else:
                        if first_sep:
                            dict_key = temp_val
                            graph_res_dict[dict_key] = tuple()
                            row[0] = row[0][1:]
                            temp_val = ''
                            first_sep = False
                        else:
                            graph_res_dict[dict_key] += (float(temp_val),)
                            row[0] = row[0][1:]
                            temp_val = ''

        return graph_res_dict

    def func_fit(self):
        coeffs = np.polyfit(self.graph_res_dict_T['beta'], self.graph_res_dict_T[self.get_nearest_var()], 8)
        pred = np.poly1d(coeffs)
        return pred



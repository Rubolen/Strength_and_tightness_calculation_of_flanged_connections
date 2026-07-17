import numpy as np
import csv
import matplotlib.pyplot as plt

class Approximation:

    def __init__(self, beta, x):
        self.beta = beta
        self.x = x
        self.graph_res_dict_T = self.get_graph_res('gost_graphs_T.csv')


    def get_graph_res(self, file_name):

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

        # print(self.x, self.graph_res_dict_T)
        # print((self.graph_res_dict_T['beta'], self.graph_res_dict_T[self.x]))
        #
        #
        coeffs = np.polyfit(self.graph_res_dict_T['beta'], self.graph_res_dict_T[self.x], 8)
        print(coeffs)
        pred = np.polyval(coeffs, self.graph_res_dict_T['beta'])

        plt.plot(self.graph_res_dict_T['beta'], self.graph_res_dict_T[self.x], 'o', label='Исходные данные')
        plt.plot(self.graph_res_dict_T['beta'], pred, '-', label='Аппроксимация')
        plt.legend()
        plt.show()


x = Approximation(1, '1')
x.func_fit()
# print(x.graph_res_dict_T)


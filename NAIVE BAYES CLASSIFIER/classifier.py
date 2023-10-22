import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class Bayes_classifier():

    def __init__(self, path):
        self.data_file = pd.read_csv(path, delimiter=';').drop(columns='id')
        self.data_count = len(self.data_file)
        # self.class_label = self.data_file.columns.values[-1]
        self.class_label = self.data_file.columns[-1]

    def data_discretisation(self):

        # automatyczny podział
        columns_to_discretize = ['age', 'weight', 'height']

        for c in range(len(columns_to_discretize)):
            min_value = self.data_file[columns_to_discretize[c]].min()
            max_value = self.data_file[columns_to_discretize[c]].max()
            d = round((max_value-min_value)/5)
            columns_to_discretize[c] = [min_value + 1*d, min_value + 2*d, min_value + 3*d, min_value + 4*d, min_value + 5*d + 1]

        array_age = columns_to_discretize[0]
        array_weight = columns_to_discretize[1]
        array_height = columns_to_discretize[2]

        # ręczny podział    (ponieważ zdarzały się pojedyncze dane z wielkimi odchyłkami)
        array_ap_hi = [110, 120, 140, 160, 200]
        array_ap_lo = [70, 80, 90, 100, 110]

        att_array = ['age', array_age,
                     'weight', array_weight,
                     'height', array_height,
                     'ap_hi', array_ap_hi,
                     'ap_lo', array_ap_lo]


        for i in range(0, len(att_array), 2):
            self.discretisation_function(att_array[i], att_array[i+1])

        self.atts_set = self.data_file.drop(columns=self.class_label)
        self.classes_set = self.data_file[self.class_label]
        self.header = self.data_file.columns.values

        # self.classes = self.classes_set.unique()
        self.att_names = self.header[0:-1]

    def discretisation_function(self, att_name, ranges_vector):

        discrete_column = np.array(self.data_file[att_name])        # utworzenie roboczej kolumny danych

        for row in range(self.data_count):
            current_class = 0
            is_dicretized = False

            for level in ranges_vector:                             # dykretyzacja w określonych przedziałach
                if discrete_column[row] < level:
                    discrete_column[row] = current_class
                    is_dicretized = True
                    break
                else:
                    current_class += 1

            if not is_dicretized:
                discrete_column[row] = current_class
        
        self.data_file[att_name] = discrete_column.astype(int) 

    def split_data_sets(self, train_size):

        random_state = 42

        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.atts_set, self.classes_set, train_size=train_size, random_state=random_state)



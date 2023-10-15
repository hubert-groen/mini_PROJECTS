import pandas as pd
import numpy as np
from math import inf
from sklearn.model_selection import train_test_split

class Medical_classifier():

    # PRZYGOTOWANIE DANYCH

    def __init__(self, path, class_label, max_depth=4):

        self.data_file = pd.read_csv(path, delimiter=';').drop(columns='id')
        self.data_count = len(self.data_file)

        self.max_tree_depth = self.data_file.shape[1] - 1                   # tyle ile klas
        # self.max_tree_depth = 5

        self.class_label = class_label

        self.max_depth = max_depth

    def manage_data(self):

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
            self.dyskretyzacja(att_array[i], att_array[i+1])

        self.atts_set = self.data_file.drop(columns=self.class_label)
        self.classes_set = self.data_file[self.class_label]
        self.header = self.data_file.columns.values

        self.classes = self.classes_set.unique()
        self.att_names = self.header[0:-1]


        # podział na TRAIN, VALIDATE, TEST
        train_size = 0.6
        validation_size = 0.2
        test_size = 0.2
        random_state = 13
            
        self.X_train, X, self.Y_train, Y = train_test_split(self.atts_set, self.classes_set, test_size=train_size, random_state=random_state)
            
        remaining_size = 1 - train_size
        val_test_ratio = validation_size / remaining_size
        self.X_val, self.X_test, self.Y_val, self.Y_test = train_test_split(X, Y, test_size=val_test_ratio, random_state=31)

    def dyskretyzacja(self, att_name, ranges_vector):

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
        
        self.data_file[att_name] = discrete_column.astype(int)      # podmiana kolumny na nową (roboczą) w oryginalnych danych


              
    def change_depth(self, new):
        self.max_depth = new

    def add_tree(self, ID3_tree):
        self.tree = ID3_tree


    # TRENOWANIE ZBIORU

    def tree_node_construction(self, att_name, data_set, curr_depth):       # konstrukcja węzła drzewa, który reprezentuje podzbiór danych określony przez dany atrybut

        node = {}                                                           # korzeń w PODDRZEWIE będzie zawierał "słownik" swoich dzieci (ich wartości i etykiet)

        for value in data_set[att_name].unique():                           # iteracja po unikalnych wartościah
            subset = data_set.loc[data_set[att_name] == value]              # utworzenie podzbioru
            subset_size = subset.shape[0]
            class_counter = subset[self.class_label].value_counts()         # policzenie klas (unikalnych wartości) w danej kolumnie w pozbiorze

            if len(class_counter) == 1:                                     # jeśli podzbiór jest jednorodny - węzeł reprezentuje jedną klasę
                node[value] = class_counter.index[0]                        # dodanie do słownika węzeła o wartości tej klasy
                data_set = data_set[data_set[att_name] != value]            # usunięcie z oryginalnego zbioru danych wiersze z wartością 'value' w kolumnie 'att_name'

            elif curr_depth < self.max_depth:                               # jeśli podzbiór nie jest jednorodny
                node[value] = None                                          # dodaje do słownika węzeł o wartości 'value' i etykiecie 'unknown_class'

            else:                                                           # jeśli podzbiór nie jest jednorodny ALE przekroczono maksymalną głębokość drzewa
                node[value] = class_counter.idxmax()                        # zwrócenie klasy z największą liczbą wystąpień w podzbiorze - PRZECIWDZIAŁANIE PRZEUCZENIU

        return node, data_set                                               # węzeł (słownik) + zmodyfikowane dane (po usunięciu węzłów jednorodnych i "unknown class")

    def entropia_PODZBIORU(self, data_set, att_name):

        dataset_size = data_set.shape[0]                                    # rozmiar zbioru danych
        attributes_column = data_set[att_name].values                       # kolumna wartości atrybutu
        attributes_values = np.unique(attributes_column)                    # unikalne wartości dla atrybutu

        subsets_entropy = 0
        
        for value in attributes_values:

            subset = data_set.loc[data_set[att_name] == value]
            subset_size = subset.shape[0]                                       # rozmiar podzbioru
            entropy_SUBSET = self.entropia_ZBIORU(subset)                       # rekurencja: entropia podzbioru
            subset_gain = subset_size * entropy_SUBSET                          # zysk entropii = rozmiar * wartość
            subsets_entropy += subset_gain

        subsets_entropy = subsets_entropy / dataset_size                        # obliczenie entropii dla atrybuty na powstawie entropii wszystkich podzbiorów

        return subsets_entropy

    def entropia_ZBIORU(self, data_set):

        classes_set = data_set.iloc[:, -1]                                          # pobranie ostatniej kolumny z etykietami klas
        classes, classes_counter = np.unique(classes_set, return_counts=True)

        classes_set_size = classes_set.shape[0]                                     # liczba elementów w zbiorze

        classes_counter = classes_counter.astype(float) / classes_set_size          # normalizacja poszczególnych klas

        entropy = -np.sum(classes_counter * np.log2(classes_counter))               # entropia na podstawie liczebności poszczególnych klas

        return entropy

    def inf_gain(self, data_set):

        max_value = -inf
        max_value_attribute = None
        entropy_DATASET = self.entropia_ZBIORU(data_set)

        for a in self.att_names:
            entropy_SUBSET = self.entropia_PODZBIORU(data_set, a)
            value = entropy_DATASET - entropy_SUBSET

            if value > max_value:
                max_value = value
                max_value_attribute = a

        return max_value_attribute                                          # zwrócenie atrybutu, który najlepiej porządkuje dane (z największą entropią)

    def ID3(self, node, parent_node, recursion, current_depth, node_data):
     
        if node_data.shape[0] <= 1:                                                                   # jeśli zbiór danych jest pusty lub zawiera tylko jeden wiersz, zakończ budowanie drzewa
            return
        
        best_attribute = self.inf_gain(node_data)                                                     # wybranie atrybutu o największym Information Gain

        current_depth += 1
        next_root, node_data = self.tree_node_construction(best_attribute, node_data, current_depth)       # utworzenie poddrzewa z najlepszym atrybuitem jako korzeniem


        if recursion is True:                                                                         # sprawdzenie czy to pierwsze wywołanie ID3
            node[best_attribute] = next_root                                                          # jeśli tak to dodajemy korzeń
        else: 
            node[parent_node] = {best_attribute: next_root}                                           # a jeśli nie to dodajemy dziecko do węzła


        for next_node, next_class in next_root.items():                                               # TERAZ PRZECHODZIMY DO WĘZŁACH W UTWORZONYM PODDRZEWIE
            if next_class is None and current_depth <= self.max_depth:                                # jeśli węzeł nie ma jeszcze przypisanej klasy:
                subset = node_data[node_data[best_attribute] == next_node]                               
                self.ID3(next_root, next_node, False, current_depth, subset)                          # rekurencja ID3 - dla tego węzła (i jego podzbioru danych)


    def prediction_accuracy(self, X, y):

        predictions = []

        for _, row in X.iterrows():

            tree = self.tree
            
            while type(tree) is dict:                             # dopóki typ drzewa to słownik
                
                node = next(iter(tree))                           # pobieramy pierwszy klucz w słowniku
                attribute_value = row[node]                       # pobieramy wartość atrybutu z bieżącego wiersza danych testowych

                if attribute_value in tree[node]:                 # sprawdzamy, czy wartość atrybutu jest w drzewie
                    tree = tree[node][attribute_value]            # jeśli tak, to przechodzimy do węzła odpowiadającego wartości atrybutu

                else:
                    tree = None                                   # jeśli nie, to nie możemy dokonać predykcji dla tego wiersza i przerywamy pętlę
                    break
            
            predictions.append(tree)                              # dodajemy przewidywanie do listy przewidywań
        

        predictions = np.array(predictions)
        accuracy = np.sum(predictions == y) / y.shape[0]          # czyli: liczba poprawnie sklasyfikowanych etykiet / łączna liczba etykiet
        
        return accuracy                                           # zwracamy dokładność predykcji


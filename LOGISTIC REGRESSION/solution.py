import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class regression():
    def __init__(self, file_name):
        data = pd.read_csv(file_name)
        self.data = data.drop(['id', 'Unnamed: 32'], axis = 1)

    def manage_data(self):

        self.data.diagnosis = [1 if each == "M" else 0 for each in self.data.diagnosis]
        self.y = self.data.diagnosis.values

        x = self.data.drop(['diagnosis'], axis = 1)
        self.x = (x - np.min(x))/(np.max(x) - np.min(x))        # normalization

        self.cost_history = []
        self.train_history = []


    def split_data(self, input_train_size):

        x_train, x_test, y_train, y_test = train_test_split(self.x, self.y, train_size = 0.8, random_state = 43)

        self.x_train = x_train.T		# po transpozycji
        self.x_test = x_test.T		    # rows: attributes
        self.y_train = y_train.T	    # columns: data
        self.y_test = y_test.T



    def sigmoid(self, y):
        y_activatred = 1/(1 + np.exp(-y))
        return y_activatred


    def forward_propagation(self):
        
        y_updated = np.dot(self.weight.T, self.x_train) + self.bias     # przemnożenie danych przez wagi + bias = tabela etykiet
        y_activated = self.sigmoid(y_updated)                           # unormowanie wartości etykiet do zakresu (0, 1)
	

        loss = - self.y_train * np.log(y_activated) - (1 - self.y_train) * np.log(1 - y_activated)      # tablica strat (różnica pomiędzy ground_true a przewidywaniami z wagami)

        cost = (np.sum(loss)) / self.x_train.shape[1]                                                   # koszt (średnia wartość strat) / liczba przykładów w zbiorze

        self.cost_history.append(cost)

        return y_activated
        

    def backward_propagation(self, y_new):

        derivative_weight = (np.dot(self.x_train, (y_new - self.y_train).T)) / self.x_train.shape[1]    # wkład każdej cechy w gradient kosztu względem wag
                                                                                                        # / liczba przykładów - uśrednienie pochodnej
        derivative_bias = np.sum(y_new - self.y_train) / self.x_train.shape[1]                          # pochodna funkcji kosztu względem obciążenia

        return derivative_weight, derivative_bias
    

    def regression(self, learning_rate, iterations):

        attributes_number = self.x_train.shape[0]

        self.weight = np.full((attributes_number, 1), 0.01)         # macierz wag
        self.bias = 0.0                                             # obciażenie


        for i in range(iterations):

            y_updated = self.forward_propagation()

            derivative_weight, derivative_bias = self.backward_propagation(y_updated)
         
            self.weight = self.weight - learning_rate * derivative_weight
            self.bias = self.bias - learning_rate * derivative_bias

            train_accuracy = self.prediction(self.weight, self.bias, self.x_train, self.y_train)
            self.train_history.append(train_accuracy)


        # after all iterations we get best weight and bias values

        test_set_accuracy = self.prediction(self.weight, self.bias, self.x_test, self.y_test)

        return test_set_accuracy, self.cost_history, self.train_history
    

    import numpy as np

    def prediction(self, weight, bias, x_subset, y_subset):
        y_predicted = np.dot(weight.T, x_subset) + bias
        y_activated = self.sigmoid(y_predicted)

        predictions = np.zeros((1, x_subset.shape[1]))

        for i in range(y_activated.shape[1]):

            if y_activated[0, i] <= 0.5:
                predictions[0, i] = 0
            else:
                predictions[0, i] = 1

        correct_predictions = 0

        total_predictions = y_subset.shape[0]

        for i in range(total_predictions):
            if predictions[0, i] == y_subset[i]:
                correct_predictions += 1

        accuracy = (correct_predictions / total_predictions) * 100
        accuracy = round(accuracy, 2)
        return accuracy

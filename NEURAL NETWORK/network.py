import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from supporting_methods import ReLu, softmax, sigmoid


def manage_data(dataset):

    data = dataset["data"]
    labels = dataset["target"]

    data = data / data.max()
    labels = np.array(pd.get_dummies(labels))

    X_tv, X_test, Y_tv, Y_test = train_test_split(data, labels, train_size=0.6, random_state=42)

    X_train, X_validation, Y_train, Y_validation = train_test_split(X_tv, Y_tv, train_size=0.5, random_state=42)

    return X_train, Y_train, X_validation, Y_validation, X_test, Y_test



class Layer(object):
    def __init__(self, neurons_count, input_size):
        self.neurons_count = neurons_count
        self.input_size = input_size
        self.weights = np.random.rand(neurons_count, input_size) - 0.5
        self.biases = np.random.rand(neurons_count, 1) - 0.5

        # # stosowane przy używaniu 'momentum'
        # self.vd_weights = np.zeros(self.weights.shape)
        # self.vd_biases = np.zeros(self.biases.shape)

        '''
        layer.weights: size = neurons x input_size
        hidden activation: size = neurons x batch_size
        output: size = output_size x batch_size
        '''



class Network(object):
    def __init__(self, hidden_count, hidden_layer_size, learning_rate, momentum = 0.9):
        self.hidden_count = hidden_count
        self.hidden_layer_size = hidden_layer_size
        self.learning_rate = learning_rate
        # self.momentum = momentum

        self.hidden_act_fun = ReLu
        self.output_act_fun = softmax


    def forward_propagation(self, batch):

        pre_hidden = []
        hidden_activated = []

        curr_data = batch
        for i in range(self.hidden_count):
            data = (self.hidden_layers[i].weights.dot(curr_data) + self.hidden_layers[i].biases)
            pre_hidden.append(data)
            curr_data = self.hidden_act_fun(data)
            hidden_activated.append(curr_data)

        pre_output = self.output_layer.weights.dot(curr_data) + self.output_layer.biases
        output_activated = self.output_act_fun(pre_output)

        return pre_hidden, hidden_activated, pre_output, output_activated


    def backward_propagation(self, batch, pre_hidden, hidden_activated, pre_output, output_error):
        
        batch_size = output_error.shape[1]

        dz_out = output_error / batch_size * self.output_act_fun(pre_output, True)                  # obliczenie gradientu dla warstwy wyjściowej
        dw_out = 1 / batch_size * dz_out.dot(hidden_activated[-1].T)                                # obliczenie gradientu wag dla warstwy wyjściowej
        db_out = 1 / batch_size * np.sum(dz_out, 1, keepdims=True)                                  # obliczenie gradientu dla obciążenia w warstwie wyjściowej

        # inicjalizacja pustych list na gradienty i propagację wsteczną dla warstw ukrytych
        dz_layers = []
        dw_layers = []
        db_layers = []

        # propagacja wstecz po warstwach
        for layer in range(self.hidden_count - 1, -1, -1):
            if layer == self.hidden_count - 1:
                dz_layer = self.output_layer.weights.T.dot(dz_out) * self.hidden_act_fun(pre_hidden[layer], True)
            else:
                dz_layer = self.hidden_layers[layer + 1].weights.T.dot(dz_layers[0]) * self.hidden_act_fun(pre_hidden[layer], True)

            # obliczamy gradient wag dla danej warstwy
            if layer != 0:
                dw_layer = 1 / batch_size * dz_layer.dot(pre_hidden[layer].T)
            else:
                dw_layer = 1 / batch_size * dz_layer.dot(batch.T)

            # obliczamy gradient obciążenia dla danej warstwy
            db_layer = 1 / batch_size * np.sum(dz_layer, 1, keepdims=True)

            dz_layers.insert(0, dz_layer)
            dw_layers.insert(0, dw_layer)
            db_layers.insert(0, db_layer)

        # gradienty wag i obciążeń dla warstwy wyjśniowej i warstw ukrytych
        return dw_out, db_out, dw_layers, db_layers

    # different version of updating parametrs with 'momentum' parameter
    # region
    # def update_parameters_with_momentum(self, output_dWs, output_dBs, layers_dWs, layers_dBs):

    #     for i in range(self.hidden_count):

    #         self.hidden_layers[i].vd_weights = (self.momentum * self.hidden_layers[i].vd_weights + (1.0 - self.momentum) * layers_dWs[i])
    #         self.hidden_layers[i].weights -= (self.learning_rate * self.hidden_layers[i].vd_weights)

    #         self.hidden_layers[i].vd_biases = self.momentum * self.hidden_layers[i].vd_biases + (1.0 - self.momentum) * np.reshape(layers_dBs[i], (self.hidden_layers[i].neurons_count, 1))
    #         self.hidden_layers[i].biases -= (self.learning_rate * self.hidden_layers[i].vd_biases)

    #     self.output_layer.vd_weights = (self.momentum * self.output_layer.vd_weights + (1.0 - self.momentum) * output_dWs)
    #     self.output_layer.weights -= self.learning_rate * self.output_layer.vd_weights

    #     self.output_layer.vd_biases = self.momentum * self.output_layer.vd_biases + (1.0 - self.momentum) * np.reshape(output_dBs, (self.output_layer.neurons_count, 1))
    #     self.output_layer.biases -= self.learning_rate * self.output_layer.vd_biases
    # endregion


    # aktualizacja wag i obciążeń w warstwach ukrytych i w warstwie wyjściowej
    def update_parameters(self, output_dWs, output_dBs, layers_dWs, layers_dBs):    

        for i in range(self.hidden_count):
            self.hidden_layers[i].weights -= self.learning_rate * layers_dWs[i]
            self.hidden_layers[i].biases -= self.learning_rate * layers_dBs[i]

        self.output_layer.weights -= self.learning_rate * output_dWs
        self.output_layer.biases -= self.learning_rate * output_dBs


    def create_layers(self, input_size, output_size):

        hidden_layers = []
        for i in range(self.hidden_count):
            if i == 0:
                layer = Layer(self.hidden_layer_size, input_size)
            else:
                layer = Layer(self.hidden_layer_size, self.hidden_layer_size)
            hidden_layers.append(layer)

        output_layer = Layer(output_size, self.hidden_layer_size)
        return hidden_layers, output_layer


    def train(self, epochs, batch_size, train_data, train_labels, valid_data, valid_labels):

        input_size = train_data.shape[1]                # 64 = 8x8 pixels of an image
        output_size = train_labels.shape[1]             # 10 = all digits

        # creation of hidden layers and output layer
        self.hidden_layers, self.output_layer = self.create_layers(input_size, output_size)

        train_accs = []
        train_losses = []
        valid_accs = []
        valid_losses = []

        for epoch in range(epochs):
            

            permutation = np.random.permutation(train_data.shape[0])
            train_data = train_data[permutation, :]
            train_labels = train_labels[permutation, :]

            for i in range(batch_size, len(train_data), batch_size):
                data_sample = train_data[i - batch_size : i].T
                sample_labels = train_labels[i - batch_size : i].T

                pre_hidden, hidden_activated, pre_output, output_activated = self.forward_propagation(data_sample)

                dw_out, db_out, dw_layers, db_layers = self.backward_propagation(data_sample, pre_hidden, hidden_activated, pre_output, 2 * (output_activated - sample_labels))

                self.update_parameters(dw_out, db_out, dw_layers, db_layers)

            train_acc, train_loss = self.evaluate(train_data, train_labels)
            train_accs.append(train_acc)
            train_losses.append(train_loss)

            valid_acc, valid_loss = self.evaluate(valid_data, valid_labels)
            valid_accs.append(valid_acc)
            valid_losses.append(valid_loss)

            print(f"\nEPOCH {epoch + 1} / {epochs}     accuracy = {round(train_acc, 2)} %")

        return train_accs, train_losses, valid_accs, valid_losses
    

    def evaluate(self, data, labels):

        _, _, _, output_activated = self.forward_propagation(data.T)
        predictions = np.argmax(output_activated, axis = 0)
        accuracy = (np.sum(predictions == np.argmax(labels, axis=1)) / labels.shape[0]) * 100

        batch_size = labels.shape[0]
        error = np.power(labels.T - output_activated, 2)
        loss = np.sum(error) / batch_size                   # loss can be called 'mean error'

        return accuracy, loss


    def test_prediction(self, data, labels, index):

        current_image = data[index, :]
        current_image = np.reshape(current_image, (1, current_image.size))
        _, _, _, output_activated = self.forward_propagation(current_image.T)
        prediction = np.argmax(output_activated, axis = 0)
        print(f'prediction:   {prediction[0]}')

        label = np.argmax(labels[index, :])
        print(f'label:        {label}\n')

        current_image = np.reshape(current_image, (int(np.sqrt(data.shape[1])), int(np.sqrt(data.shape[1]))),) * 16
        plt.gray()
        plt.imshow(current_image, interpolation="nearest")
        plt.show()


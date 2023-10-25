from network import Network, manage_data
from supporting_methods import ReLu, softmax, sigmoid
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import numpy as np



dataset = load_digits()

X_train, Y_train, X_validation, Y_validation, X_test, Y_test = manage_data(dataset)



net = Network(hidden_count = 3, hidden_layer_size = 64, learning_rate = 0.1)



train_accuuracies, train_losses, validation_accuracies, validation_losses = net.train(epochs = 500, batch_size = 32, 
                                                                                    train_data = X_train, train_labels = Y_train, 
                                                                                    valid_data = X_validation, valid_labels = Y_validation)





# PLOTS
# region
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

ax1.plot(range(len(train_accuuracies)), train_accuuracies, 'b', label='training data')
ax1.plot(range(len(validation_accuracies)), validation_accuracies, 'r', label='validation data')
ax1.legend(loc='upper left')
ax1.set_xlabel('EPOCHS')
ax1.set_ylabel('ACCURACY')
ax1.set_title('ACCURACY over iterations')

ax2.plot(range(len(train_losses)), train_losses, 'b', label='training data')
ax2.plot(range(len(validation_losses)), validation_losses, 'r', label='validation data')
ax2.legend(loc='upper left')
ax2.set_xlabel('EPOCHS')
ax2.set_ylabel('LOSS')
ax2.set_title('LOSS over iterations')

plt.show()
# endregion

test_accuracy, test_loss = net.evaluate(X_test, Y_test)

print("---------------------------------------\n")
print(f"TEST ACCURACY = {round(test_accuracy, 2)} %")


print('\n\nRANDOM SAMPLE TEST:')
net.test_prediction(X_test, Y_test, np.random.randint(1, X_test.shape[0] - 1))

# net.test_prediction(X_test, Y_test, 14)
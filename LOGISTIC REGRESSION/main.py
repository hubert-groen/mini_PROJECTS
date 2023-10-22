import matplotlib.pyplot as plt
from solution import regression

def plot(cost, train_acc):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 4))

    ax1.plot(cost)
    ax1.set_xlabel("ITERATIONS")
    ax1.set_ylabel("COST")
    ax1.set_title("COST over iterations")

    ax2.plot(train_acc)
    ax2.set_xlabel("ITERATIONS")
    ax2.set_ylabel("ACCURACY")
    ax2.set_title("TRAINING SET ACCURACY over iterations")

    plt.show()


model = regression("data.csv")

model.manage_data()

model.split_data(0.8)

test_set_accuracy, cost, train_updates = model.regression(0.2, 1000)



print(f"Acurracy of TEST SET = {test_set_accuracy} %")

plot(cost, train_updates)


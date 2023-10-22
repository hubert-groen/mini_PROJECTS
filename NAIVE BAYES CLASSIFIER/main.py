from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from classifier import Bayes_classifier


def main():

    data_path = 'cardio_train.csv'

    model = Bayes_classifier(data_path)
    model.data_discretisation()
    model.split_data_sets(0.8)

    X_train_0 = model.X_train[model.Y_train == 0]
    X_train_1 = model.X_train[model.Y_train == 1]

    value_counts_dict_0 = {}
    for column in X_train_0.columns:

        value_counts = X_train_0[column].value_counts()
        value_counts_dict_0[column] = value_counts


    value_counts_dict_1 = {}
    for column in X_train_1.columns:

        value_counts = X_train_1[column].value_counts()
        value_counts_dict_1[column] = value_counts

    
    def calculate_single_record_prob(data_row):

        yes = 1

        for a in model.att_names:

            test_value = data_row[a]
            num_in_dict = value_counts_dict_1[a]
            fraction = num_in_dict / len(X_train_1)
            yes = yes * fraction

        yes = yes * (len(X_train_1) / len(model.X_train))

        print(f"yes = {yes}")


        no = 1

        for a in model.att_names:

            test_value = data_row[a]
            num_in_dict = value_counts_dict_0[a][test_value]
            fraction = num_in_dict / len(X_train_0)
            no = no * fraction

        no = no * (len(X_train_0) / len(model.X_train))

        print(f"no = {no}")

        percentage = yes / (yes+no)

        print(f"percentage = {percentage}")

        if percentage >= 0.5:
            return 1
        else:
            return 0


    success = 0

    # for i in range(len(model.X_test)):
    for i in range(1):

        single_record = model.X_test.iloc[i]

        prediciton = calculate_single_record_prob(single_record)

        if prediciton == model.Y_test.iloc[i]:
            success += 1

    print(f"Overal prediction accuracy = {(success/len(model.X_test))*100} %")

    # single_record = model.X_test.iloc[1]


    # print(single_record['gender'])





if __name__ == '__main__':
    main()



# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import GaussianNB
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# # 1. Wczytaj dane z odpowiednim separatorem
# data = pd.read_csv('cardio_train.csv', sep=';')

# # 2. Przygotuj dane
# X = data.drop('cardio', axis=1)  # Funkcje (cechy)
# y = data['cardio']  # Zmienna docelowa

# # Podział danych na zbiór treningowy i testowy
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # 3. Zastosuj model Gaussian Naive Bayes
# naive_bayes_classifier = GaussianNB()
# naive_bayes_classifier.fit(X_train, y_train)

# # 4. Dokonaj predykcji na zbiorze testowym
# y_pred = naive_bayes_classifier.predict(X_test)

# # 5. Ocen dokładność modelu
# accuracy = accuracy_score(y_test, y_pred)
# print("Dokładność modelu: {:.2f}%".format(accuracy * 100))

# # Inne metryki oceny modelu
# print("\nMacierz błędów:")
# print(confusion_matrix(y_test, y_pred))

# print("\nRaport klasyfikacji:")
# print(classification_report(y_test, y_pred))

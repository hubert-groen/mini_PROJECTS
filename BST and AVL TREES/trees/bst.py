import matplotlib.pyplot as plt
import random
# klasa węzła, zawiera jego wartość, oraz wartości po prawej i lewej (na dole)


class Node:
    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None

# klasa drzewa


class BST:
    def __init__(self):
        self.root = None

    def insert_list(self, list):
        for element in list:
            self.insert(element)

    def search_list(self, list):
        for element in list:
            self.search(element)

    def delete_list(self, list):
        for element in list:
            self.delete(element)

    def insert(self, value):

        # jeśli drzewo jest puste
        if self.root is None:
            self.root = Node(value)

        # jeśli drzewo już ma węzły
        else:
            current = self.root

            # iterujemy po kolejnych węzłach:
            # dopóki nie znajdziemy pustego węzła terminalnego, to idzizemy dalej (w prawo lub lewo)
            while current is not None:
                if value < current.value:
                    if current.left is None:
                        current.left = Node(value)
                        return
                    else:
                        current = current.left

                if value > current.value:
                    if current.right is None:
                        current.right = Node(value)
                        return
                    else:
                        current = current.right

    def search(self, value):
        current_search = self.root      # klasa node jest już "wywołana w funkcji wstawianie"

        while current_search is not None:
            if current_search.value == value:
                return True

            elif value < current_search.value:
                current_search = current_search.left

            else:
                current_search = current_search.right
        return False

    def delete(self, value):
        rodzic = None
        current_check = self.root

        # poszukiwanie węzła do usunięcia w pętli
        while current_check is not None:
            if current_check.value == value:            # jeśli zleżliśmy wartość to przerywamy
                break
            elif value < current_check.value:           # jeśli nie to idziemy w lewo
                rodzic = current_check
                current_check = current_check.left
            else:                                       # lub w prawo
                rodzic = current_check
                current_check = current_check.right

        # jeśli po wykonaniu pętli, element nie zostanie znaleziony, znaczy że nie ma czego usuwać
        if current_check is None:
            return

        # węzeł do usunięcia NIE MA DZIECI (jest terminalny)
        if current_check.left is None and current_check.right is None:
            # przypadek kiedy usuwamy jedyny węzeł w drzewie
            if rodzic is None:
                self.root = None
            # usuwanie węzła terminalnego - lewego od rodzica
            elif rodzic.left == current_check:
                rodzic.left = None
            else:                                                            # usuwanie węzła terminalnego - prawego od rodzica
                rodzic.right = None

        # węzeł do usunięcia NIE MA LEWEGO DZIECKA
        elif current_check.left is None:
            # jeśli to korzeń to zastępuje go jedyne dziecko (prawe)
            if rodzic is None:
                self.root = current_check.right
            elif rodzic.left == current_check:
                rodzic.left = current_check.right
            else:                                                            # rodzic.right == current_check
                rodzic.right = current_check.right

        # węzeł do usunięcia NIE MA PRAWEGO DZIECKA
        # jeśli to korzeń to zastępuje go jedyne dziecko (lewe)
        elif current_check.right is None:
            if rodzic is None:
                self.root = current_check.left
            elif rodzic.left == current_check:
                rodzic.left = current_check.left
            else:
                rodzic.right = current_check.left

        # węzeł do usunięcia MA DWOJE DZIECI (prawe i lewe)
        else:
            successor_parent = current_check
            # następcą będzie pierwszy z prawej
            successor = current_check.right

            while successor.left is not None:                       # chyba, że ma on mniejsze dzieci
                successor_parent = successor
                successor = successor.left

            # zamiana wartości usuwanej na zastępce (co to wyżej)
            current_check.value = successor.value

            # trzeba jeszcze usunąć zastępce z pierwotnego miejsca (żeby się nie duplikował)
            if successor_parent.left == successor:
                # jeśli zastępca ma prawego brata, do "zamieniamy go w tego brata"
                successor_parent.left = successor.right
            else:
                # jeśli zastępca nie ma swoich dzieci
                successor_parent.right = successor.right

    def prepare_data(self, node, ax, x, y, dx, dy):

        # jeśli węzeł nie istnieje to nie ma czego rysować
        if node is None:
            return

        # rysowanie lewego poddrzewa
        if node.left is not None:
            # linia of węzła do lewego dziecka
            ax.plot([x-dx, x], [y-dy, y], 'b')
            # rekurenkcja - lewe podrzewo (przesuwanie się w lewo w dół)
            self.prepare_data(node.left, ax, x-dx, y-dy, dx/2, dy+10)

        # rysowanie prawego poddrzewa
        if node.right is not None:
            # linia of węzła do prawego dziecka
            ax.plot([x+dx, x], [y-dy, y], 'b')
            # rekurenkcja - prawe podrzewo (przesuwanie się w prawo w dół)
            self.prepare_data(node.right, ax, x+dx, y-dy, dx/2, dy+10)

        # rysowanie węzła
        ax.text(x, y, str(node.value), fontsize=12, ha='center', va='center',
                bbox=dict(facecolor='grey', alpha=0.2, edgecolor='grey'))

    def draw(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')      # proporcje osi = równe
        ax.axis('off')
        ax.set_xlim([-50, 50])
        ax.set_ylim([-50, 50])
        # funkcja rysująca (od korzenia)
        self.prepare_data(self.root, ax, 0, 40, 20, 10)
        plt.show()


def main():

    bst = BST()

    bst.insert(6)
    bst.insert(21212)
    bst.insert(10)
    bst.insert(3)
    bst.insert(4)
    bst.insert(7)
    bst.insert(12)
    bst.insert(11)
    bst.insert(13)

    print(bst.search(6))  # True
    print(bst.search(18))  # False

    bst.delete(12)

    # szukanie tego co zostało usunięte
    print(bst.search(12))  # False

    bst.draw()


if __name__ == "__main__":
    main()

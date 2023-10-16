# Python code to insert a node in AVL tree
import random
import matplotlib.pyplot as plt


class TreeNode(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1


class AVL(object):

    def __init__(self) -> None:
        self.root = None

    def insert_list(self, list):
        for element in list:
            self.insert(element)

    def search_list(self, list):
        for element in list:
            self.search(element)

    def insert(self, key):
        self.root = self.insert_helper(self.root, key)

    def insert_helper(self, root, key):

        # Step 1 - Perform normal BST
        if not root:
            return TreeNode(key)
        elif key < root.val:
            root.left = self.insert_helper(root.left, key)
        else:
            root.right = self.insert_helper(root.right, key)

        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        # Step 3 - Get the balance factor
        balance = self.get_balance(root)

        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and key < root.left.val:
            return self.right_rotate(root)

        # Case 2 - Right Right
        if balance < -1 and key > root.right.val:
            return self.left_rotate(root)

        # Case 3 - Left Right
        if balance > 1 and key > root.left.val:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Case 4 - Right Left
        if balance < -1 and key < root.right.val:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        """
            |               |
            x               y
           / \             / \
          a   y    =>     x   c
             / \         / \
            b   c       a   b
        """
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        # Return the new root
        return y

    def right_rotate(self, z):
        """
            |               |
            x               y
           / \             / \
          y   a    =>     b   x
         / \                 / \
        b   c               c   a
        """
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        # Return the new root
        return y

    def get_height(self, root):
        if not root:
            return 0

        return root.height

    def get_balance(self, root):
        if not root:
            return 0

        return self.get_height(root.left) - self.get_height(root.right)

    def prepare_data(self, node, ax, x, y, dx, dy):

        if node is None:
            return

        if node.left is not None:
            ax.plot([x-dx, x], [y-dy, y], 'b')
            self.prepare_data(node.left, ax, x-dx, y-dy, dx/2, dy+10)

        if node.right is not None:
            ax.plot([x+dx, x], [y-dy, y], 'b')
            self.prepare_data(node.right, ax, x+dx, y-dy, dx/2, dy+10)

        ax.text(x, y, str(node.val), fontsize=12, ha='center', va='center',
                bbox=dict(facecolor='grey', alpha=0.2, edgecolor='grey'))

    def draw_tree(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_xlim([-50, 50])
        ax.set_ylim([-50, 50])
        self.prepare_data(self.root, ax, 0, 40, 20, 10)
        plt.show()

    def search(self, value):
        current_search = self.root

        while current_search is not None:
            if current_search.val == value:
                return True

            elif value < current_search.val:
                current_search = current_search.left

            else:
                current_search = current_search.right
        return False


if __name__ == "__main__":
    myTree = AVL()
    root = None

    nums = random.sample(range(1, 300000), 20)
    root = None
    for num in nums:
        myTree.insert(num)
    myTree.insert(123)

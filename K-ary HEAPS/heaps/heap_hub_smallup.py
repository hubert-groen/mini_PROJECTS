import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class HeapV:
    def __init__(self, degree) -> None:
        self.degree = degree
        self.heap_list = []
        self.last_index = -1

    def insert_list(self, elements_list):
        for element in elements_list:
            self.insert_element(element)

    def delete_n(self, number):
        for _ in range(number):
            self.delete_top_element()

    def insert_element(self, element):
        self.heap_list.append(element)
        self.last_index += 1
        self.heapify_up(self.last_index)

    def delete_top_element(self):
        if self.last_index == -1:
            return None
        root = self.heap_list[0]
        self.heap_list[0] = self.heap_list[self.last_index]
        self.heap_list.pop()
        self.last_index -= 1
        self.heapify_down(0)
        return root

    def heapify_up(self, index):
        if index == 0:
            return
        parent_index = (index - 1) // self.degree
        if self.heap_list[parent_index] > self.heap_list[index]:
            self.heap_list[parent_index], self.heap_list[index] = self.heap_list[index], self.heap_list[parent_index]
            self.heapify_up(parent_index)

    def heapify_down(self, index):
        min_index = index
        for i in range(1, self.degree + 1):
            child_index = self.degree * index + i
            if child_index <= self.last_index and self.heap_list[child_index] < self.heap_list[min_index]:
                min_index = child_index
        if min_index != index:
            self.heap_list[min_index], self.heap_list[index] = self.heap_list[index], self.heap_list[min_index]
            self.heapify_down(min_index)


def draw_heap(heap):
    G = nx.Graph()
    node_labels = {}
    node_colors = []
    levels = {}  # dictionary to keep track of node levels
    max_level = 0  # to keep track of the maximum level of the heap

    for i, elem in enumerate(heap.heap_list):
        level = 0 if i == 0 else levels[(i - 1) // heap.degree] + 1
        levels[i] = level
        max_level = max(max_level, level)

        G.add_node(i, label=str(elem))
        node_labels[i] = str(elem)

        if i > 0:
            parent_index = (i - 1) // heap.degree
            G.add_edge(parent_index, i)

        # koloruj korzeń na czerwono
        if i == 0:
            node_colors.append('red')
        else:
            node_colors.append('white')

    # calculate the position of nodes at each level
    pos = {}
    nodes_at_level = {}
    node_spacing = 0.05
    level_height = 0.15
    for level in range(max_level + 1):
        nodes_at_level[level] = [n for n in G.nodes() if levels[n] == level]
        nodes_count = len(nodes_at_level[level])
        level_width = node_spacing * (nodes_count - 1)
        x_pos = np.linspace(-level_width/2, level_width/2, nodes_count)
        pos.update({node: (x_pos[i], -level*level_height) for i, node in enumerate(nodes_at_level[level])})

    # plot the heap
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=False, node_size=500, node_color=node_colors, edgecolors='black', linewidths=1, arrowsize=20)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=15, font_weight='bold')
    plt.axis('off')
    # plt.show()



def main():
    heap = HeapV(7)
    heap.insert_list([31, 5, 10, 18, 14, 9, 6, 17, 1, 11])
    draw_heap(heap)

    


if __name__ == "__main__":
    main()

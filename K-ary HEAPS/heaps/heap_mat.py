import matplotlib.pyplot as plt
import math
from heapq import heappush, heappop
import networkx as nx
import numpy as np

MAX_SIZE = 10000
TOP_INDEX = 0


class Heap:
    def __init__(self, degree) -> None:
        self.degree = degree
        self.heap_list = [None]*MAX_SIZE
        self.last_index = -1

    def insert_list(self, elements_list):
        for element in elements_list:
            self.insert_element(element)

    def delete_n(self, number):
        for _ in range(number):
            self.delete_top_element()

    def insert_element(self, element):
        if self.last_index != MAX_SIZE:
            self.last_index += 1
            self.heap_list[self.last_index] = element
            self.heapify_all()

    def delete_top_element(self):
        if self.last_index > -1:
            self.heap_list[TOP_INDEX] = self.heap_list[self.last_index]
            self.heap_list[self.last_index] = None
            self.last_index -= 1
            self.heapify_all()

    def heapify_all(self):
        for element_index in range(self.last_index+1, -1, -1):
            self.heapify(element_index)

    def heapify(self, parent_index):
        for child_number in range(1, self.degree+1):
            child_index = parent_index * self.degree + child_number
            if child_index <= self.last_index:
                if self.heap_list[parent_index] < self.heap_list[child_index]:
                    self.replace_elements(parent_index, child_index)

    def replace_elements(self, index_1, index_2):
        temp = self.heap_list[index_1]
        self.heap_list[index_1] = self.heap_list[index_2]
        self.heap_list[index_2] = temp


def draw_heap(heap):
    G = nx.Graph()
    node_labels = {}
    node_colors = []
    levels = {}  # dictionary to keep track of node levels
    max_level = 0  # to keep track of the maximum level of the heap

    for i, elem in enumerate(heap.heap_list[:heap.last_index]):
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
        pos.update({node: (x_pos[i], -level*level_height)
                   for i, node in enumerate(nodes_at_level[level])})

    # plot the heap
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=False, node_size=500, node_color=node_colors,
            edgecolors='black', linewidths=1, arrowsize=20)
    nx.draw_networkx_labels(G, pos, labels=node_labels,
                            font_size=15, font_weight='bold')
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    heap = Heap(5)
    heap.insert_element(2)
    heap.insert_element(5)
    heap.insert_element(6)
    heap.insert_element(19)
    heap.insert_element(31)
    heap.insert_element(51)
    heap.insert_element(4)
    heap.insert_element(8)
    heap.insert_element(12)
    heap.insert_element(100)
    heap.insert_element(31)
    heap.insert_element(51)
    # heap.insert_element(11)
    # heap.insert_element(1)
    # heap.insert_element(3)
    # heap.delete_top_element()
    # heap.delete_top_element()
    draw_heap(heap)
    print(heap.heap_list[:20])

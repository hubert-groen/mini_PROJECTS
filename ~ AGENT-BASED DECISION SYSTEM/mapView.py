import tkinter as tk
import time
import threading

class MapView(threading.Thread):
    def __init__(self, matrix_size = 20, start_postions_map = {}):
        self.rectangles = {}
        self.matrix_size = matrix_size
        self.matrix = [[0] * matrix_size for _ in range(matrix_size)]
        self.root = tk.Tk()
        self.root.title("Matrix Display")

        # Create a canvas
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        # Calculate cell size
        self.cell_size = 400 / len(self.matrix)

        # Draw the grid
        for i in range(len(self.matrix) + 1):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, 400)
            self.canvas.create_line(0, i * self.cell_size, 400, i * self.cell_size)
        for id, position in start_postions_map.items():
            x, y = position
            # self.matrix[x][y] = 1
            self.rectangles[id] = self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill="red")
        
        threading.Thread.__init__(self)
    
    def run(self):
        self.root.mainloop()

    def moveAmbulance(self, id, newPosition):
        rect = self.rectangles[id]
        x, y = newPosition
        self.canvas.coords(rect, x,y, x + self.cell_size, y + self.cell_size)
        



if __name__ == "__main__":

   
    karetka_1 = [2, 2]
    karetka_2 = [15, 6]

    map = MapView(start_postions_map={1:karetka_1, 2:karetka_2})
    map.run()
    print("Poczekam 3 sekundy...")
    time.sleep(3)
    print("Minęło 3 sekundy!")
    map.moveAmbulance(1,[3,3])    

import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    def __init__(self, grid):
        self.grid = grid
        self.fig, self.ax = plt.subplots()  # Kreiramo samo jedan prozor
        self.img = None  # Držimo referencu na sliku koju ćemo ažurirati

    def visualize(self, step):
        """
        Vizualizacija trenutnog stanja mreže pomoću Matplotlib.
        """
        color_map = {
            'D': 'green',  # Drvo
            'G': 'red',  # Gori
            'P': 'gray',  # Prazno
            'O': 'black'  # Prepreka
        }

        grid_data = np.zeros((self.grid.size, self.grid.size, 3))

        for i in range(self.grid.size):
            for j in range(self.grid.size):
                cell = self.grid.grid[i][j]
                color = color_map.get(cell.state, 'white')
                if color == 'green':  # Drvo
                    grid_data[i, j] = [0, 1, 0]
                elif color == 'red':  # Gori
                    grid_data[i, j] = [1, 0, 0]
                elif color == 'gray':  # Prazno
                    grid_data[i, j] = [0.5, 0.5, 0.5]
                elif color == 'black':  # Prepreka
                    grid_data[i, j] = [0, 0, 0]

        if self.img is None:
            self.img = self.ax.imshow(grid_data)  # Prvi put kreiramo sliku
        else:
            self.img.set_data(grid_data)  # Ažuriramo postojeću sliku

        self.ax.set_title(f"Simulacija širenja požara - Korak {step}")
        plt.draw()  # Prikazuje promjene u prozoru
        plt.pause(0.1)  # Pauza kako bi se prozor ažurirao

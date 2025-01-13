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
        Dodali smo boje koje zavise od temperature ćelija.
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

                # Dodavanje temperaturnih varijacija u boji
                if cell.state == 'G':  # Požar
                    grid_data[i, j] = [1, 0, 0]  # Požar u crvenoj
                elif cell.state == 'D':  # Drvo
                    # Boja zavisi od temperature ćelije
                    temp_ratio = min(cell.temperature / 100, 1)  # Normalizacija temperature
                    grid_data[i, j] = [0, temp_ratio, 0]  # Zelena sa rastućim intenzitetom
                elif cell.state == 'O':  # Prepreka
                    grid_data[i, j] = [0, 0, 0]  # Crna za prepreke
                else:
                    grid_data[i, j] = [0.5, 0.5, 0.5]  # Prazna ćelija u sivoj

        if self.img is None:
            self.img = self.ax.imshow(grid_data)  # Prvi put kreiramo sliku
        else:
            self.img.set_data(grid_data)  # Ažuriramo postojeću sliku

        self.ax.set_title(f"Simulacija širenja požara - Korak {step}")
        plt.draw()  # Prikazuje promjene u prozoru
        plt.pause(0.1)  # Pauza kako bi se prozor ažurirao

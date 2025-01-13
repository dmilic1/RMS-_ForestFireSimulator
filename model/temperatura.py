import random


class Temperatura:
    def __init__(self, vanjska_temperatura):
        self.vanjska_temperatura = vanjska_temperatura  # Vanjska temperatura koja utječe na ćelije

    def calculate_temperature_change(self, i, j, grid):
        """
        Funkcija koja računa promenu temperature na osnovu okruženja ćelije.
        Može se koristiti razlika u temperaturama susednih ćelija.
        """
        cell = grid[i][j]
        temp_change = 0

        # Povećanje temperature na osnovu spoljne temperature
        if cell.state == 'D':  # Drvo
            temp_change += random.uniform(0, 5)
        elif cell.state == 'G':  # Gori
            temp_change += random.uniform(5, 10)

        return temp_change

    def azuriraj_temperaturu(self, grid):
        """
        Ažurira temperaturu svih ćelija prema vanjskoj temperaturi.
        Ova funkcija je sada generator i koristi yield za usklađivanje sa SimPy.
        """
        for i in range(grid.size):
            for j in range(grid.size):
                cell = grid.grid[i][j]
                # Izračunavanje promene temperature za svaku ćeliju
                temperature_change = self.calculate_temperature_change(i, j, grid)
                cell.temperature += temperature_change
                yield grid.env.timeout(0.1)  # Pauza između koraka

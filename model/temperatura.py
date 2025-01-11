import random
class Temperatura:
    def __init__(self, vanjska_temperatura):
        self.vanjska_temperatura = vanjska_temperatura  # Vanjska temperatura koja utječe na ćelije

    def azuriraj_temperaturu(self, grid):
        """
        Ažurira temperaturu svih ćelija prema vanjskoj temperaturi.
        """
        for i in range(grid.size):
            for j in range(grid.size):
                cell = grid.grid[i][j]
                if cell.state == 'D':  # Drvo, povećava se prema vanjskoj temperaturi
                    cell.temperature += random.uniform(0, 5)
                elif cell.state == 'G':  # Požar, temperatura raste brže
                    cell.temperature += random.uniform(5, 10)

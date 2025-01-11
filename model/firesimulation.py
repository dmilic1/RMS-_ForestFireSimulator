import random

class FireSimulation:
    def __init__(self, grid, env, temperatura_objekt):
        self.grid = grid
        self.env = env
        self.temperatura_objekt = temperatura_objekt  # Objekt klase Temperatura

    def spread_fire(self):
        """
        Funkcija za širenje požara prema susjednim ćelijama.
        Požar se širi iz trenutnih 'G' ćelija u susjedne 'D' ćelije.
        """
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                cell = self.grid.grid[i][j]
                if cell.state == 'G':  # Ako ćelija gori
                    for neighbor in cell.neighbors:
                        if neighbor.state == 'D':  # Ako susjedna ćelija nije izgorjela
                            if random.random() < 0.1:  # 10% šanse da požar pređe u susjednu ćeliju
                                neighbor.state = 'G'  # Požar se širi
        yield self.env.timeout(1)  # Trajanje širenja požara na sljedeći vremenski korak

    def update_temperature(self):
        """
        Funkcija za ažuriranje temperature svakih nekoliko vremenskih koraka.
        """
        # Ažuriranje temperature svih ćelija na temelju vanjske temperature
        self.temperatura_objekt.azuriraj_temperaturu(self.grid)
        yield self.env.timeout(1)  # Trajanje za ažuriranje temperature

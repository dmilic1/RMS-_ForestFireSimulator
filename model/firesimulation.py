import random


class FireSimulation:
    def __init__(self, grid, env, temperatura_objekt):
        self.grid = grid
        self.env = env
        self.temperatura_objekt = temperatura_objekt  # Objekt klase Temperatura

    def calculate_fire_spread_chance(self, cell, neighbor):
        """
        Funkcija koja izračunava vjerovatnoću širenja požara na temelju temperature.
        Šansa se povećava ako je temperatura susjedne ćelije veća.
        """
        # Razlika u temperaturama između trenutne ćelije i susjeda
        temperature_diff = abs(cell.temperature - neighbor.temperature)

        # Osnovna šansa za širenje požara
        base_chance = 0.01

        # Povećavamo šansu sa većom razlikom u temperaturama
        spread_chance = base_chance + temperature_diff * 0.3  # Faktor zavisnosti od temperature

        # Dodavanje veće šanse ako je temperatura ćelije veoma visoka
        if cell.temperature > 60:
            spread_chance += 0.1  # Velika šansa za širenje požara pri visokoj temperaturi

        return min(spread_chance, 1)  # Osiguravamo da šansa ne prelazi 100%

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
                            fire_spread_chance = self.calculate_fire_spread_chance(cell, neighbor)

                            if random.random() < fire_spread_chance:  # Ako je šansa zadovoljena, požar se širi
                                neighbor.state = 'G'  # Požar se širi
        yield self.env.timeout(1)  # Trajanje širenja požara na sljedeći vremenski korak

    def update_temperature(self):
        """
        Funkcija za ažuriranje temperature svakih nekoliko vremenskih koraka.
        """
        # Ažuriranje temperature svih ćelija na temelju vanjske temperature
        self.temperatura_objekt.azuriraj_temperaturu(self.grid)
        yield self.env.timeout(1)  # Trajanje za ažuriranje temperature


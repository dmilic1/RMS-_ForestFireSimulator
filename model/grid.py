import random


class Cell:
    def __init__(self, id):
        self.id = id
        self.state = 'D'  # Početno stanje - Drvo (vegetacija)
        self.temperature = 20  # Početna temperatura ćelije
        self.neighbors = []  # Susedi ćelije

    def add_neighbors(self, neighbors):
        self.neighbors = neighbors


class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[Cell((i, j)) for j in range(size)] for i in range(size)]
        self.initialize_neighbors()
        self.initialize_fire_and_obstacles()

    def initialize_neighbors(self):
        for i in range(self.size):
            for j in range(self.size):
                neighbors = []
                if i > 0:
                    neighbors.append(self.grid[i - 1][j])
                if i < self.size - 1:
                    neighbors.append(self.grid[i + 1][j])
                if j > 0:
                    neighbors.append(self.grid[i][j - 1])
                if j < self.size - 1:
                    neighbors.append(self.grid[i][j + 1])
                self.grid[i][j].add_neighbors(neighbors)

    def initialize_fire_and_obstacles(self):
        """
        Inicijalizuje požar i prepreke na početku simulacije.
        """
        # Postavljanje požara u sredinu mreže
        self.grid[self.size // 2][self.size // 2].state = 'G'  # Požar u centru mreže

        # Nasumično postavljanje prepreka (O) na mreži
        for _ in range(self.size * self.size // 10):  # 10% mreže sa preprekama
            i, j = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.grid[i][j].state == 'D':  # Ako nije već drvo, postavi prepreku
                self.grid[i][j].state = 'O'

    def display(self):
        for row in self.grid:
            print(" ".join([cell.state for cell in row]))

# Simulira širenje požara na nasumično generisanom prostoru
# Korisnik podešava temperaturu zraka, veličinu ćelija i izvor požara klikom na proizvoljne ćelije

import tkinter as tk
from tkinter import messagebox
from model.grid import Grid
from model.temperatura import Temperatura
from model.firesimulation import FireSimulation
import simpy
from vizualizacija.prikaz import Visualizer


class FireSimulationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Forest Fire Simulation")

        # Grid parameters
        self.grid_size = 30  # Default grid size
        self.temperature = 20  # Default temperature
        self.cell_size = 7  # Size of each cell on the canvas

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Grid size input
        self.grid_size_label = tk.Label(self.master, text="Grid Size:")
        self.grid_size_label.grid(row=0, column=0)
        self.grid_size_entry = tk.Entry(self.master)
        self.grid_size_entry.grid(row=0, column=1)
        self.grid_size_entry.insert(0, str(self.grid_size))

        # Temperature input
        self.temp_label = tk.Label(self.master, text="Temperature:")
        self.temp_label.grid(row=1, column=0)
        self.temp_entry = tk.Entry(self.master)
        self.temp_entry.grid(row=1, column=1)
        self.temp_entry.insert(0, str(self.temperature))

        # Create grid button
        self.create_button = tk.Button(self.master, text="Create Grid", command=self.create_grid)
        self.create_button.grid(row=2, column=0, columnspan=2)

        # Start simulation button
        self.start_button = tk.Button(self.master, text="Start Simulation", command=self.start_simulation,
                                      state=tk.DISABLED)
        self.start_button.grid(row=3, column=0, columnspan=2)

        # Canvas for grid
        self.canvas = tk.Canvas(self.master, width=650, height=650)
        self.canvas.grid(row=4, column=0, columnspan=2)

        self.grid = None
        self.simulation = None
        self.env = None
        self.visualizer = None

    def create_grid(self):
        try:
            # Get the grid size and temperature from the user input
            self.grid_size = int(self.grid_size_entry.get())
            self.temperature = int(self.temp_entry.get())

            # Create the grid and initialize the simulation
            self.grid = Grid(self.grid_size)
            self.env = simpy.Environment()
            self.visualizer = Visualizer(self.grid)
            self.simulation = FireSimulation(self.grid, self.env, Temperatura(self.temperature))

            # Draw the grid on the canvas
            self.draw_grid()

            # Enable the start simulation button
            self.start_button.config(state=tk.NORMAL)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid grid size and temperature.")

    def draw_grid(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Draw the current grid state
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                cell = self.grid.grid[i][j]
                state = cell.state
                color = "green" if state == "D" else "red" if state == "G" else "gray"

                self.canvas.create_rectangle(
                    j * self.cell_size, i * self.cell_size,
                    (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                    fill=color, outline="black", tags=f"{i}_{j}"
                )

        # Bind click event to update cells
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        # Get clicked cell coordinates
        row = event.y // self.cell_size
        col = event.x // self.cell_size

        if 0 <= row < self.grid.size and 0 <= col < self.grid.size:
            cell = self.grid.grid[row][col]
            if cell.state == "D":
                cell.state = "G"  # Change to fire state
            elif cell.state == "G":
                cell.state = "D"  # Change to tree state
            self.draw_grid()  # Redraw the grid after the change

    def start_simulation(self):
        max_steps = 200
        visualization_interval = 5  # Visualize every 5 steps

        # Start the simulation
        self.run_simulation(max_steps, visualization_interval)

    def run_simulation(self, max_steps, visualization_interval):
        def simulation_step():
            for step in range(max_steps):
                yield self.env.process(self.simulation.spread_fire())
                yield self.env.process(self.simulation.update_temperature())

                if step % visualization_interval == 0:
                    self.visualizer.visualize(step)

                yield self.env.timeout(1)

        self.env.process(simulation_step())
        self.env.run()


# Run the GUI
root = tk.Tk()
app = FireSimulationGUI(root)
root.mainloop()
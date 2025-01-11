import random
import simpy
from model.grid import Grid
from model.temperatura import Temperatura
from model.pravila import STANJA, azuriraj_stanja
from model.firesimulation import FireSimulation
from vizualizacija.prikaz import Visualizer  # Importovanje klase za vizualizaciju

# Parametri
grid_size = 50
max_steps = 300
external_temperature = 55
visualization_interval = 5  # Prikazivanje vizualizacije na svakih 5 koraka

# Kreiranje objekata
env = simpy.Environment()  # SimPy environment
grid = Grid(grid_size)  # Grid sa početnim stanjem
temperatura_objekt = Temperatura(external_temperature)

# Kreiraj objekat za vizualizaciju
visualizer = Visualizer(grid)

# Inicijalizacija simulacije
simulation = FireSimulation(grid, env, temperatura_objekt)


def run_simulation():
    """
    Pokreće simulaciju po vremenskim koracima.
    """
    for step in range(max_steps):
        yield env.process(simulation.spread_fire())  # Širenje požara
        yield env.process(simulation.update_temperature())  # Ažuriranje temperature

        # Prikaz trenutnog stanja mreže (vizualizacija na određenim koracima)
        if step % visualization_interval == 0:  # Prikazivanje na svakih `visualization_interval` koraka
            visualizer.visualize(step)

        yield env.timeout(1)  # Čekanje na sljedeći vremenski korak


# Pokretanje simulacije
env.process(run_simulation())
env.run()  # Pokreće SimPy environment
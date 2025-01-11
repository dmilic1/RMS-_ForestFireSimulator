import random
# Definiranje stanja ćelija
STANJA = {
    'D': 'Drvo',  # Nepogođena vegetacija
    'G': 'Gori',  # Trenutno zahvaćeno plamenom
    'P': 'Prazno',  # Izgorjelo područje
    'O': 'Prepreka',  # Nepodnošljivo za sagorijevanje
}

def azuriraj_stanja(grid):
    # Ovdje možete dodati logiku za ažuriranje stanja ćelija na temelju okolnosti
    for row in grid:
        for cell in row:
            if cell.state == 'D' and random.random() < 0.05:
                cell.state = 'G'  # Ponekad će ćelija iznenada zapaliti
            elif cell.state == 'G' and random.random() < 0.1:
                cell.state = 'P'  # Požar će se ugasiti i postati prazno područje

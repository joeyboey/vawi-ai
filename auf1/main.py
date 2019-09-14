# %% Imports
from ca import GoL

# %% Init
gol = GoL(size=25, reproduction_prey=5, food=3, reproduction_predator=10, predator=3, predator_death=.05)   # Initialisierung des Game of Life mit Startparametern
for x in range(int(gol.getGridSize()/2)):                                                                   # Hinzufügen von von zufälligen Enitäten auf einem Drittel aller Felder (20% Räuber, 80% Beute)
    gol.addEntity(gol.randomEntity(chances=[.2, .8]))
gol.plotGrid()                                                                                              # Plotten des Koordinatensystems zur Veranschaulichung

# %% cycle
for x in range(0, 60):                                                                                      # Darstellung von 60 Zyklen
    gol.cycle()
    gol.plotGrid()

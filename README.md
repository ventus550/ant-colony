# Ant Colony

This is a simple ant colony simulator.
We distinct two main simulated environment objects: colonies and food piles.
Both of which can be added to the simulation at runtime.

<p align="center">
  <img src="https://imgur.com/hqAEUg2.png" alt="Food gathering" width="400" style="border-radius:12px">
</p>

Randomly traveling ants emerge from the colonies. Ants that successfully reach the food pile will emit pheromones on their way back to the colony. Other ants may choose to follow that trail. Underlying database allows full recovery of the most recently interrupted simulation, which is done so automatically. 


### Technologies used
- Simulation is rendered by Tkinter graphics library.
- Database is managed and created with Sqlite.

### How to run
The simulation can be started by typing `make` in the root directory.
To run a fresh simulation type `make new` or press delete to reset the current simulation.
One may also run some tests and testing scenarios via `make test` and `make scenarios`.


<p align="center">
  <img src="https://imgur.com/ia8ghjB.png" alt="Scenario" width="500" style="border-radius:12px">
</p>

# Ant Colony

This is a simple ant colony simulator.
We distinct two main simulated environment objects: colonies and food piles.
Both of which can be added to the simulation at runtime.

<svg fill="none" viewBox="0 0 300 120" width="300" height="120" xmlns="http://www.w3.org/2000/svg">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">

      <style>
        .tags {
          display: flex;
          flex-wrap: wrap;
          height: 100%;
          width: 100%;
        }
        .tag {
          background-color: #E3FFFF;
          border-radius: 0.25em;
          color: #0ca4a5;
          border: 1px solid #0ca4a5;
          display: inline-block;
          font-size: 0.75em;
          line-height: 2em;
          margin: 0.125em;
          padding: 0 0.5em;
          text-decoration: none;
          font-family: sans-serif;
        }
      </style>

      <div class="tags">
        <div class="tag">Angular</div>
        <div class="tag">Vue(X)</div>
        <div class="tag">JavaScript</div>
        <div class="tag">TypeScript</div>
      </div>
      <div class="tags">
        <div class="tag">(S)CSS</div>
        <div class="tag">Building UIs</div>
        <div class="tag">Web Components</div>
      </div>
      <div class="tags">
        <div class="tag">Ionic</div>
        <div class="tag">Electron</div>
        <div class="tag">.NET</div>
      </div>

    </div>
  </foreignObject>
</svg>

<p align="center">
  <img src="https://imgur.com/z7oyVXe.pngg" alt="Food gathering" width="500" style="border-radius:12px">
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

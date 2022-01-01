from ants import Colony, Food
from time import sleep
from tkinter import Tk
from params import geometry, animation_speed


def draw_colony(colony: Colony, app: Tk):
    "Draw colony and its ants on the tkinter canvas."
    rng = range(geometry)
    for x in rng:
        for y in rng:
            pos = (x, y)
            if colony.pheromones[pos] > 0:
                app.ctx.point(pos, color=colony.color)
    for ant in colony:
        if ant.payload:
            app.ctx.box(ant.position, size=0.75, color='green', fill='green')
        else:
            app.ctx.box(ant.position, size=0.5, color=colony.color)
    app.ctx.circle(colony.location, r=3, color=colony.color)


def draw_food(food: Food, app: Tk):
    "Draw food and its ants on the tkinter canvas."
    app.ctx.circle(food.location, r=food.radius(),
                   color='green', stipple='error')


class Simulation:
    "Simulation engine resposible for drawing objects and maintaining tkinter loop."

    def __init__(self):
        self.colonies = []
        self.food = []
        self.app = None
        self.running = False

    def spawn_colony(self, x: int, y: int, ants: int, color: str) -> Colony:
        "Creates a colony."
        self.colonies.append(Colony((y, x), size=ants, color=color))
        return self.colonies[-1]

    def spawn_food(self, x: int, y: int, size: int) -> Food:
        "Creates food."
        self.food.append(Food((y, x), size=size))
        return self.food[-1]

    def connect(self, app: Tk) -> None:
        "Bind the simulator to the app window."
        self.app = app
        self.running = True
        self.run()

    def reset(self) -> None:
        "Revert to the default state."
        self.colonies = []
        for food in Food.instances:
            food.size = 0
        self.food = []
        Food.cleanup()
    
    def stop(self) -> None:
        self.running = False

    def run(self) -> None:
        "Run the animation loop."
        while self.running:
            sleep(animation_speed)
            self.app.ctx.clear()
            Food.cleanup()

            for colony in self.colonies:
                colony.update()
                draw_colony(colony, self.app)

            for food in Food.instances:
                draw_food(food, self.app)
            self.app.ctx.message()

"""
Driver code and some event handling.
"""

from window import Window
from database import Database
from simulation import Simulation
from params import block, palette

if __name__ == '__main__':

    def blockify(x):
        return x // block

    app = Window()
    sim = Simulation()
    db = Database()

    def shutdown():
        db.wipe()
        for colony in sim.colonies:
            db.store_colony(colony)
        for food in sim.food:
            db.store_food(food)
        db.commit()
        sim.running = False
    
    def del_handler(event):
        if event.char == '\x7f':
            db.wipe()
            sim.reset()

    def lpm_handler(event):
        sim.spawn_food(blockify(event.y), blockify(event.x), 100)

    def rpm_handler(event):
        idx = 3 + len(sim.colonies)
        free_color = palette[idx] if idx < len(palette) else 'white'
        sim.spawn_colony(blockify(event.y), blockify(event.x),
                         50, free_color)

    app.bind('<Key>', del_handler)
    app.ctx.bind("<Button-1>", lpm_handler)
    app.ctx.bind("<Button-2>", rpm_handler)
    app.ctx.bind("<Button-3>", rpm_handler)
    app.protocol("WM_DELETE_WINDOW", shutdown)

    sim.colonies = list(db.colonies())
    sim.food = list(db.food())

    sim.connect(app)

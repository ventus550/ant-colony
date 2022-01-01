import unittest
import context
from window import Window
from simulation import Simulation

def scenario(setup, time):
    sim = Simulation()
    sim.reset()
    setup(sim)
    app = Window()
    app.after(time, lambda:sim.stop())
    sim.connect(app)
    return sim

class test_ants(unittest.TestCase):

    def test_food(self):
        def setup(sim):
            sim.spawn_colony(100, 100, 200, "orange")
            sim.spawn_food(115, 115, 1000)

        self.assertFalse(scenario(setup, 10000).food[0].size)


    def test_payload(self):
        def setup(sim):
            colony = sim.spawn_colony(100, 100, 10, "red")
            for _ in range(100):
                colony.update()
            for ant in colony:
                ant.payload = True

        for ant in scenario(setup, 10000).colonies[0]:
            self.assertFalse(ant.payload)
    

    def test_colonies(self):
        def setup(sim):
            sim.spawn_colony(150, 150, 100, "blue")
            sim.spawn_colony(50, 50, 100, "red")
            sim.spawn_colony(150, 50, 100, "yellow")
            sim.spawn_food(100, 100, 5000)

        for colony in scenario(setup, 10000).colonies:
            self.assertEqual(len(colony), 100)
            for ant in colony:
                self.assertTrue(len(ant.path) < 2*colony.max)


if __name__ == '__main__':
    unittest.main()

    def test_payload(self):

        sim = Simulation()
        sim.spawn_colony(100, 100, 10, "red")
        colony = sim.colonies[0]
        for _ in range(100):
            colony.update()
        
        for ant in colony:
            ant.payload = True

        app = Window()
        app.after(10000, lambda: sim.stop())
        sim.connect(app)
        
        for ant in colony:
            self.assertFalse(ant.payload)
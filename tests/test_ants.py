import unittest
import context
from ants import Ant, Colony
from numpy import inf


class test_ants(unittest.TestCase):

    def test_movement(self):
        __aux = Colony((0,0), 0)
        ant = Ant((100, 100), __aux)
        shadow = [None, None]
        for i in range(10000):
            self.assertEqual(len(ant.path), i)
            ant.move()
            self.assertNotEqual(list(shadow), list(ant.position))
            shadow = ant.position
    
    def test_payload(self):
        colony = Colony((100, 100), 10)
        colony.update()
        self.assertEqual(colony.max, inf)
        for _ in range(100):
            colony.update()
        
        for ant in colony:
            ant.payload = True
        
        for ant in colony:
            self.assertTrue(len(ant.path) <= colony.max)


if __name__ == '__main__':
    unittest.main()

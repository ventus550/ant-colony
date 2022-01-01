from random import choice, shuffle
from math import pi
from numpy import zeros, where, array, exp
import numpy as np
from params import geometry, exploration_factor, vaporization_time
from mytypes import Coords, Any, Callable


directions = [(-1, -1), (0, -1), (1, -1), (1, 0),
              (1, 1), (0, 1), (-1, 1), (-1, 0)]
dmap = {dr: directions.index(dr) for dr in directions}


def next(direction: Coords) -> Coords:
    "Return the next direction moving clockwise."
    return directions[(dmap[direction] + 1) % len(directions)]


def prev(direction: Coords) -> Coords:
    "Return the next direction moving anti-clockwise."
    return directions[dmap[direction] - 1]


def opposite(direction: Coords) -> Coords:
    "Return direction opposite to the one passed as argument."
    return directions[dmap[direction] - 4]


def manhattan(v: Coords, u: Coords) -> int:
    "Calculate manhattan distance."
    return sum(abs(v-u))


def softmax(ls: list, key: Callable[[Any], float]) -> Any:
    "Return item from the list chosen randomly with softmax distribution."
    values = array([key(x) for x in ls])
    values /= exploration_factor
    e = exp(values - max(values))
    return ls[np.random.choice(np.arange(len(ls)), p=e/e.sum())]


class Food:
    """
    Once placed will attract nearby ants.
    Upon contact a tasty chunk is separated and carried home by the lucky finder.

    Atrributes:
        location    -- block coordinates of the object in the simulated environment

        size        -- chunking subtracts from this value, food is depleted when it reaches zero
    """
    instances = set()
    chunk = 1

    def __init__(self, location: Coords, size: int = 1000):
        self.location = location
        self.size = size
        self.instances.add(self)

    def radius(self) -> float:
        "Calculate the radius of the object ine the simulated environment."
        return (self.size/pi)**0.5

    def in_range(self, xy: Coords) -> bool:
        "Check if xy position is considered to be touching the object."
        x, y = xy
        a, b = self.location
        return (x-a)**2 + (y-b)**2 <= self.radius()**2

    def proxima(pos: Coords):
        "Return the closest reachable food or None otherwise for the position."
        for f in Food.instances:
            if f.in_range(pos):
                return f
        return None

    def consume(self) -> None:
        "Split a chunk from the food object."
        self.size -= self.chunk
        self.size = max(0, self.size)

    def cleanup() -> None:
        "Remove depleted food objects from the simulation."
        Food.instances = {food for food in Food.instances if food.size != 0}


class Colony(set):
    """
    Ants form colonies where they stockpile the gathered resources.

    Atrributes:
        location    -- block coordinates of the object in the simulated environment

        color       -- color used to distinct different colonies in the simulated environment

        max         -- length of the current shortest path and a soft limit for all future paths

        pheromones  -- pheromone matrix
    """

    def __init__(self, location: Coords, size: int = 10, color: str = 'white'):
        self.location = array(location)
        self.color = color
        self.max = np.inf
        self.pheromones = zeros((geometry, geometry))

        # create ants and assign them to the colony
        for _ in range(size):
            self.add(Ant(self.location, colony=self))

    def update(self) -> None:
        "Handle pheromone vaporization, kill ants that wondered too far off and collect the payloads."
        phero = self.pheromones
        phero[where(phero > 0)] -= 1
        payloads = False
        for ant in self:
            payloads = ant.payload or payloads
            if len(ant.path) > self.max:
                ant.position = self.location.copy()

            if manhattan(self.location, ant.position) < 2:
                ant.payload = False
                ant.path = []
                ant.direction = opposite(ant.direction)
            ant.move()

        if not payloads:
            self.max = np.inf


class Ant:
    """
    A small insect typically having a sting and living in a complex social colony.
    Ants move at random until they encounter a trail of phenoytpe left behind by another ant
    from the same colony carrying a payload (chunk of food).
    Curious ants may choose to follow that trail, especially when the trail is fresh.

    Atrributes:
        payload     -- marks an ant as a food carrier

        path        -- sequence of steps from the colony

        direction   -- current direction of travel

        position    -- block coordinates of the object in the simulated environment

        colony      -- colony the ant belongs to
    """

    def __init__(self, position: Coords, colony: Colony):
        self.payload = False
        self.path = []
        self.direction = choice(directions)
        self.position = array(position)
        self.colony = colony

    def move(self) -> None:
        """
        Move an ant in the current general direction of travel, handle food interactions (if any)
        and leave behind pheromone trail (if payload).
        """
        phero = self.colony.pheromones
        sdr = self.direction

        # shuffle similar directions so that ant moves randomly
        # when no pheromone traces are detected
        directions = [prev(sdr), sdr, next(sdr)]
        shuffle(directions)

        # reposition accordingly to the given direction
        def step(pos, dr):
            return (pos + dr) % geometry

        # if payload rewind the path sequence and return to the colony
        # otherwise choose the new direction of travel
        if self.payload:
            self.direction = softmax(
                directions, key=lambda d: phero[tuple((self.position + d) % geometry)])
            self.direction = opposite(self.path.pop())
        else:
            self.direction = softmax(
                directions, key=lambda d: phero[tuple((self.position + d) % geometry)])
            self.path.append(self.direction)
        self.position = step(self.position, self.direction)

        # handle food interaction
        for d in directions:
            food = Food.proxima(step(self.position, d))
            if food:
                food.consume()
                phero[tuple(step(self.position, d))] = vaporization_time
                self.direction = opposite(self.direction)
                self.payload = True
                self.colony.max = min(self.colony.max, len(self.path)*2)

        # leave pheromone trail if carrying payload
        phero[tuple(self.position)] = max(
            vaporization_time*int(self.payload), phero[tuple(self.position)])

import sqlite3
import numpy as np
from ants import Colony, Food, Ant
from params import geometry


class Database:
    "Database to store ants, colonies and food objects."

    def __init__(self):
        self.database = sqlite3.connect('ants.db')
        self.cursor = self.database.cursor()
        try:
            self.cursor.execute("""CREATE TABLE ants
			(x integer, y integer, dx integer, dy integer, payload integer, colony text, path txt)""")

            self.cursor.execute("""CREATE TABLE colonies
			(x integer, y integer, color text, max integer, pheromones blob)""")

            self.cursor.execute("""CREATE TABLE food
			(x integer, y integer, size integer)""")
        except sqlite3.OperationalError:
            ...

    def store_ant(self, ant: Ant) -> None:
        "Stores an ant in the database."
        self.cursor.execute(f"""INSERT INTO ants VALUES
		({ant.position[0]}, {ant.position[1]}, {ant.direction[0]}, {ant.direction[1]},
		{int(ant.payload)}, '{ant.colony.color}', '{ant.path}')""")

    def store_colony(self, colony: Colony) -> None:
        "Stores a colony in the database."
        self.cursor.execute(f"""INSERT INTO colonies VALUES
		({colony.location[0]}, {colony.location[1]}, '{colony.color}',
		{colony.max if colony.max != np.inf else -1}, '{list(colony.pheromones.flatten())}')""")

        for ant in colony:
            self.store_ant(ant)

    def store_food(self, food: Food) -> None:
        "Stores food in the database."
        if food.size > 0:
            self.cursor.execute(f"""INSERT INTO food VALUES
            ({food.location[0]}, {food.location[1]}, '{food.size}')""")

    def colonies(self) -> None:
        "Fetches colonies from the database using generator."
        for x, y, color, mx, pheromones in self.cursor.execute("SELECT * FROM colonies").fetchall():
            ants = self.cursor.execute(
                f"SELECT * FROM ants WHERE colony = '{color}'").fetchall()
            colony = Colony((x, y), size=len(ants), color=color)
            colony.max = mx if mx != -1 else np.inf
            colony.pheromones = np.array(
                eval(pheromones)).reshape((geometry, geometry))
            for i, ant in enumerate(colony):
                x, y, dx, dy, payload, color, path = ants[i]
                ant.position = np.array((x, y))
                ant.direction = (dx, dy)
                ant.payload = bool(payload)
                ant.path = eval(path)
            yield colony

    def food(self) -> None:
        "Fetches food from the database using generator."
        for x, y, size in self.cursor.execute("SELECT * FROM food").fetchall():
            yield Food((x, y), size=size)

    def wipe(self) -> None:
        "Wipes the database clean."
        self.cursor.execute("""DELETE FROM ants""")
        self.cursor.execute("""DELETE FROM colonies""")
        self.cursor.execute("""DELETE FROM food""")

    def commit(self) -> None:
        "Commits changes to the databse."
        self.database.commit()

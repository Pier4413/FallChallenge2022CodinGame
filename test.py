from dataclasses import dataclass
@dataclass
class Tile:
  owner: int

distances = list[tuple[Tile, float]]()
distances.append((Tile(1), 12.2147414))
distances.append((Tile(1), 5.4))
distances.append((Tile(1), 0.847))
distances.append((Tile(1), 15.7))
distances.append((Tile(1), 1.25))
distances.sort(key=(lambda value: value[1]))
print(distances)
nearest_element = list(map(lambda value: value[0], distances[-2:]))
print(nearest_element)
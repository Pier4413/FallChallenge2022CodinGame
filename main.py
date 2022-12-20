import sys
import math

import sys
import math
from dataclasses import dataclass
from typing import Any

# global variables
ME = 1
OPP = 0
NONE = -1

tiles = list["Tile"]() # Toutes les tiles

my_units = list["Tile"]() # Mes unités
opp_units = list["Tile"]() # Les unités adversaire

my_recyclers = list["Tile"]() # Mes recycleurs
opp_recyclers = list["Tile"]() # Les recycleurs adverses

my_tiles = list["Tile"]() # Mes tiles
opp_tiles = list["Tile"]() # Les tiles adverses
neutral_tiles = list["Tile"]() # Les tiles neutres

@dataclass
class Tile:
  x: int
  y: int
  scrap_amount: int
  owner: int
  units: int
  recycler: bool
  can_build: bool
  can_spawn: bool
  in_range_of_recycler: bool

  def __str__(self) -> str:
    return f"Position : [{self.x}; {self.y}; Owner : {self.owner}"
  
  def has_units(self):
    return self.units > 0

  def calculate_distance(self, tile : "Tile") -> float:
    if tile is not None:
        return (abs((self.x - tile.x)) + abs((self.y - tile.y)))
        # return math.sqrt(math.pow((self.x - tile.x), 2) + math.pow((self.y - tile.y), 2))
    return 1000

  def find_nearest_by_criteria(self, tiles : list["Tile"], criteria : str, value : Any) -> "Tile":
    min_distance = 1000 # On prends une tres grande distance pour demarrer puis on retrecit petit a petit
    if tiles is not None and len(tiles) > 0:
        ret_tile = tiles[len(tiles) - 1]

        for tile in tiles:
            distance = self.calculate_distance(tile)
            if tile is not self and criteria == value and distance < min_distance:
                ret_tile = tile
                min_distance = distance
        return ret_tile

  def calculate_amount_to_spawn(self, matter : int) -> int:
      return matter // 10

  def should_build(self, tiles : list["Tile"]) -> bool:
    return len(tiles) == 0 or self.calculate_distance(self.find_nearest_by_criteria(tiles, [self.recycler], [True])) > 2

  def find_neighbourgs(self, tiles: list["Tile"]) -> list["Tile"]:
    ret = list[Tile]()
    if tiles is not None:
      for tile in tiles:
        if self.calculate_distance(tile) == 1:
          ret.append(tile)
    return ret
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

print("SIZE", file=sys.stderr)
width, height = [int(i) for i in input().split()]


def filter_tiles(mines : list["Tile"], 
                opponents : list["Tile"], 
                criterias : list[Any], 
                my_values : list[Any], 
                opp_values : list[Any],
                neutral_tiles : list["Tile"] = None,
                neutral_values : list[Any] = None) -> None:
  """
    Fonction générique visant à préfiltrer les tiles pour éviter de boucler plusieurs fois en cherchant. 
    Si la tile n'entre dans aucune catégorie alors il ne se passe rien

    :param mines: Liste des tiles du joueur
    :param opponents: Liste des tiles de l'adversaire
    :param criterias: Les criteres de tile que l'on veut comparer
    :param my_values: Les valeurs de critere attendus pour le joueur
    :param opp_values: Les valeurs de critere attendus pour l'adversaire
    :param neutral: Liste des tiles neutres si applicables
  """
  if criterias == my_values: # On compare les criteres aux valeurs attendus pour le joueur
    mines.append(tile)
  elif criterias == opp_values: # On compare les criteres aux valeurs attendus pour l'adversaire
    opponents.append(tile)
  else: # Si on a rien on regarde si on des tiles neutres pour ces criteres. Si oui on ajoute aux tiles neutres sinon on dégage
    if neutral_tiles is not None and neutral_values is not None and criterias == neutral_values:
      neutral_tiles.append(tile)


def strategy(my_matter : int, opp_matter: int, tiles: list[Tile], my_units: list[Tile], opp_units: list[Tile], my_recyclers: list[Tile], opp_recyclers: list[Tile], 
              my_tiles: list[Tile], opp_tiles: list[Tile], neutral_tiles: list[Tile], turn: int):
  actions = []

  tiles_mine = my_tiles.copy()
  tiles_mine.extend(my_units)
  tiles_mine.extend(my_recyclers)

  tiles_opp = opp_tiles.copy()
  tiles_opp.extend(opp_units)
  tiles_opp.extend(opp_recyclers)
  # Les regles d'ordre sont les suivantes
  # D'abord toutes les actions BUILD sont executees
  # Puis les actions MOVE et SPAWN se font en même temps, ainsi un bot qui SPAWN ne peut pas MOVE et inversement

  # Notre strategie est donc :

  # Stratégie des recycleurs
  # 1. Voir si on peut construire en limitant le nombre de recycleurs à 4 pour limiter les couts et on ne construit de recycleurs que si l'on a 30 matieres minimum
  # 1. i Il n'y a pas d'optimisation du recyclage le but étant de construire un "mur" pour l'ennemi
  # 1. ii Pas plus de 4 recycleurs en même temps pour l'équipe
  # 1. iii Un recycleur doit se trouver le plus près possible de l'ennemi ou alors si on a aucun recycleur dans le jeu
  # 1. iv On ne construit pas avant le tour 3
  nb_recycleurs = len(my_recyclers)
  for tile in my_tiles:
    # On vérifie si la tile n'est pas en range d'un recycleur puis la distance à la tile ennemi la plus proche ou si on a aucun recycleur
    if tile.can_build is True and tile.should_build(my_recyclers) is True and nb_recycleurs < 4 and my_matter < 20 and len(tiles_mine) <= len(tiles_opp):
      actions.append('BUILD {} {}'.format(tile.y, tile.x))
      my_recyclers.append(tile)
      nb_recycleurs = len(my_recyclers)
      my_matter -= 10

  # Stratégie de création/déplacement
  # 2. On commence par construire sur toutes les cases vides sans unité tant que faire ce peut
  # 3. Avec les unités on se déplace vers la case ennemi la plus proche ou si elle n'est pas accollé la case neutre la plus proche accolé
  # 3. si aucunes des ces cases n'existe on prend la plus proche neutre/ennemi qui existe quelle quel soit
  for tile in my_tiles:
    if my_matter >= 10 and tile.recycler is False:
      amount_spawn = 1
      actions.append(f"SPAWN {amount_spawn} {tile.y} {tile.x}")
      my_matter -= 10
  
  for tile in my_units:
      ret_tile = None
      opp_tiles.extend(neutral_tiles)
      amount_move = tile.units
      neighbourgs = tile.find_neighbourgs(opp_tiles)
      for neighbourg in neighbourgs:
          if neighbourg.units > 0:
            ret_tile = neighbourg
          elif neighbourg.owner == OPP and ret_tile is None:
            ret_tile = neighbourg
          elif ret_tile is None:
            ret_tile = neighbourg
          tile.units -= amount_move
      if ret_tile is None:
        ret_tile = tile.find_nearest_by_criteria(opp_tiles, [tile.owner], [OPP])

      if ret_tile is None:
        ret_tile = tile.find_nearest_by_criteria(neutral_tiles, [tile.owner], [NONE])

      if ret_tile is not None:
        actions.append(f'MOVE {amount_move} {tile.y} {tile.x} {ret_tile.y} {ret_tile.x}')
      else:
        actions.append(f"WAIT")
        break
  """
  # Stratégie de création/déplacement
  # 2. On cherche ceux qui sont le plus proche de l'ennemi et on met de côté les deux plus éloignés
  # 2. i Avec les plus proches on se déplace le plus rapidement possible vers l'ennemi, le but étant de s'approcher assez pour commencer la construction des recycleurs
  # 2. ii Avec les plus éloignés on opte pour une stratégie de conquete de territoire en se déplacant sur les lignes en hauteur, puis d'une case à gauche
  distances = list[tuple[Tile, float]]()
  for tile in my:
      distances.append((tile, tile.calculate_distance(tile.find_nearest_by_criteria(opp_tiles, [tile.owner], OPP))))
  distances.sort(key=(lambda value: value[1]))
  nearest_elements = list(map(lambda value: value[0], distances[-2:]))

  
  for (tile, distance) in distances: 
    # 2. iii Pendant les trois premiers tours on va vers l'ennemi sans distinction
    if turn < 3:
      if len(opp_tiles) > 0:
        target = opp_tiles[0]
        amount_move = tile.units
        actions.append(f"MOVE {amount_move} {tile.y} {tile.x} {target.y} {target.x}")
      else:
        actions.append(f"WAIT")
    else:
      # 2. iii Deplacement des plus proches de l'ennemi vers celui-ci
      opp_tiles.extend(neutral_tiles)
      target = tile.find_nearest_by_criteria(opp_tiles, [tile.owner == OPP or tile.owner == NONE], [True])
      
      # 2. iv Pour les plus eloignes on adopte la strategie suivante
      # 2. iv. i Si on a plus de 10 de matiere alors on fait apparaitre un bot et on déplace tous ceux en trop sur la case vers l'ennemi
      # 2. iv. ii Si on plus assez de matières pour faire apparaître des bots alors on se déplace en groupe
      if tile in nearest_elements:
        if my_matter >= 10 and tile.units == 0:
          amount_spawn = tile.calculate_amount_to_spawn(my_matter)
          actions.append(f"SPAWN {amount_spawn} {tile.y} {tile.x}")
          my_matter -= 10 * amount_spawn
        else:
          amount_move = tile.units # On déplace toutes les unités de la case en même temps (stratégie de groupe)
          actions.append(f"MOVE {amount_move} {tile.y} {tile.x} {target.y} {target.x}")
      else:
        neighbourgs = tile.find_neighbourgs(neutral_tiles.extend(opp_tiles))
        for neighbourg in neighbourgs:
          if tile.units > 0:
            amount_move = 1 # On déplace toutes les unités de la case en même temps (stratégie de groupe)
            actions.append(f'MOVE {amount_move} {tile.y} {tile.x} {neighbourg.y} {neighbourg.x}')
            tile.units -= amount_move
    """
  return actions

turn = 1
# game loop
while True:
    
    tiles.clear() # Toutes les tiles

    my_units.clear() # Mes unités
    opp_units.clear() # Les unités adversaire

    my_recyclers.clear() # Mes recycleurs
    opp_recyclers.clear() # Les recycleurs adverses

    my_tiles.clear() # Mes tiles
    opp_tiles.clear() # Les tiles adverses
    neutral_tiles.clear() # Les tiles neutres

    my_matter, opp_matter = [int(i) for i in input().split()]

    for i in range(height):
        for j in range(width):
          
            # owner: 1 = me, 0 = foe, -1 = neutral
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]
            tile = Tile(i, j, scrap_amount, owner, units, recycler == 1, can_build == 1, can_spawn == 1, in_range_of_recycler == 1)
            tiles.append(tile) # On ajoute la tile dans la liste de toutes les tiles du jeu
            filter_tiles(my_units, opp_units, [tile.owner, tile.has_units()], [ME, True], [OPP, True]) # On filtre les tiles combattantes
            filter_tiles(my_recyclers, opp_recyclers, [tile.owner, tile.recycler], [ME, True], [OPP, True]) # 
            filter_tiles(my_tiles, opp_tiles, [tile.owner, tile.scrap_amount > 0, tile.units == 0], [ME, True, True], [OPP, True, True], neutral_tiles, [NONE, True, True])

    actions = strategy(my_matter, opp_matter, tiles, my_units, opp_units, my_recyclers, opp_recyclers, my_tiles, opp_tiles, neutral_tiles, turn)
    turn += 1
    
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    #print(actions, file=sys.stderr)
    print(';'.join(actions) if len(actions) > 0 else f"WAIT")

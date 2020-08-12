## Helper functions for creating vector tiles from a PostGIS database - adapted from https://github.com/pramsey/minimal-mvt
from psycopg2 import sql


def tileIsValid(tile):
    """
    Check whether the requested tile is valid. Extra checks on the x/y/z/format variables have been added on top of those provided by Django's URL dispatcher because I'm paranoid about the raw SQL query needed to return a tile.
    """
    if not ('x' in tile and 'y' in tile and 'zoom' in tile):
        return False
    if not (type(tile['x']) == int and type(tile['y'] == int)):
        return False
    if 'format' not in tile or tile['format'] not in ['pbf', 'mvt']:
        return False
    size = 2 ** tile['zoom'];
    if tile['x'] >= size or tile['y'] >= size:
        return False
    if tile['x'] < 0 or tile['y'] < 0:
        return False
    return True


# Calculate envelope in "Spherical Mercator" (https://epsg.io/3857)
def tileToEnvelope(tile):
    # Width of world in EPSG:3857
    worldMercMax = 20037508.3427892
    worldMercMin = -1 * worldMercMax
    worldMercSize = worldMercMax - worldMercMin
    # Width in tiles
    worldTileSize = 2 ** tile['zoom']
    # Tile width in EPSG:3857
    tileMercSize = worldMercSize / worldTileSize
    # Calculate geographic bounds from tile coordinates
    # XYZ tile coordinates are in "image space" so origin is
    # top-left, not bottom right
    env = dict()
    env['xmin'] = worldMercMin + tileMercSize * tile['x']
    env['xmax'] = worldMercMin + tileMercSize * (tile['x'] + 1)
    env['ymin'] = worldMercMax - tileMercSize * (tile['y'] + 1)
    env['ymax'] = worldMercMax - tileMercSize * (tile['y'])
    return env
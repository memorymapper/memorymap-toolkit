## Helper functions for creating vector tiles from a PostGIS database - adapted from https://github.com/pramsey/minimal-mvt

def tileIsValid(tile):
    if not ('x' in tile and 'y' in tile and 'zoom' in tile):
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


# Generate SQL to materialize a query envelope in EPSG:3857.
# Densify the edges a little so the envelope can be
# safely converted to other coordinate systems.
def envelopeToBoundsSQL(env):
    DENSIFY_FACTOR = 4
    env['segSize'] = (env['xmax'] - env['xmin'])/DENSIFY_FACTOR
    sql_tmpl = 'ST_Segmentize(ST_MakeEnvelope({xmin}, {ymin}, {xmax}, {ymax}, 3857),{segSize})'
    return sql_tmpl.format(**env)
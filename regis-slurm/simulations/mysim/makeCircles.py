import sys
import json
import numpy as np

inputsFile = sys.argv[1]
inputs = json.load(open(inputsFile))

try:
    x = float(inputs['centre'][0]['x'])
    y = float(inputs['centre'][0]['y'])
    r = float(inputs['radius'])
    ident = inputs['centre'][0]['id']
except:
    print('Could not read centre / radius, using default values', file=sys.stderr)
    x = 0
    y = 0
    z = 10

def createCircle(x, y, r):
    coords = [  ]

    for t in np.linspace(0, 2*np.pi, 500):
        lon = np.round(x + np.cos(t) * r,4)
        lat = np.round(y + np.sin(t) * r,4)

        coords.append([ lon, lat ])
    return coords


if not ident:
    ident = "circles"

numCircles = 100
features = []
xs = np.random.normal(x, 1, numCircles)
ys = np.random.normal(y, 1, numCircles)
radii = np.random.uniform(0, r+0.5, numCircles)
for c in range(numCircles):
    coords = createCircle(xs[c], ys[c], radii[c])

    f = {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          coords
        ]
      },
      "properties": {
        'name': 'Circle-' + str(c),
        'x': xs[c],
        'y': ys[c],
        'radius': radii[c]
      },
      "id": ident + '-' + str(c)
    }

    features.append(f)

geojson = {
  "type": "FeatureCollection",
  "properties": {
      "name": "urn:ogc:def:crs:EPSG::3395"
  },
  "features": features
}

print(json.dumps(geojson))

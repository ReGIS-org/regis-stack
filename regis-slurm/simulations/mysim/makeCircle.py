import sys
import json
import numpy as np

inputsFile = sys.argv[1]
inputs = json.load(open(inputsFile))

try:
    x = float(inputs['centre'][0]['x'])
    y = float(inputs['centre'][0]['y'])
    r = float(inputs['radius'])
except:
    print('Could not read centre / radius, using default values', file=sys.stderr)
    x = 0
    y = 0
    z = 10

coords = [  ]

for t in np.linspace(0, 2*np.pi, 500):
    lon = np.round(x + np.cos(t) * r,4)
    lat = np.round(y + np.sin(t) * r,4)

    # lon = x_circ
    # lat = 2 * np.arctan(np.exp(y_circ)) - np.pi/2

    coords.append([ lon, lat ])

geojson = {
  "type": "FeatureCollection",
  "properties": {
      "name": "urn:ogc:def:crs:EPSG::3395"
  },
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          coords
        ]
      },
      "properties": {
        'name': 'Circle-1',
        'x': x,
        'y': y,
        'radius': r
      },
      "id": "xxxx_-8000"
    }
  ]
}

print(json.dumps(geojson))

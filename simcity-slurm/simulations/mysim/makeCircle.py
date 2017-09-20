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

for t in np.linspace(0, 2*np.pi, 50):
    h = np.round(x + np.cos(t) * r,4)
    k = np.round(y + np.sin(t) * r,4)
    coords.append([ h, k ])

geojson = {
  "type": "FeatureCollection",
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

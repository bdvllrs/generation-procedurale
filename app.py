from Map import Map
from Show import show
import matplotlib.pyplot as plt
from Fractal import PerlinNoise


if __name__ == '__main__':
    m = Map(65)
    m.generate_map(method="perlin", smoothness=20)
    # print(m.map)
    plt.imshow(m.map, cmap=plt.cm.binary)
    plt.show()
    # show(m)

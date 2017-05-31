from Map import Map
from Show import show
import matplotlib.pyplot as plt
# from Fractal import PerlinNoise


if __name__ == '__main__':
    m = Map(256)
    m.generate_map(method="perlin_combined")
    # show(m)
    # print(m.map)
    plt.imshow(m.map, cmap=plt.cm.binary)
    plt.show()

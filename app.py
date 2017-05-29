from Map import Map
from Show import show
import matplotlib.pyplot as plt
from Fractal import PerlinNoise


if __name__ == '__main__':
    m = Map(257)
    m.generate_map(seed=2)
    # print(m.map)
    # plt.imshow(m.map, cmap=plt.cm.binary)
    # plt.show()
    show(m)

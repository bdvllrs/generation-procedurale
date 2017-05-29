from Map import Map
from Show import show
import matplotlib.pyplot as plt
from Fractal import PerlinNoise


if __name__ == '__main__':
    m = Map(5)
    m.generate_map(seed=1)
    # print(m.map)
    # plt.imshow(m.map, cmap=plt.cm.binary)
    # plt.show()
    show(m)

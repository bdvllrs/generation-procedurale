from Map import Map
from Show import show
import matplotlib.pyplot as plt


if __name__ == '__main__':
    m = Map(129)
    m.generate_map(method='perlin_combined')
    # m.generate_map(method='perlin', smoothness=1.2)
    print(m.map)
    plt.imshow(m.map, cmap=plt.cm.binary)
    plt.show()
    # show(m)

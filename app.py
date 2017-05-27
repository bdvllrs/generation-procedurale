from Map import Map
from Show import show
import matplotlib.pyplot as plt


if __name__ == '__main__':
    m = Map(400)
    m.generate_map(method='perlin', smoothness=50)
    print(m.map)
    plt.imshow(m.map, cmap=plt.cm.binary)
    plt.show(m)

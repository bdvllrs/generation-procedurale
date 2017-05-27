from Map import Map
import matplotlib.pyplot as plt


if __name__ == '__main__':
    m = Map(100)
    m.generate_map(method='perlin', smoothness=2)
    print(m.map)
    plt.imshow(m.map, cmap=plt.cm.binary)
    plt.show()

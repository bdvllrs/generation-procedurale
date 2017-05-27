from Map import Map
from Show import show
#import matplotlib.pyplot as plt

if __name__ == '__main__':
    m = Map(20)
    m.generate_map(random_factor=5)
    print(m.map)
    show(m)
    # plt.imshow(m.map, cmap=plt.cm.binary)
    # plt.show()

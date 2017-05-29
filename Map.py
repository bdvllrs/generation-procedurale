# coding: utf-8

import pickle
from Fractal import Fractal


class MapSizeException(Exception):
    pass


class Map:
    def __init__(self, side=None):
        self.map = None
        self.side = side

    def load_map(self, m):
        """
        Charge une carte
        :param map: si map est un string, utilise pickle pour charger
        le fichier, si c'est un tableau, directement utilisé
        """
        if isinstance(m, str):
            self.map, self.side = pickle.load(open(m, 'rb'))
        elif isinstance(m, list):
            self.map, self.side = m, len(m)

    def save_map(self, filename):
        """
        Sauvegarde la carte dans un fichier
        :param filename: nom du fichier
        """
        pickle.dump((self.map, self.side), open(filename, 'ab'))

    def generate_map(self, method='diamond-square', seed=None, random_factor=1,
                     diversity_factor=0, smoothness=5):
        """
        Génère une carte avec l'algo du diamant-carré
        """
        if method == 'diamond-square':
            self.map = Fractal.diamond_square(self.side, random_factor,
                                              diversity_factor, seed=seed)
        elif method == 'alea':
            self.map = Fractal.alea(self.side)
        elif method == 'perlin':
            self.map = Fractal.perlin_noise(self.side, smoothness=smoothness)
        elif method == 'perlin_combined':
            self.map = Fractal.perlin_combined(self.side)

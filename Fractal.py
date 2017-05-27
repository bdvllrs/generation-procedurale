# coding: utf-8

import random as rd
import numpy as np
from math import sqrt


class Fractal:
    @staticmethod
    def diamond_square(side, random_factor=1, diversity_factor=0):
        """
        Génère une carte avec l'algo du diamant-carré
        :param side: coté de la carte à générer
        """
        # Map
        m = np.array([[0 for i in range(side)] for j in range(side)])
        # On initialise les 4 coins
        m[0][0] = rd.randint(-side * random_factor,
                             side * random_factor)
        m[0][side - 1] = rd.randint(-side * random_factor,
                                    side * random_factor)
        m[side - 1][side - 1] = rd.randint(-side * random_factor,
                                           side * random_factor)
        m[side - 1][0] = rd.randint(-side * random_factor,
                                    side * random_factor)
        step = side - 1
        while step > 1:
            middle = step // 2
            # Phase diamand
            for i in range(middle, side, step):
                for j in range(middle, side, step):
                    # Calcul de la moyenne des quatres coins du carré
                    if i + middle < side and j + middle < side: # normalement pas besoin
                        mean = (m[i - middle][j - middle] +
                                m[i - middle][j + middle] +
                                m[i + middle][j - middle] +
                                m[i + middle][j + middle]) / 4
                        # On met a jour le point central
                        m[i][j] = (mean +
                                   (rd.random()*2-1.) * middle * random_factor +
                                   rd.uniform(-step * diversity_factor,
                                              step * diversity_factor))
            # Phase carré
            for i in range(0, side, middle):
                if i % step == 0:
                    offset = middle
                else:
                    offset = 0
                for j in range(offset, side, step):
                    s = 0  # Somme des quatres coins
                    number_of_corners = 0
                    if i >= middle:
                        s += m[i - middle][j]
                        number_of_corners += 1
                    if i + middle < side:
                        s += m[i + middle][j]
                        number_of_corners += 1
                    if j >= middle:
                        s += m[i][j - middle]
                        number_of_corners += 1
                    if j + middle < side:
                        s += m[i][j + middle]
                        number_of_corners += 1
                    m[i][j] = (s / number_of_corners +
                               (rd.random()*2-1) * middle)
            step = middle
        # Normalisation des valeurs
        min_value = m.min()
        m -= min_value  # Fait commencer à 0
        max_value = m.max()
        m = m / max_value
        return m

    @staticmethod
    def perlin_noise(size):
        pass

    @staticmethod
    def alea(side):
        return [[rd.random() for i in range(side)] for j in range(side)]


class PerlinNoise:
    def __init__(self, size=256):
        self.permutation = np.random.permutation(256)
        unit_bisector = sqrt(2) / 2
        self.gradient = [(1, 0), (0, 1), (-1, 0), (0, -1),
                         (unit_bisector, unit_bisector),
                         (unit_bisector, -unit_bisector)
                         (-unit_bisector, unit_bisector),
                         (-unit_bisector, -unit_bisector)]

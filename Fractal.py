# coding: utf-8

import random as rd
import numpy as np
from math import sqrt


class Fractal:
    @staticmethod
    def diamond_square(side, random_factor=1, diversity_factor=0, seed=None):
        """
        Génère une carte avec l'algo du diamant-carré
        :param side: coté de la carte à générer
        """
        # Map
        if(seed is not None):
            rd.seed(seed)
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
                    # normalement pas besoin
                    if i + middle < side and j + middle < side:
                        mean = (m[i - middle][j - middle] +
                                m[i - middle][j + middle] +
                                m[i + middle][j - middle] +
                                m[i + middle][j + middle]) / 4
                        # On met a jour le point central
                        m[i][j] = (mean +
                                   (rd.random() * 2 - 1.) * middle *
                                   random_factor +
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
                               (rd.random() * 2 - 1) * middle)
            step = middle
        # Normalisation des valeurs
        min_value = m.min()
        m -= min_value  # Fait commencer à 0
        max_value = m.max()
        m = m / max_value
        return m

    @staticmethod
    def perlin_noise(side, smoothness=5):
        noise = PerlinNoise(smoothness=smoothness)
        m = np.array([[noise.val(i, j) for i in range(side)]
                      for j in range(side)])
        return m

    @staticmethod
    def noise(x, y, side):
        noise1 = PerlinNoise(smoothness=side)
        permutation = noise1.permutation
        noise2 = PerlinNoise(smoothness=(side // 2), permutation=permutation)
        noise3 = PerlinNoise(smoothness=50, permutation=permutation)
        noise4 = PerlinNoise(smoothness=20, permutation=permutation)
        noise5 = PerlinNoise(smoothness=5, permutation=permutation)
        noise6 = PerlinNoise(smoothness=side)
        noise7 = PerlinNoise(smoothness=side)
        return (0.5 * noise1.val(x, y) +
                # 0.02 * noise6.val(x, y) +
                # 0.01 * noise7.val(x, y) +
                # 0.25 * noise2.val(x, y) +
                # 0.0125 * noise3.val(x, y) +
                # 0.00625 * noise4.val(x, y) +
                0 * noise5.val(x, y))

    @staticmethod
    def perlin_combined(side):
        m = np.array([[Fractal.noise(i, j, side) for i in range(side)]
                      for j in range(side)])
        m -= m.min()
        m = m / m.max()
        return m

    @staticmethod
    def alea(side):
        return [[rd.random() for i in range(side)] for j in range(side)]


class PerlinNoise:
    """
    Create a new Perlin Noise fractal
    :param size: the size of the permutation (default 256)
    :param permutation: if given uses this permutation
    """

    def __init__(self, smoothness=1, size=256, permutation=None, seed=None):
        self.smoothness = smoothness
        if seed is not None:
            np.random.seed(seed)
        if permutation is None:
            self.permutation = np.random.permutation(256)
        else:
            self.permutation = permutation
        # Pour avoir deux fois la permutation
        self.perm = np.concatenate((self.permutation, self.permutation))
        unit_bisector = sqrt(2) / 2
        self.gradients = [(unit_bisector, unit_bisector),
                          (-unit_bisector, unit_bisector),
                          (unit_bisector, -unit_bisector),
                          (-unit_bisector, -unit_bisector),
                          (1, 0), (0, 1), (-1, 0), (0, -1)]

    @staticmethod
    def scalar(x, y):
        return x[0] * y[0] + x[1] * y[1]

    @staticmethod
    def smoth_function(x):
        return 3 * x * x - 2 * x * x * x

    def val(self, x, y):
        x, y = x / self.smoothness, y / self.smoothness
        x0, y0 = int(x), int(y)
        if(x == x0 and y == y0):
            x = x + 0.01
        i = x0
        j = y0
        grad1 = self.perm[i + self.perm[j]] % 8
        grad2 = self.perm[i + 1 + self.perm[j]] % 8
        grad3 = self.perm[i + self.perm[j + 1]] % 8
        grad4 = self.perm[i + 1 + self.perm[j + 1]] % 8
        vect1 = [self.gradients[grad1][0], self.gradients[grad1][1]]
        vect2 = [self.gradients[grad2][0], self.gradients[grad2][1]]
        vect3 = [self.gradients[grad3][0], self.gradients[grad3][1]]
        vect4 = [self.gradients[grad4][0], self.gradients[grad4][1]]
        part_frac_x = x - x0
        part_frac_y = y - y0
        s = self.scalar(vect1, (part_frac_x, part_frac_y))
        t = self.scalar(vect2, (part_frac_x - 1, part_frac_y))
        u = self.scalar(vect4, (part_frac_x, part_frac_y - 1))
        v = self.scalar(vect3, (part_frac_x - 1, part_frac_y - 1))
        Cx = self.smoth_function(part_frac_x)
        Cy = self.smoth_function(part_frac_y)
        Li1 = s + Cx * (t - s)
        Li2 = u + Cx * (v - u)
        return abs(Li1 + Cy * (Li2 - Li1))

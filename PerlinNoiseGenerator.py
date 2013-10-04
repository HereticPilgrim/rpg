"""
Code by: https://code.google.com/p/perlin-noise-island-generator/
"""


import random


class PerlinNoiseGenerator:


    def __init__(self):

        self.noise = []
        self.noise_width = 0
        self.noise_height = 0


    def generate_noise(self, width, height, frequency, octaves):

        """Generates a 2d array of random noise."""

        del self.noise[:]
        self.noise_width = width
        self.noise_height = height

        for y in range(0, self.noise_height):
            noise_row = []
            for x in range(0, self.noise_width):
                noise_row.append(random.randint(0, 1000)/1000.0)
            self.noise.append(noise_row)

        result = []

        for y in range(0, self.noise_height):
            row = []
            for x in range(0, self.noise_width):
                row.append(int(self.turbulence(x*frequency,
                                               y*frequency,
                                               octaves)))
            result.append(row)

        return result


    def smooth_noise(self, x, y):

        """Returns the average value of the 4 neighbors of (x, y) from the
           noise array."""

        fractX = x - int(x)
        fractY = y - int(y)

        x1 = (int(x) + self.noise_width) % self.noise_width
        y1 = (int(y) + self.noise_height) % self.noise_height

        x2 = (x1 + self.noise_width - 1) % self.noise_width
        y2 = (y1 + self.noise_height - 1) % self.noise_height

        value = 0.0
        value += fractX       * fractY       * self.noise[y1][x1]
        value += fractX       * (1 - fractY) * self.noise[y2][x1]
        value += (1 - fractX) * fractY       * self.noise[y1][x2]
        value += (1 - fractX) * (1 - fractY) * self.noise[y2][x2]

        return value


    def turbulence(self, x, y, size):

        """This function controls how far we zoom in/out of the noise array.
           The further zoomed in gives less detail and is more blurry."""

        value = 0.0
        size *= 1.0
        initial_size = size

        while size >= 1:
            value += self.smooth_noise(x / size, y / size) * size
            size /= 2.0

        return 128.0 * value / initial_size

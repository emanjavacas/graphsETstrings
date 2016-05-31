# coding: utf-8

from PIL import Image
import math


class SeamCarver(object):
    def __init__(self, pic):
        self.pic = pic
        self.W, self.H = pic.size
        self.e2d = [[self.energy(x, y) for x in range(self.W)]
                    for y in range(self.H)]

    @classmethod
    def from_file(cls, fname):
        pic = Image.open(fname)
        return cls(pic)

    def width(self):
        return self.W

    def height(self):
        return self.H

    def _gradient(self, pxl1, pxl2):
        return sum([(pxl2[i] - pxl1[i]) ** 2 for i in range(3)])

    def energy(self, x, y):
        if x < 0 or y < 0:
            raise ValueError("x, y must be positive")
        if x >= self.width() or y >= self.height():
            raise ValueError("Pixel out of bounds")
        if x == 0 or y == 0 or x == self.width() - 1 or y == self.height() - 1:
            return 1000
        e, w = self.pic.getpixel((x - 1, y)), self.pic.getpixel((x + 1, y))
        n, s = self.pic.getpixel((x, y - 1)), self.pic.getpixel((x, y + 1))
        Dx = self._gradient(w, e)
        Dy = self._gradient(s, n)
        return math.sqrt(Dx + Dy)

    def _seam_energy(self, seam):
        if len(seam) == self.width():  # horizontal
            return sum([self.e2d[x][y] for x, y in enumerate(seam)])
        elif len(seam) == self.height():  # vertical
            return sum([row[x] for x, row in zip(seam, self.e2d)])
        else:
            raise ValueError("Seam doesn't match image proportions")

    def find_horizontal_seam(self):
        "returns list of row numbers of length image width"
        pass

    def find_vertical_seam(self):
        "returns list of column numbers of length image height"
        seams = []
        for col in range(self.width()):
            seam, current = [], col
            seam.append(current)
            for row in self.e2d[1:]:
                f, t = max(0, current-1), min(self.W-1, current+2)
                current, _ = min(list(enumerate(row))[f:t], key=lambda x: x[1])
                seam.append(current)
            seams.append(seam)
        return seams

    def remove_horizontal_seam(self, seam):
        if len(seam) != self.width():
            raise ValueError("Seam doesn't match image width")

    def remove_vertical_seam(self, seam):
        if len(seam) != self.height():
            raise ValueError("Seam doesn't match image height")

    def energy_pic(self):
        pic = Image.new("RGB", self.pic.size, "black")
        pixels = pic.load()
        for x in range(self.width()):
            for y in range(self.height()):
                pixels[x, y] = (int(self.e2d[y][x]),) * 3
        return pic

    def _seam_pic(self, pic, seam, color=(255, 0, 0)):
        pixels = pic.load()
        if len(seam) == self.width():  # horizontal seam
            for x, y in enumerate(seam):
                pixels[x, y] = color
        elif len(seam) == self.height():  # vertical seam
            for y, x in enumerate(seam):
                pixels[x, y] = color
        else:
            raise ValueError("Seam doesn't match image proportions")
        return pic

    def original_seam_pic(self, seam, **kwargs):
        return self._seam_pic(self.pic, seam, **kwargs)

    def energy_seam_pic(self, seam, **kwargs):
        return self._seam_pic(self.energy_pic(), seam, **kwargs)

    def print_e2d(self):
        return "\n".join([" ".join(map(lambda x: "%10.2f" % x, col))
                          for col in self.e2d])


# carver = SeamCarver.from_file(
#     "/Users/quique/Downloads/seamCarving/HJocean.png")
# seam = carver.find_vertical_seam()
# carver.energy_seam_pic(seam[345]).show()
# print(carver.print_e2d())
# list(enumerate([carver._seam_energy(s) for s in seam]))

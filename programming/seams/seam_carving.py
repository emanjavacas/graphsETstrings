# coding: utf-8

from PIL import Image
import math


class SeamCarver(object):
    def __init__(self, pic):
        self.pic = pic
        self.e2d = self._to_energy_matrix(*pic.size)

    @classmethod
    def from_file(cls, fname):
        pic = Image.open(fname)
        return cls(pic)

    def transpose(self, m):
        return [[m[y][x] for y in range(len(m))] for x in range(len(m[0]))]

    def width(self):
        return self.pic.size[0]

    def height(self):
        return self.pic.size[1]

    def _gradient(self, pxl1, pxl2):
        return sum([(pxl2[i] - pxl1[i]) ** 2 for i in range(3)])

    def _to_energy_matrix(self, w, h):
        return [[self.energy(x, y) for x in range(w)] for y in range(h)]

    def energy(self, x, y):
        if x < 0 or y < 0:
            raise ValueError("x, y must be positive")
        if x >= self.width():
            raise ValueError("Pixel x [%d] out of bounds" % x)
        if y >= self.height():
            raise ValueError("Pixel y [%d ]out of bounds" % y)
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

    def _check_seam(self, seam):
        for idx, y in enumerate(seam[1:]):
            if abs(y - seam[idx]) > 1:
                raise ValueError("Illegal seam sequence index [%d]" % idx)

    def find_horizontal_seam(self):
        "returns list of row numbers of length image width"
        return self._find_vertical_seam(self.transpose(self.e2d))

    def find_vertical_seam(self):
        return self._find_vertical_seam(self.e2d)

    def _find_vertical_seam(self, m):
        inf = float("inf")
        H, W = len(m), len(m[0])
        edge_to = [[None for _ in range(W)] for _ in range(H)]
        energy_to = [[inf for _ in range(W)] for _ in range(H)]
        energy_to[0] = [1000 for _ in range(W)]
        for x in range(H - 1):  # dont include last row
            for y in range(W):
                for k in range(y - 1, y + 2):
                    if k >= 0 and k < W:
                        # relax
                        current = energy_to[x][y] + m[x + 1][k]
                        if energy_to[x + 1][k] > current:
                            energy_to[x + 1][k] = current
                            edge_to[x + 1][k] = y
        # lookup min and backtrack
        edge, energy = min(zip(edge_to[-1], energy_to[-1]), key=lambda x: x[1])
        seam = [edge]
        for x in range(1, H)[::-1]:
            edge = edge_to[x][edge]
            seam.append(edge)
        return seam[::-1]

    def remove_horizontal_seam(self, seam):
        if len(seam) != self.width():
            raise ValueError("Seam doesn't match image width")
        print(self.width())
        print(self.height())
        self.pic = self.pic.transpose(Image.ROTATE_90)
        self.e2d = self.transpose(self.e2d)
        self.remove_vertical_seam(seam)
        self.pic = self.pic.transpose(Image.ROTATE_270)
        self.e2d = self.transpose(self.e2d)

    def remove_vertical_seam(self, seam):
        if len(seam) != self.height():
            raise ValueError("Seam doesn't match image height")
        pixels = self.pic.load()
        new_im = Image.new('RGB', (self.width()-1, self.height()), "black")
        new_pixels = new_im.load()
        self.pic = new_im
        for y in range(self.height()):
            for x in range(self.width() + 1):
                if x < seam[y]:
                    new_pixels[x, y] = pixels[x, y]
                elif x > seam[y]:
                    new_pixels[x - 1, y] = pixels[x, y]
        for x, y in enumerate(seam):
            del self.e2d[x][y]
            self.e2d[x][y] = self.energy(y, x)
            self.e2d[x][y-1] = self.energy(y-1, x)

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

    def __str__(self):
        return "\n".join([" ".join(map(lambda x: "%10.2f" % x, col))
                          for col in self.e2d])


# carver = SeamCarver.from_file(
#     "/Users/quique/Downloads/seamCarving/HJocean.png")
# carver = SeamCarver.from_file(
#     "/Users/quique/Downloads/seamCarving/12x10.png")

# seam_v = carver.find_vertical_seam()
# carver.energy_seam_pic(seam_v).show()
# carver.remove_vertical_seam(seam_v)

# seam_h = carver.find_horizontal_seam()
# carver.energy_seam_pic(seam_h).show()
# carver.remove_horizontal_seam(seam_h)

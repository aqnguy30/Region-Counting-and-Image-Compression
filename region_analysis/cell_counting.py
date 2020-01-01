import cv2
import numpy as np
from collections import Counter

class cell_counting:

    def _get_sq_window(self, image, x, y):
        coords = []
        subimg = []
        n, m = image.shape
        sq_window = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1), (0, 0), (0, 1)]
        for i, j in sq_window:
            xx = x + i
            yy = y + j

            ii = xx if 0 <= xx < n else 0 if xx < n else n - 1
            jj = yy if 0 <= yy < m else 0 if yy < m else m - 1

            coords.append((ii, jj))
            subimg.append(image[ii, jj] if 0 <= xx < n and 0 <= yy < m else 0.0)

        return coords, subimg

    def _pick_from_candidates(self, regions):
        counter = Counter(regions)
        reg, count = counter.most_common(1)[0]

        # Pick the most common color
        if reg != 0.0 and count > 2:
            return reg

        # Pick the first region that comes across
        for region in regions:
            if region:
                return region
        return 0.0

    def blob_coloring(self, image):
        """Uses the blob coloring algorithm based on 5 pixel cross window assigns region names
        takes a input:
        image: binary image
        return: a list of regions"""

        k = 1
        regions = np.zeros(image.shape)

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):

                px_curr = image[i, j]
                coords, window = self._get_sq_window(image, i, j)

                # Order matters for priority
                candidates = [regions[coords[0]], regions[coords[1]], regions[coords[2]], regions[coords[3]]]
                cand_color = self._pick_from_candidates(candidates)

                if cand_color and px_curr:
                    for l, px in enumerate(
                            window[:]):  # Tagging all the neighbors or just the seen ones yielded the same
                        if px:
                            regions[coords[l]] = cand_color
                elif px_curr:
                    regions[i, j] = k
                    k += 1

        return regions

        #regions = dict()

        #return regions

    def compute_statistics(self, region, filter = 15):
        """Compute cell statistics area and location
        takes as input
        region: a list of pixels in a region
        returns: area"""

        labels = dict()
        rows = region.shape[0]
        cols = region.shape[1]

        for i in range(rows):
            for j in range(cols):
                label = region[i, j]
                if label:  # 0.0 is not a label
                    pixel = [(i, j)]
                    labels[label] = labels[label] + pixel if label in labels else pixel

        stats = dict()
        for label in labels:
            area = len(labels[label])

            if area > filter:
                ranges = list(zip(*labels[label]))

                i_center = int(sum(ranges[0]) / area)
                j_center = int(sum(ranges[1]) / area)

                stat = {
                    'area': area,
                    'centroid': (i_center, j_center)
                }

                stats[label] = stat
                print("Region: {},\tArea: {},\tCentroid: {}".format(label, area, stat['centroid']))

        return stats

        # Please print your region statistics to stdout
        # <region number>: <location or center>, <area>
        # print(stats)

        #return 0

    def mark_regions_image(self, regions, stats):
        """Creates a new image with computed stats
        takes as input
        image: a list of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""

        image = np.zeros(regions.shape)

        for i in range(regions.shape[0]):
            for j in range(regions.shape[1]):
                if regions[i, j] in stats:
                    image[i, j] = 255
        c = 1
        for stat in stats.values():
            text = '*' + str(c) + str(',') + str(stat['area'])
            x, y = stat['centroid']
            cv2.putText(image, text, (y, x), cv2.FONT_HERSHEY_PLAIN, 0.5, 0)
            c += 1
        return image

        #return image


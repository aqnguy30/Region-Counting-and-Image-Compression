import numpy as np

class binary_image:

    def standarize_background(self, bin_image):
        counter = {0: 0, 255: 0}
        for row in range(bin_image.shape[0]):
            for col in range(bin_image.shape[1]):
                counter[bin_image[row, col]] += 1

        if counter[255] > counter[0]:
            print("Switching colors to get a black background")
            return np.array([[0 if bin_image[row, col] else 255
                              for col in range(bin_image.shape[1])]
                             for row in range(bin_image.shape[0])])
        return bin_image

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram"""

        hist = [0]*256

        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                hist[image[row, col]] += 1

        return hist

    def find_optimal_threshold(self, hist):
        """analyses a histogram it to find the optimal threshold value assuming a bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value"""

        #threshold = 0

        total1 = sum(hist[:len(hist)//2])  # The sum of all the frequencies
        total2 = sum(hist[len(hist)//2:])
        hsize = len(hist)  # The number of K-levels

        n_hist1 = [value / total1 for value in hist]  # Normalized histogram
        n_hist2 = [value / total2 for value in hist]
        k_half = round(len(hist) / 2)  # Calculating halves

        thresh = k_half  # Initializing threshold
        m1, m2 = 0, 0  # Initializing means

        while True:
            exp_1 = sum([k * n_hist1[k] for k in range(0, k_half)])
            exp_2 = sum([k * n_hist2[k] for k in range(k_half, hsize)])

            thresh = (exp_1 + exp_2) / 2

            if m1 - exp_1 != 0 and m2 - exp_2 != 0:
                m1 = exp_1
                m2 = exp_2
            else:
                break

        return thresh


        #return threshold

    def binarize(self, image, threshold):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        take as input
        image: an grey scale image
        returns: a binary image"""

        #bin_img = image.copy()

        bin_img = np.zeros(image.shape)

        for row in range(bin_img.shape[0]):
            for col in range(bin_img.shape[1]):
                if image[row, col] < threshold:
                    bin_img[row, col] = 255

        bin_img = self.standarize_background(bin_img)

        return bin_img

        #return bin_img



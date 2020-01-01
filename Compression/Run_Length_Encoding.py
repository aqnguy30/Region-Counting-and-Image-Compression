from itertools import chain

import numpy as np

class rle:

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        last_pixel = binary_image[0,0]
        c = 0
        rle_code = []

        for x in range(0, binary_image.shape[0]):
            for y in range(0, binary_image.shape[1]):
                if last_pixel == binary_image[x,y]:
                    c += 1
                else:
                    rle_code.append(c)
                    last_pixel = binary_image[x,y]
                    c = 1
        rle_code.append(c)


        #return [str(i), last_pixel] + encode_image(binary_image[i:])
        return rle_code
        #return np.zeros(100) #replace zeros with rle_code



    def decode_image(self, rle_code, height , width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """
        lst = []
        for i in range (0, len(rle_code)):
            if i % 2 == 0:
                lst.append([0] * rle_code[i])
            else: lst.append([255] * rle_code[i])
        a = np.array(sum(lst, []))
        binary_image = np.reshape(a, (height, width))

        return binary_image




        #return  np.zeros((100,100), np.uint8) #replace zeros with image reconstructed from rle_Code





        





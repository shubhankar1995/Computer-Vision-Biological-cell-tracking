import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
# from uitl.plot import plot_image


class Watershed:
    def __init__(self, image):
        self.image = image.copy()

    def perform(self):
        distance = ndi.distance_transform_edt(self.image)
        # Testing the distance transform
        # plt.imshow(distance)
        # plt.savefig('results/distance.png')

        local_maxi = peak_local_max(
            distance, indices=False, labels=self.image,
            footprint=np.ones((21, 21))
        )
        markers = ndi.label(local_maxi)[0]

        ws_labels = watershed(-distance, markers, mask=self.image)

        return ws_labels

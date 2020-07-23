import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import sys

from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max

from preprocessor import Preprocessor
from segment_finder import SegmentFinder
from boxes_drawer import BoxesDrawer


class Watershed:
    def __init__(self, image, mode):
        self.image = image.copy()
        self.mode = mode

    def perform(self):
        distance = ndi.distance_transform_edt(self.image)
        # Testing the distance transform
        # plt.imshow(distance)
        # plt.savefig('results/distance.png')

        if self.mode == 1:  # Fluo
            local_maxi = peak_local_max(
                distance, indices=False, labels=self.image,
                threshold_abs=3,
                footprint=np.ones((9, 9))
            )
        else:               # PhC
            local_maxi = peak_local_max(
                distance, indices=False, labels=self.image,
                footprint=np.ones((9, 9))
            )
        markers = ndi.label(local_maxi)[0]

        return watershed(-distance, markers, mask=self.image)


# Used for experiments
if __name__ == '__main__':
    # Check argv
    if len(sys.argv) < 3:
        sys.exit(
            'Wrong number of arguments.\n'
            'Parameters: filepath mode\n'
            f'Example: python3 {sys.argv[0]} path/to/image 1\n'
            'Modes are 0: DIC, 1: Fluo, 2: PhC'
        )

    image = cv.imread(sys.argv[1], cv.IMREAD_GRAYSCALE)
    mode = int(sys.argv[2])

    orig_image = image.copy()
    cv.imwrite('results/original.png', orig_image)
    # Preprocess image
    image = Preprocessor(image, mode).preprocess()
    prep_image = image.copy()
    cv.imwrite('results/prep.png', prep_image)

    # Segment image
    distance = ndi.distance_transform_edt(image)

    # Testing the distance transform
    # plt.imshow(distance)
    # plt.savefig('results/distance.png')

    if mode == 1:
        local_maxi = peak_local_max(
            distance, indices=False, labels=image,
            threshold_abs=3,
            footprint=np.ones((9, 9))
        )
    else:
        local_maxi = peak_local_max(
            distance, indices=False, labels=image,
            footprint=np.ones((9, 9))
        )

    markers = ndi.label(local_maxi)[0]

    segmented_image = watershed(-distance, markers, mask=image)

    # Find segments
    segments = SegmentFinder(segmented_image).find()

    # Draw bounding box
    boxed_orig_image = BoxesDrawer(segments, orig_image).draw()
    cv.imwrite('results/boxed_orig.png', boxed_orig_image)
    boxed_prep_image = BoxesDrawer(segments, prep_image).draw()
    cv.imwrite('results/boxed_prep.png', boxed_prep_image)

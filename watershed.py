from scipy import ndimage as ndi
from skimage.morphology import watershed
from skimage.feature import peak_local_max
from uitl.plot import plot_image

class Watershed:
    def __init__(self, image):
        self.image = image


    def perform(self):
        img_array = self.image
        distance = ndi.distance_transform_edt(img_array)
        plot_image('water.jpg', distance, 'distance')
        local_maxi = peak_local_max(distance, indices=False, labels=img_array)
        markers = ndi.label(local_maxi)[0]

        ws_labels = watershed(-distance, markers, mask=img_array)

        return ws_labels
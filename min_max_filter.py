import numpy as np
import cv2 as cv

class MinMaxFilter:
    def __init__(self, image, neighborhood_size=35, is_min_max=True):
        self.image = image
        self.neighborhood_size = neighborhood_size
        self.is_min_max = is_min_max
    
    def filter(self):
        background = self.get_background()
        cv.imwrite('background.png', background)        # TODO: remove
        return cv.subtract(self.image, self.get_background())
    
    def get_background(self):
        min_filtered = self.neighbor_filter(self.image, self.is_min_max)
        return self.neighbor_filter(min_filtered, not self.is_min_max)
        
    def neighbor_filter(self, image, is_min):
        # Copy image
        copied_image = image.copy()

        # Iterate pixels
        for (r, c), _ in np.ndenumerate(image):
            # Get neighborhood max or min
            neighborhood = self.get_neighborhood(image, r, c)
            if is_min:
                value = neighborhood.min()
            else:
                value = neighborhood.max()
            copied_image[r, c] = value
        return copied_image
            
    def get_neighborhood(self, image, r, c):
        rows, cols = image.shape
        # X coordinates
        start_x_i = c - self.neighborhood_size // 2
        end_x_i = start_x_i + self.neighborhood_size
        start_x = max(0, start_x_i)
        end_x = min(cols, end_x_i)
        # Y coordinates
        start_y_i = r - self.neighborhood_size // 2
        end_y_i = start_y_i + self.neighborhood_size
        start_y = max(0, start_y_i)
        end_y = min(rows, end_y_i)
        # Slice
        return image[start_y:end_y, start_x:end_x]
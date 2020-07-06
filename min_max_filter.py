class MinMaxFilter:
    def __init__(self, image, neighborhood_size):
        self.image = image
        self.neighborhood_size = neighborhood_size
    
    def filter(self):
        return MinMaxFilter.invert(
            MinMaxFilter.invert(self.image) 
            -
            MinMaxFilter.invert(self.get_background())
        )
    
    def get_background(self):
        max_filtered = neighbor_filter(True)
        return neighbor_filter(False)
        
    def neighbor_filter(self, is_max):
        # Copy image
        copied_image = self.image.copy()

        # Iterate pixels
        for (r, c), _ in np.ndenumerate(self.image):
            # Get neighborhood max or min
            neighborhood = get_neighborhood(r, c)
            if is_max:
                value = neighborhood.max()
            else:
                value = neighborhood.min()
            copied_image[r, c] = value
        return copied_image
            
    def get_neighborhood(self, r, c):
        rows, cols = self.image.shape
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
        return self.image[start_y:end_y, start_x:end_x]

    def invert(image):
        return 255 - image
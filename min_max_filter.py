class MinMaxFilter:
    def __init__(self, image, neigh_size):
        self.image = image
        self.neigh_size = neigh_size
    
    def filter(self):
        invert(invert(self.image) - invert(self.get_background())
    
    def get_background(self):
        a = neighbor_filter(i, N, True)
        b = neighbor_filter(a, N, False)
        return b
        
    def neigh_filter(img, N, is_max):
        # Copy image
        out = self.image.copy()

        # Iterate pixels
        rows, cols = self.image.shape
        for (r, c), _ in np.ndenumerate(img):
            # Get neighborhood max or min
            neigh = neighborhood_of(self.image, r, c, self.neigh_size, rows,
                                    cols)
            if is_max:
                val = neigh.max()
            else:
                val = neigh.min()
            out[r, c] = val
        return out
            
    def get_neighborhood(self, r, c, N, rows, cols):
        # X coordinates
        start_x_i = c - N // 2
        end_x_i = start_x_i + N
        start_x = max(0, start_x_i)
        end_x = min(cols, end_x_i)
        # Y coordinates
        start_y_i = r - N // 2
        end_y_i = start_y_i + N
        start_y = max(0, start_y_i)
        end_y = min(rows, end_y_i)
        # Slice
        return self.image[start_y:end_y, start_x:end_x]

def invert(img):
    return 255 - img

if __name__ == '__main__':
    i = cv.imread('Particles.png', cv.IMREAD_GRAYSCALE)
    b = extract_background(i, 11, 0)
    cv.imwrite('results/task1/B11.png', b)
    o = subtract_background(i, b, 0)
    cv.imwrite('results/task2/O.png', o)

    i = cv.imread('Cells.png', cv.IMREAD_GRAYSCALE)
    b = extract_background(i, 35, 1)
    cv.imwrite('results/task3/B35.png', b)
    o = subtract_background(i, b, 1)
    cv.imwrite('results/task3/O35.png', o)
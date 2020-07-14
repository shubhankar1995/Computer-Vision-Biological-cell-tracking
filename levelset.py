import numpy as np
from preprocessor import Preprocessor
import cv2 as cv


class Levelset:
    def __init__(self, image):
        self.image = image

    def grad(self,x):
        return np.array(np.gradient(x))

    def norm(self,x, axis=0):
        return np.sqrt(np.sum(np.square(x), axis=axis))

    def stopping_fun(self,x):
        return 1. / (1. + self.norm(self.grad(x)) ** 2)

    def default_phi(self,x):
        # Initialize surface phi at the border (5px from the border) of the image
        # i.e. 1 outside the curve, and -1 inside the curve
        phi = np.ones(x.shape[:2])
        phi[5:-5, 5:-5] = -1.
        return phi

    def perform(self):

        F = self.stopping_fun(self.image)
        phi = self.default_phi(self.image)

        dt = 1
        n_iter = 100
        for i in range(n_iter):
            dphi = self.grad(phi)
            dphi_norm = self.norm(dphi)

            dphi_t = F * dphi_norm

            phi = phi + dt * dphi_t
            # plt.contour(phi, 0)
            # plt.show()

        return phi


# if __name__ == '__main__':
#     image = cv.imread('/Users/apple/Documents/COMP9517/9517project/images/Fluo-N2DL-HeLa/Sequence 1/t000.tif', cv.IMREAD_GRAYSCALE)
#     image = Preprocessor(image).preprocess()
#     print(image.max())
#     image=Levelset(image).perform()
#     print(image.shape)
#     cv.imwrite('inter/fimage.png',image)
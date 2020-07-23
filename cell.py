class Cell:
    def __init__(self, idx, origin, mileage=0):
        self.id = idx
        self.origin = origin
        self.mileage = mileage
        self.deleted = False    # Is this a segmentation error?

    def copy(self):
        return Cell(self.id, self.origin, self.mileage)

    def delete(self):
        self.deleted = True

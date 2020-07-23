class Cell:
    def __init__(self, idx, origin, mileage=0):
        self.id = idx
        self.origin = origin
        self.mileage = mileage

    def copy(self, idx):
        return Cell(idx, self.origin, self.mileage)

    def update_mileage(self, addition):
        self.mileage += addition

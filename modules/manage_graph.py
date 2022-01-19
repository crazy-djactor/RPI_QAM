class ManageGraph:
    def __init__(self):
        self.o2data_max = 10
        self.o2data_min = 0
        self.h2odata_max = 10
        self.h2odata_min = 0
        pass

    def update_o2_values(self, o2):
        if abs(self.o2data_max - o2) > 1000:
            return False
        if abs(self.o2data_min - o2) > 1000:
            return False

        if self.o2data_max < o2:
            self.o2data_max = o2

        if self.o2data_min > o2:
            self.o2data_min = o2
        return True

    def update_h2o_values(self, h2o):
        if abs(self.h2odata_max - h2o) > 1000:
            return False
        if abs(self.h2odata_min - h2o) > 1000:
            return False

        if self.h2odata_max < h2o:
            self.h2odata_max = h2o

        if self.h2odata_min > h2o:
            self.h2odata_min = h2o
        return True

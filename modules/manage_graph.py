class ManageGraph:
    def __init__(self):
        self.o2data_max = 10
        self.o2data_min = 0
        self.h2odata_max = 10
        self.h2odata_min = 0
        self.o2xList = []
        self.o2yList = []
        self.o2data_string = ""
        self.o2dataList = []

        self.h2oxList = []
        self.h2oyList = []
        self.h2odata_string = ""
        self.h2odataList = []
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

    def update_o2_dataList(self, o2, o2time):
        self.o2data_string = f"{self.o2data_string}\n{str(round((o2time.total_seconds()) / 60, 0))},{o2}"
        ############################
        self.o2dataList = self.o2data_string.split('\n')
        self.o2dataList.pop(0)
        initial_tick = self.o2dataList[0].split(',')
        # print(initial_tick[1])
        self.o2dataList[0] = "0," + initial_tick[1]
        self.o2xList = []
        self.o2yList = []
        for eachLine in self.o2dataList:
            if len(str(eachLine)) > 1:
                x1, y1 = eachLine.split(',')
                self.o2xList.append(float(x1))
                self.o2yList.append(float(y1))

    def update_h2o_dataList(self, h2o, h2otime):
        self.h2odata_string = f"{self.h2odata_string}\n{str(round((h2otime.total_seconds()) / 60, 0))},{h2o}"
        ############################
        self.h2odataList = self.h2odata_string.split('\n')
        self.h2odataList.pop(0)
        initial_tick = self.h2odataList[0].split(',')
        # print(initial_tick[1])
        self.h2odataList[0] = "0," + initial_tick[1]
        self.h2oxList = []
        self.h2oyList = []
        for eachLine in self.h2odataList:
            if len(str(eachLine)) > 1:
                x1, y1 = eachLine.split(',')
                self.h2oxList.append(float(x1))
                self.h2oyList.append(float(y1))


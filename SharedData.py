class SharedData:
    def __init__(self):
        self.data = {}
        self.data['rgb'] = None
    
    def setData(key, value):
        self.data[key] = value

    def checkData(key):
        ret = None
        if key in self.data:
            ret = self.data[key]

        return ret

    def getData(key):
        ret = None
        if key in self.data:
            ret = self.data[key]
            self.data[key] = None

        return ret

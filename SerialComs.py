import serial, re

class SerialComs:
    def __init__(self, **kwargs):
        port = '/dev/ttyUSB0' if 'port' not in kwargs else kwargs['port']
        baudrate = 9600 if 'baudrate' not in kwargs else kwargs['baudrate']

        self.com = serial.Serial(port, baudrate, timeout=1)

    def write(self, msg):
        msg = str.encode(str(msg))
        self.com.write(msg)
        self.flush()

    def read(self):
        self.flush()
        return self.com.readline().decode().strip()

    def flush(self):
        self.com.flush()


class MDComs(SerialComs):
    MSG_FORMAT = 'state:(?P<state>[a-zA-Z:_]+);pirOutput:(?P<pirOutput>[a-zA-Z:]+);color:(?P<color>.*)'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.msgPattern = re.compile(MDComs.MSG_FORMAT)

    def read(self):
        data = super().read()
        #print(data)
        
        match = self.msgPattern.search(data)

        ret = None
        if match is not None:
            ret = {
                    'state' : match.group('state'),
                    'pirOutput' : match.group('pirOutput'),
                    'color' : match.group('color')
            }
        
        #print(ret)

        return ret

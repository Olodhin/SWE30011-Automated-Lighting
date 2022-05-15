from MotionDetectorServer import startServer 
from SharedData import SharedData

import serial, threading, re, pymysql

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
    MSG_FORMAT = 'state:(?P<state>[a-zA-Z:_]+);pirOutput(?P<pirOutput>[a-zA-Z:]+);color:(?P<color>.*)'

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


class DBComs:
    def __init__(self, **kwargs):
        host = 'localhost' if 'host' not in kwargs else kwargs['host']
        user = 'pi' if 'user' not in kwargs else kwargs['user']
        pwd = '' if 'pwd' not in kwargs else kwargs['pwd']
        db = 'ovenDB' if 'db' not in kwargs else kwargs['db']

        self.com = pymysql.connect(
            host=host,
            user=user,
            password=pwd,
            database=db,
            cursorclass=pymysql.cursors.DictCursor
        ) or die('failed to connect')

        with self.com:
            self.cursor = self.com.cursor

    def commit(self, table, colNames, data):
        colNames = ', '.join(colNames)
        data = ', '.join(data)
        command = 'INSERT INTO {} ({}}) VALUES ({})'.format(table, colNames, data)
        self.cursor.execute(command)
        self.com.commit()

def checkCommand(sharedData):
    ret = None
    
    colorSet = sharedData.checkData('colors')
    print('colorSet ', colorSet)
    if colorSet != '0,0,0':
        ret = colorSet
        sharedData.getData('colors')

    return ret


if __name__ == '__main__':
    sharedData = SharedData()
    SerialComs = MDComs(port='/dev/ttyS2', baudrate=9600)
    dbCon = DBComs()
    dbTable = 'MotionDetectorLog'

    flaskThread = threading.Thread(target=startServer, args=(sharedData,'127.0.0.1', 8080, False,))
    flaskThread.start()

    while True:
        try:
            data = SerialComs.read()
            print(data)
            # wait for data from node
            if data is None:
                continue

            cols = ['state', 'pirOutput', 'color']
            #dbCon.commit(dbTable, cols, data)

            cmd = checkCommand(sharedData)
            if cmd != None:
                rgb = cmd.split(',')
                command = 'r:{},g:{},b:{}'.format(rgb[0], rgb[1], rgb[2])
                SerialComs.write(command)
                print(command)
        except UnicodeDecodeError as e:
            print('UnicodeDecodeError')
            continue
        except serial.SerialException as e:
            print('Serial Exception')
            continue

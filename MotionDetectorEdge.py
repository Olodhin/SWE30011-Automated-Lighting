from SerialComs import MDComs
from DBComs import DBComs
from MotionDetectorServer import startServer
from MQTT import MQTT
from SharedData import SharedData

import serial, threading

class MotionDetectorEdge:
    def __init__(self, **kwargs):
        # variables
        serialPort = kwargs['serial']['port']
        serialBaudrate = kwargs['serial']['baudrate']

        dbHost = kwargs['db']['host']
        dbUser = kwargs['db']['user']
        dbPwd = kwargs['db']['pwd']
        dbName = kwargs['db']['name']
        dbTName = kwargs['db']['tableName']
        dbCols = kwargs['db']['cols']
        dbDict = kwargs['db']

        flaskHost = kwargs['flask']['ip']
        flaskPort = kwargs['flask']['port']
        flaskDebug = kwargs['flask']['debug']

        mqttUser = kwargs['mqtt']['user']
        mqttPwd = kwargs['mqtt']['pwd']
        mqttHost = kwargs['mqtt']['host']
        mqttPort = kwargs['mqtt']['port']
        mqttTopic = kwargs['mqtt']['topic']

        # shared data
        self.data = SharedData()

        # serial
        self.serial = MDComs(
            port=serialPort,
            baudrate=serialBaudrate
        )

        # db
        self.db = DBComs(
            host=dbHost,
            user=dbUser,
            pwd=dbPwd,
            dbName=dbName
        )
        self.dbTName = dbTName
        self.dbCols = dbCols
        self.dbDict = dbDict

        # mqtt
        self.mqtt = MQTT(
            username=mqttUser,
            password=mqttPwd,
            host=mqttHost,
            port=mqttPort
        )
        self.mqttTopic = mqttTopic

        # flask
        self.flaskHost = flaskHost
        self.flaskPort = flaskPort
        self.flaskDebug = flaskDebug

    def checkCommand(self, data):
        ret = None

        colorSet = data.checkData('colors')
        #print('colorSet ', colorSet)
        if colorSet != '0,0,0':
            ret = colorSet
            data.getData('colors')

        return ret

    def formatDB(self, data):
        state = data['state']
        pir = data['pirOutput']
        color = data['color']

        # Format to string
        state = '\"{}\"'.format(state)
        pir = '1' if pir == 'HIGH' else '0'
        color = '\"{}\"'.format(color)

        ret = [state, pir, color]
        return ret

    def formatMQTT(self, data):
        msg1 = '\"state\":\"{}\"'.format(data['state'])
        msg2 = '\"pirOutput\":\"{}\"'.format(data['pirOutput'])
        msg3 = '\"color\":\"{}\"'.format(data['color'])

        msg = '{' + msg1 + ',' + msg2 + ',' + msg3 + '}'
        return msg

    def run(self):
        # start flask
        flaskThread = threading.Thread(
            target=startServer,
            args=(
                self.data,
                self.dbDict,
                self.flaskHost,
                self.flaskPort,
                self.flaskDebug,
            )
        )
        flaskThread.start()

        while True:
            try:
                data = self.serial.read()
                print('ser: ', data)

                # wait for data from node
                if data is None:
                    continue

                dbData = self.formatDB(data)
                self.db.commit(
                    self.dbTName, 
                    self.dbCols, 
                    dbData
                )

                mqttMsg = self.formatMQTT(data)
                #print(mqttMsg)
                self.mqtt.publish(
                    mqttMsg,
                    self.mqttTopic
                )

                cmd = self.checkCommand(self.data)
                if cmd != None:
                    rgb = cmd.split(',')
                    command = 'r:{},g:{},b:{}'.format(rgb[0],rgb[1],rgb[2])
                    self.serial.write(command)
                    # print(command)
            except UnicodeDecodeError as e:
                print('unicode decode error')
                continue
            except serial.SerialException as e:
                print('serial exception')
                continue
    

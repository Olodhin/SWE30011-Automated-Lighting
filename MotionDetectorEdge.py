from SerialComs import MDComs
from DBComs import DBComs
from MotionDetectorServer import startServer
from MQTT import MQTT
from MQTTClient import MQTTClient
#from SharedData import SharedData

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

        #mqttUser = kwargs['mqtt']['user']
        #mqttPwd = kwargs['mqtt']['pwd']
        mqttHost = kwargs['mqtt']['host']
        mqttPort = kwargs['mqtt']['port']
        mqttPubTopic = kwargs['mqtt']['pubTopic']
        mqttSubTopic = kwargs['mqtt']['subTopics']

        tbHost = kwargs['tb']['host']
        tbPort = kwargs['tb']['port']
        tbUser = kwargs['tb']['user']
        tbPwd = kwargs['tb']['pwd']
        tbPubTopic = kwargs['tb']['pubTopic']

        webHost = kwargs['web']['host']
        webPort = kwargs['web']['port']
        webPubTopic = kwargs['web']['pubTopic']

        # shared data
        #self.data = SharedData()

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
        #self.mqtt = MQTT(
        #    username=mqttUser,
        #    password=mqttPwd,
        #    host=mqttHost,
        #    port=mqttPort
        #)
        self.mqtt = MQTTClient(
            host=mqttHost,
            port=mqttPort,
            onMessage=self.mqttOnMessage,
            subTopic=mqttSubTopic
        )
        self.mqttPubTopic = mqttPubTopic
        self.tb = MQTTClient(
            host=tbHost,
            port=tbPort,
            user=tbUser,
            pwd=tbPwd
        )
        self.tbPubTopic = tbPubTopic
        self.web = MQTTClient(
            host=webHost,
            port=webPort,
        )
        self.webPubTopic = webPubTopic

        # flask
        self.flaskHost = flaskHost
        self.flaskPort = flaskPort
        self.flaskDebug = flaskDebug

        # commmand buffer
        self.cmdBuffer = []

    #def checkCommand(self, data):
    #    ret = None

    #    colorSet = data.checkData('colors')
    #    #print('colorSet ', colorSet)
    #    if colorSet != '0,0,0':
    #        ret = colorSet
    #        data.getData('colors')

    #    return ret

    def mqttOnMessage(self, mqttc, obj, msg):
        print('topic: ', msg.topic)
        print('msg: ', msg.payload)
        self.cmdBuffer.append(msg.payload.decode())

    def checkCommand(self, buf):
        ret = None

        if len(buf) > 0:
            ret = buf.pop(0)

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
        #flaskThread = threading.Thread(
        #    target=startServer,
        #    args=(
        #        self.data,
        #        self.dbDict,
        #        self.flaskHost,
        #        self.flaskPort,
        #        self.flaskDebug,
        #    )
        #)
        #flaskThread.start()

        mqttThread = threading.Thread(
            target=self.mqtt.loop
        )
        mqttThread.start()

        tbThread = threading.Thread(
            target=self.tb.loop        
        )
        tbThread.start()

        webThread = threading.Thread(
            target=self.web.loop
        )
        webThread.start()

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

                # publish to ThingsBoard
                mqttMsg = self.formatMQTT(data)
                self.web.publish(
                    data['state'],
                    self.webPubTopic
                )
                #print(mqttMsg)
                self.tb.publish(
                    mqttMsg,
                    self.tbPubTopic
                )

                cmd = self.checkCommand(self.cmdBuffer)
                if cmd != None:
                    command = cmd
                    if len(cmd) > 2:
                        rgb = cmd.split(',')
                        command = 'r:{},g:{},b:{}'.format(rgb[0],rgb[1],rgb[2])
                   
                    self.serial.write(command)
                    print(command)
            except UnicodeDecodeError as e:
                print('unicode decode error')
                continue
            except serial.SerialException as e:
                print('serial exception')
                continue
    

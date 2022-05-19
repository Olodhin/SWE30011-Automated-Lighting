import paho.mqtt.publish as mqttPublish
import paho.mqtt.client as client
import os

class MQTT:
    def __init__(self, **kwargs):
        username = None
        password = None

        host = '127.0.0.1'
        port = 1883

        if 'username' in kwargs:
            username = kwargs['username']
        if 'password' in kwargs:
            password = kwargs['password']
        if 'host' in kwargs:
            host = kwargs['host']
        if 'port' in kwargs:
            port = kwargs['port']

        self.auth = {
            'username' : username,
            'password' : password
        }
        self.tkn = password
        self.host = host
        self.port = port


    def publish(self, msg, topic):
        #mqttPublish.single(
        #    topic, 
        #    msg,
        #    hostname=self.host,
        #    auth=self.auth,
        #    port=self.port
        #)

        cmd = 'mosquitto_pub -d -q 1 -h \"{}\" -p {} -u \"{}\" -t {} -m {}'.format(
            self.host, self.port, self.tkn, topic, msg
        )
        ost.system

if __name__ == '__main__':
    #c = client.Client()
    #c.username_pw_set('Dist')
    #c.connect('192.168.43.194', 1883, 60)
    #c.loop_start()
    #c.publish('v1/devices/me/telemetry', '{\"testMsg\":5}', 1)
    #print('pubDone')
    host = '\"192.168.43.194\"'
    port = 1883
    topic = 'v1/devices/me/telemetry'
    msg = '{\"testing\":200}'
    tkn = '\"PIR\"'

    cmd = 'mosquitto_pub -d -q 1 -h {} -p {} -u {} -t {} -m {} > /dev/null'.format(
        host, port, tkn, topic, msg
    )
    print(cmd)
    os.system(cmd)

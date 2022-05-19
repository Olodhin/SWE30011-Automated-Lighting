import paho.mqtt.publish as mqttPublish
import paho.mqtt.client as client

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
        self.host = host
        self.port = port


    def publish(self, msg, topic):
        mqttPublish.single(
            topic, 
            msg,
            hostname=self.host,
            auth=self.auth,
            port=self.port
        )

if __name__ == '__main__':
    mDict = {
        'username' : '',
        'password' : ''
    }
    mqtt = MQTT(**mDict)
    mqtt.publish('Test', '/test')

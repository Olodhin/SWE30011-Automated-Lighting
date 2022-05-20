import paho.mqtt.client as client

class MQTTClient:
    def __init__(self, **kwargs):
        self.client = client.Client()
        
        if 'onConnect' in kwargs:
            self.client.on_connect = kwargs['onConnect']
        if 'onMessage' in kwargs:
            self.client.on_message = kwargs['onMessage']
        if 'onPublish' in kwargs:
            self.client.on_publish = kwargs['onPublish']

        host = kwargs['host'] if 'host' in kwargs else '127.0.0.1'
        port = kwargs['port'] if 'port' in kwargs else 1883
        self.connect(host, port, 60)

    def publish(self ,msg, topic, qos=0):
        self.client.publish(topic, msg, qos=qos)

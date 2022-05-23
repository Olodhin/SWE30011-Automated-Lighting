import paho.mqtt.client as client

class MQTTClient:
    def __init__(self, **kwargs):
        self.client = client.Client()
        
        if 'onConnect' in kwargs:
            self.client.on_connect = kwargs['onConnect']
        if 'onMessage' in kwargs:
            self.client.on_message = kwargs['onMessage']
        else:
            self.client.on_message = MQTTClient.onMessage
        if 'onPublish' in kwargs:
            self.client.on_publish = kwargs['onPublish']
        self.client.on_subscribe = onSub

        user = kwargs['user'] if 'user' in kwargs else None
        pwd = kwargs['pwd'] if 'pwd' in kwargs else None
        host = kwargs['host'] if 'host' in kwargs else '127.0.0.1'
        port = int(kwargs['port']) if 'port' in kwargs else 1883
        subTopic = kwargs['subTopic'] if 'subTopic' in kwargs else None
        
        if user is not None:
            self.client.username_pw_set(user)
        
        self.client.connect(host, port, 60)
        if subTopic is not None:
            for topic in subTopic:
                self.client.subscribe(topic, 0)

    def loop(self):
        self.client.loop_forever()

    def onMessage(client, obj, msg):
        print('received: ', msg.payload.decode())

    def onSub(client, obj, mid, qos):
        print('subscribed')

    def publish(self ,msg, topic, qos=0):
        self.client.publish(topic, msg, qos=qos)

def onMessage(mqttc, obj, msg):
    print(msg.payload)

def onConnect(mqttc, obj, flags, rc):
    print('connected')
    print('rc: ', str(rc))

def onSub(mqttc, obj, mid, granted_qos):
    print('subscribed')

def on_log(mqttc, obj, level, string):
    print(string)

if __name__ == '__main__':
    #params = {
    #    'host' : '127.0.0.1',
    #    'port' : 1883,
    #    'onMesssage' : onMessage
    #}
    #cl = MQTTClient(**params)
    cl = client.Client()
    cl.on_message = onMessage
    cl.on_connect = onConnect
    cl.on_subscribe = onSub
    #cl.on_log = on_log
    cl.connect('127.0.0.1', 1883, 60)
    cl.subscribe('test', 0)
    cl.loop_forever()

import paho.mqtt.client as client
import threading

class MQTTClient:
    def onSubscribe(self, client, obj, mid, qos):
        print('{}: Subscribed to {}'.format(
            self.thread.name, str(mid)))

    def onMessage(self, client, obj, msg):
        print('{}: Got message {}'.format(
            self.thread.name, msg.payload.decode()))

    def onPublish(client, obj, mid):
        print('{}: Sending message'.format(self.thread.name))

    def __init__(self, **kwargs):
        self.client = client.Client()

        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = None

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

        self.thread = threading.Thread(name=self.name, target=self.client.loop_forever)

        if 'subscribe' in kwargs:
            for sub in kwargs['subscribe']:
                self.client.subscribe(sub, 0)
    
    def loop(self):
        self.client.loop_forever()

    def onMessage(client, obj, msg):
        print('received: ', msg.payload.decode())

    def onSub(client, obj, mid, qos):
        print('subscribed')
    
    def publish(self ,msg, topic, qos=0):
        self.client.publish(topic, msg, qos=qos)

    def startLoopThread(self):
        print('{}: STARTING'.format(self.thread.name))
        self.thread.start()
        print('{}: STARTED'.format(self.thread.name))


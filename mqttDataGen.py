from MQTTClient import MQTTClient as client
import threading
import numpy as np
import time

clients = []

host = '127.0.0.1'
port = 1883

cl1 = client(
    name='climate control',
    host=host,
    port=port,
    subscribe=['topic/fanState']
)

cl2 = client(
    name='auto doors',
    host=host,
    port=port,
    subscribe=['topic/doorState']
)

cl3 = client(
    name='auto lights',
    host=host,
    port=port,
    subscribe=['lighting/rgb', 'lighting/on']
)

print('starting threads')

cl1.startLoopThread()
cl2.startLoopThread()
cl3.startLoopThread()

print('running data generation')

while True:
    data = np.random.normal(20, 4, 10)
    data = str(data[0])
    cl1.publish(data, 'topic/fanPub')
    time.sleep(1)

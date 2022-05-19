import flask
import paho.mqtt.client as client
import threading
import re

intRe = re.compile('(?P<num>^\d+$)')

def onConnect(mqttc, obj, flags, rc):
    print('connected')
    print('rc: ', str(rc))
    mqttClient.subscribe('test', 0)

def onMessage(mqttc, obj, msg):
    print('topic: ', msg.topic)
    print('qos: ', msg.qos)
    print('msg: ', msg.payload)

    # ADD TO DATABASE

def onPub(mqttc, obj, mid):
    print('mid: ', str(mid))

mqttClient = client.Client()
mqttClient.on_connect = onConnect
mqttClient.on_message = onMessage
mqttClient.on_publish = onPub

mqttClient.connect('192.168.0.232', 1883, 60)

app = flask.Flask(__name__)

data = {
    'state' : 'N/A',
    'color' : 'N/A',
    'pir' : 'N/A'
}

@app.route('/')
def motionHome():
    ctx = {
        'data' : data
    }

    return flask.render_template('MotionDetector.html', **ctx)

@app.route('/setColor', methods=['GET', 'POST'])
def setColor():
    r = flask.request.values.get('rVal') 
    g = flask.request.values.get('gVal')
    b = flask.request.values.get('bVal')

    r = checkInt(r)
    g = checkInt(g)
    b = checkInt(b)

    if r is None:
        r = 0
    if g is None:
        g = 0
    if b is None:
        b = 0

    color = '{},{},{}'.format(r, g, b)

    mqttClient.publish('test/topic2', color, qos=0)

    return flask.redirect(flask.url_for('motionHome'))

def checkInt(string):
    ret = None

    match = intRe.search('{}'.format(string))
    if match is not None:
        ret = int(match.group('num'))

    return ret

def startServer():
    app.run(
        host='127.0.0.1',
        port=8080
    )

if __name__ == '__main__':
    comThread = threading.Thread(target=mqttClient.loop_forever)
    comThread.start()

    startServer()
    #flaskThread = threading.Thread(target=startServer)
    #flaskThread.start()

    #mqttClient.loop_forever()

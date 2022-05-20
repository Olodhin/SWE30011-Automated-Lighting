import flask
import paho.mqtt.client as client
import threading
import re

intRe = re.compile('(?P<num>^\d+$)')
msgRe = re.compile('{"state":"(?P<state>[a-zA-Z_]+)","pirOutput":"(?P<pirOutput>[a-zA-Z_]+)","color":"(?P<color>[0-9,]+)"}')

data = {
    'state' : 'N/A',
    'color' : 'N/A',
    'pir' : 'N/A'
}

def onConnect(mqttc, obj, flags, rc):
    print('connected')
    print('rc: ', str(rc))
    mqttClient.subscribe('v1/devices/me/telemetry', 0)

def onMessage(mqttc, obj, msg):
    #print('topic: ', msg.topic)
    #print('qos: ', msg.qos)
    #print('msg: ', msg.payload)

    match = msgRe.search(msg.payload.decode())
    #print(msg.payload.decode())
    if match is not None:
        data['state'] = match.group('state')
        data['color'] = match.group('color')
        data['pir'] = match.group('pirOutput')

    #print(data)

    # ADD TO DATABASE

def onPub(mqttc, obj, mid):
    print('mid: ', str(mid))

mqttClient = client.Client()
mqttClient.on_connect = onConnect
mqttClient.on_message = onMessage
mqttClient.on_publish = onPub

mqttClient.connect('127.0.0.1', 1883, 60)

app = flask.Flask(__name__)

@app.route('/')
def motionHome():
    ctx = {
        'data' : data
    }

    return flask.render_template('MotionDetector.html', **ctx)

def home():
    return flask.redirect(flask.url_for('motionHome'))

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

    #print('topic: {}\npubMsg: {}'.format('lighting/rgb', color))
    if r != 0 or g != 0 or b != 0:
        mqttClient.publish('lighting/rgb', color, qos=0)

    return home()

@app.route('/toggleOn', methods=['GET'])
def turnOn():
    print('on')
    mqttClient.publish('lighting/on', 'e', qos=0)

    return home()

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

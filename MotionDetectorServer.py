import flask
import re
from SharedData import SharedData

intPattern = '(?P<num>^\d+$)'
intRe = re.compile(intPattern)

shared = None

app = flask.Flask(__name__)

data = {
    'state' : 'N/A',
    'color' : 'N/A',
    'pir' : 'N/A'
}    

@app.route('/')
def index():
    ctx = {
        'data' : data
    }

    return flask.render_template('MotionDetector.html', **ctx)


@app.route('/setColor', methods=['GET', 'POST'])
def setColor():
    ctx = {
        'data' : data
    }

    r = flask.request.values.get('rVal')
    g = flask.request.values.get('gVal')
    b = flask.request.values.get('bVal')

    #print('rgb: {} {} {}'.format(r, g, b))

    if g is None:
        print('gNone')

    r = checkInt(r)
    g = checkInt(g)
    b = checkInt(b)

    if r is None:
        r = 0
    if g is None:
        g = 0
    if b is None:
        b = 0

    colors = '{},{},{}'.format(r, g, b)
    shared.setData('colors', colors)

    print('color: '+ colors)

    return flask.redirect(flask.url_for('index'))


def checkInt(string):
    ret = None
    
    match = intRe.search('{}'.format(string))
    if match is not None:
        ret = int(match.group('num'))

    return ret


def startServer(data, host='127.0.0.1', port=8080, debug=True):
    global shared
    shared = data
    app.run(
        host=host,
        port=port,
        debug=debug
    )

if __name__ == '__main__':
    startServer()



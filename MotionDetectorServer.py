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

    return flask.redirect(flask.url_for('index'))


def checkInt(string):
    ret = None
    
    match = intRe.search('{}'.format(string))
    if match is not None:
        ret = match.group('num')

    return ret


def startServer(host='127.0.0.1', port=8080, debug=True, data):
    global shared
    shared = data
    app.run(
        host=host,
        port=port,
        debug=debug
    )

if __name__ == '__main__':
    startServer()



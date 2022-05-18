import flask
import base64

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html', **dict())

@app.route('/api/test', methods=['POST'])
def apiTest():
    r = flask.request
    raw = r.data.decode()
    decoded = base64.b64decode(raw)
    #print(decoded)
    fo = open('fig-written.png', 'wb')
    #img = np.fromstring(r.data, np.uint8)
    fo.write(decoded)
    fo.close()


    data = 'hello world'
    response = {
        'message' : data
    }
    
    return flask.Response(
        response=data,
        status=200, 
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)

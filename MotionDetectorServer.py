import flask, re, pymysql
from SharedData import SharedData
from DBComs import DBComs

intPattern = '(?P<num>^\d+$)'
intRe = re.compile(intPattern)

shared = None
dbParams = None

app = flask.Flask(__name__)

data = {
    'state' : 'N/A',
    'color' : 'N/A',
    'pir' : 'N/A'
}    

@app.route('/')
def index():
    if dbParams is not None:        
        dbComs = pymysql.connect(
            host=dbParams['host'],
            user=dbParams['user'],
            password=dbParams['pwd'],
            database=dbParams['name'],
            cursorclass=pymysql.cursors.DictCursor
        ) or die("Failed to connect")
        cursor = dbComs.cursor()
        cmd = 'SELECT * FROM {} ORDER BY id DESC LIMIT 1'.format(
            dbParams['tableName'], 
        )
        cursor.execute(cmd)
        row = cursor.fetchone()
        print(row)
        data['state'] = row['state']
        data['pir'] = row['pirOutput']
        data['color'] = row['color']

    ctx = {
        'data' : data
    }
    print(ctx)

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


def startServer(data, db, host='127.0.0.1', port=8080, debug=True):
    global shared, dbParams
    dbParams = db

    shared = data
    app.run(
        host=host,
        port=port,
        debug=debug
    )

if __name__ == '__main__':
    startServer()



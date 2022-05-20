from MotionDetectorEdge import MotionDetectorEdge

serial = {
    'port' : '/dev/ttyS2',
    'baudrate' : 9600
}

db = {
    'host' : '127.0.0.1',
    'user' : 'pi',
    'pwd' : '',
    'name' : 'MotionLighting',
    'tableName' : 'MotionDetectorLog',
    'cols' : ['state', 'pirOutput', 'color']
}

flask = {
    'ip' : '127.0.0.1',
    'port' : 8080,
    'debug' : False
}

#mqtt = {
#    'user' : 'IOT_LIGHT_TOKEN',
#    'pwd' : '',
#    'host' : '192.168.56.1',
#    'port' : 1883,
#    'topic' : 'v1/devices/me/telemetry'
#}

mqtt = {
    #'user' : 'PIR',
    #'pwd' : '',
    'host' : '127.0.0.1',
    'port' : 1883,
    'pubTopic' : 'v1/devices/me/telemetry',
    'subTopics' : ['lighting/rgb', 'lighting/on']
}

mdDict = {
    'serial' : serial,
    'db' : db,
    'flask' : flask,
    'mqtt' : mqtt
}

edge = MotionDetectorEdge(**mdDict)
edge.run()

import json


def readSetting(fileName):
    try:
        file = open(fileName, 'r')
        data = file.read()
        values = json.loads(data)
        file.close()
        return values
    except:
        print("An exception occurred")


def writeSetting(fileName, data):
    try:
        file = open(fileName, 'w')
        file.write(json.dumps(data, sort_keys=True, indent=4))
        file.close()
    except:
        print("An exception occurred")

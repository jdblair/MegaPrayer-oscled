from bottle import Bottle, route, run, request, response, static_file
from datetime import datetime
import os
import json

app = Bottle()

@app.route('/', method=['GET'])
def set_time_view():
    """
    For simplicity's sake, have the root path just serve static/index.html
    """
    return send_static('index.html')


@app.route('/static/:filename')
def send_static(filename):
    """
    Mostly so that I can serve up jquery, otherwise I'd just return the
    index.html file directly here
    """
    pwd = os.path.dirname(os.path.realpath(__file__))
    return static_file(filename, os.path.join(pwd, 'static'))


@app.route('/set_time', method=['OPTIONS','POST'])
def set_time():

    if request.method == 'OPTIONS':
        return {}
    else:

        print("Received: {}".format(request.json))

        # If we can't convert to int there's no point continuing
        timestamp = int(request.json.get('timestamp'))

        # If given millis, convert to seconds
        if timestamp > 1500000000000:
            timestamp /= 1000

        # NOTE: THIS ACTUALLY SETS YOUR SYSTEM CLOCK
        os.system("date -s '@{}'".format(timestamp))

        return "Set time to {} (timezone-naive)".format(datetime.fromtimestamp(timestamp))

run(app, host='localhost', port=8080, debug=True)

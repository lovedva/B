<<<<<<< HEAD
from flask import Flask,request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Python Server run successful.  ---By 韩大狗♂'



if __name__ == '__main__':

try:
    # app.run(debug=True, port=88, host='0.0.0.0')
    http_serv= WSGIServer(("0.0.0.0",88),app)
    # handler_class=WebSocketHandler
    http_serv.serve_forever()
finally:
    RPi.GPIO.cleanup() 

=======
from flask import Flask,request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Python Server run successful.  ---By 韩大狗♂'



if __name__ == '__main__':

try:
    # app.run(debug=True, port=88, host='0.0.0.0')
    http_serv= WSGIServer(("0.0.0.0",88),app)
    # handler_class=WebSocketHandler
    http_serv.serve_forever()
finally:
    RPi.GPIO.cleanup() 

>>>>>>> 7798c2dc6080938b6265d50a0f1c36df11d3dd8c

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import RPi.GPIO
from flask import Flask,request
import cp
import time

app = Flask(__name__)

# a simple page that says hello
@app.route('/')
def hello():
    return 'Hello, World!'
    
app.register_blueprint(cp.bp)


if __name__ == '__main__':
    try:
        RPi.GPIO.cleanup() 
        # serv=WSGIServer(("0.0.0.0",88),app,handler_class=WebSocketHandler,processes=8)
        # serv.serve_forever()

        app.run(debug=True, port=88, host='0.0.0.0')  #processes=8

    finally:
        RPi.GPIO.cleanup() 




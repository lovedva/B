#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask
import cp

app = Flask(__name__)

# a simple page that says hello
@app.route('/')
def hello():
    return 'Hello, World!'

# from . import db
# db.init_app(app)

# from . import auth
# app.register_blueprint(auth.bp)

# from . import blog
# app.register_blueprint(blog.bp)
# app.add_url_rule('/', endpoint='index')

 
app.register_blueprint(cp.bp)

if __name__ == '__main__':
    app.run(debug=True, port=88, host='0.0.0.0')


from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Python Server run successful.  ---By 韩大狗♂'

if __name__ == '__main__':
    app.run(debug=True, port=88, host='0.0.0.0')
    

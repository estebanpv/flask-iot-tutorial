from flask import Flask
from blueprints import publisher

app = Flask(__name__)

app.register_blueprint(publisher, url_prefix='/publisher')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
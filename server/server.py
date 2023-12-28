from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello from Flask!'


@app.route('/health')
def health():
    return 'ok'


@app.route('/hello/<string>')
def hello(string):
    return 'Hello {}'.format(string)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
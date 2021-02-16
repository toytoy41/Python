# from wsgiref import simple_server
from flask import Flask

# def application(environ, start_response):
#     start_response('200 OK', [('Content-type', 'text/plain')])
#     return 'Hello, world'

app = Flask(__name__)

@app.route('/')
def index():
    name = "Hello World ???!!!"
    return name

    # return 'Hello  ????!!!'

## おまじない
if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == '__main__':
#     app.debug = True
#     app.run #(host='0.0.0.0', port=80)
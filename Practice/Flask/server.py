from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():

    lis = ["a1", "a2", "a3"]
    dic = {"name":"John", "age":24}
    bl = True

    return render_template('index.html', s=s, lis=lis, dic=dic, bl=bl)


    # return render_template('index.html')
    # return 'Hello'

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        res = request.args.get('get_value')
    elif request.method == 'POST':
        res = request.form['post_value']

    return res

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5001)
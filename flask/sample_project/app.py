from flask import Flask
app = Flask(__name__)

@app.route('/')

def hello_world():
    return 'Hello, World!!!!!'

@app.route('/page/<variable>')
def func(variable):
    return variable


if __name__ == "__main__":
    app.run(debug=True)
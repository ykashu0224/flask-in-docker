from flask import Flask, render_template, request
 
app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/form/', methods=['GET'])
def form():
    return render_template('form.html', title='Sample', lead='名前確認ページ')

@app.route('/form/', methods=['POST'])
def result():
	your_name = request.form['name']
	return render_template('result.html', result=your_name)

 
if __name__ == "__main__":
    app.run(debug=True)
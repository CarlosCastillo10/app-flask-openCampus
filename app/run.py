from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

if __name__ == '__main__':
    # app.run(host='0.0.0.0') # en una direccion en especifico
    app.run() # en el localhost (127.0.0.1)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/single_player.html')
def singleplayer():
    return render_template('single_player.html')

@app.route('/two_player.html')
def twoplayer():
    return render_template('two_player.html')

if __name__ == '__main__':
    app.run(debug = True)
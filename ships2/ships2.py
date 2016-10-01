from flask import Flask
from flask import render_template
from flask import request
import os
from game import Game

app = Flask(__name__)
g = Game()

@app.route('/')
def game_default():
    global g
    return render_template('game.html', game=g )

@app.route('/new_game')
def game_new():
    global g
    g = Game()
    return render_template('game.html', game=g )

@app.route('/step/<x>/<y>')
def game_step(x,y):
    g.moveOnField(int(x),int(y))
    return render_template('game.html', game=g)

@app.route('/flag/<x>/<y>')
def game_flag(x,y):
    g.toggleCellFlag(int(x),int(y))
    return render_template('game.html', game=g)

@app.route('/quit_server')
def quit_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Quitting server... <br/> <a href='/new_game'>restart</a>"
   
try:
    port = int(os.getenv("PORT"))
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=port) 
except:
    pass

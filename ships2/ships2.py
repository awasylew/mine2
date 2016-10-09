from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import jsonify
import os
from game import Game

app = Flask(__name__)
g = Game()

@app.route('/')
def game_default():
    global g
    return render_template('game.html', game=g )

api_prefix = '/api/v1'

@app.route( api_prefix + '/field')
def api_field_get():
    global g
    rsp = { 'width': g.width, 
           'height': g.height,
           'totalMines': g.totalMines,
           'status': g.status,
           'field': g.surfaceString() }
    return jsonify(rsp)

@app.route('/new_game')
def game_new():
    global g
    g = Game()
#    return render_template('game.html', game=g )
    return redirect( url_for('game_default'))

@app.route('/step/<x>/<y>')
def game_step(x,y):
    g.stepOnField(int(x),int(y))
#    return render_template('game.html', game=g)
    return redirect( url_for('game_default'))

@app.route('/flag/<x>/<y>')
def game_flag(x,y):
    g.toggleCellFlag(int(x),int(y))
#    return render_template('game.html', game=g)
    return redirect( url_for('game_default'))

@app.route('/quit_server')
def quit_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Quitting server... <br/> <a href='/new_game'>restart</a>"
   
# try:
#port = int(os.getenv("PORT"))
if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=port) 
    app.run( debug=True )
#except:
#    pass

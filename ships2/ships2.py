from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import jsonify
import os
from game import Game
from gameset import GameSet
 
app = Flask(__name__) 
g = Game()
gameset = GameSet()
api_prefix = '/api/v1'

@app.route('/')
def game_default():
    global g
    return render_template('game.html', game=g )

@app.route('/ab/games/<gameID>')
def ab_games_default( gameID ):
    game = gameset.getGameByID( gameID )
    game_ids = gameset.getGameList()
    return render_template('game.html', game=game, game_url=url_for('ab_games_default', gameID=gameID), 
                           game_ids=game_ids, games_url='/ab/games' )

@app.route( api_prefix + '/field')
def api_show_field():
    global g
    rsp = { 'width': g.width, 
           'height': g.height,
           'totalMines': g.totalMines,
           'minesLeft': g.getMinesLeft(),
           'status': g.status,
           'field': g.fieldAsString(True) }
    return jsonify(rsp), 200                                        # dodac naglowki

@app.route('/new_game')
def game_new():
    global g
    g = Game()
    return redirect( url_for('game_default'))

@app.route('/ab/games/new')
def ab_new_game():
    id = gameset.startNewGame()
    return 'id = ' + str(id)

@app.route('/ab/games')
def ab_games():
    rsp = {'game_ids': gameset.getGameList()}
    print( rsp )
    return jsonify( rsp )

@app.route('/step/<x>/<y>')
def game_step(x,y):
    g.stepOnField(int(x),int(y)) # brak obslugi bledow
    return redirect( url_for('game_default'))

@app.route('/ab/games/<gameID>/step/<x>/<y>')
def ab_game_step( gameID, x, y ):
    game = gameset.getGameByID( gameID )
    game.stepOnField(int(x),int(y)) # brak obslugi bledow
    return redirect( url_for('ab_games_default', gameID=gameID ))

@app.route( api_prefix + '/step', methods=['GET', 'POST'] )                                  # powinno byc tylko POST
def api_step():
    try:                                                            # nie mozna tego kodu ladnie uwspolnic z flag?
        x = int( request.argameset.get( 'x' ))
        y = int( request.argameset.get( 'y' ))
        if not 0 <= x < g.width or not 0 <= y < g.height:
            raise 
    except:
        return 'Expecting params 0,0 <= x,y < width,height', 400        # dodac naglowki
    g.stepOnField( x, y )
    return api_show_field()
    
@app.route('/flag/<x>/<y>/<state>')
def game_flag(x,y,state):
    g.setFlag( int(x), int(y), state.upper()=='TRUE' )  # brak obslugi bledow
    return redirect( url_for('game_default'))

@app.route( api_prefix + '/set_flag', methods=['GET', 'POST'] )                              # powinno byc tylko POST
def api_set_flag():
    try:
        x = int( request.argameset.get( 'x' ))
        y = int( request.argameset.get( 'y' ))
        t = request.argameset.get( 'state' ).upper()
        if not 0 <= x < g.width or not 0 <= y < g.height or not t in ['TRUE', 'FALSE']:
            raise 
    except:
        return 'Expecting params 0,0 <= x,y < width,height, state==false|true', 400
    g.setFlag( x, y, t=='TRUE' )
    return api_show_field()
    
@app.route('/ab/games/<gameID>/flag/<x>/<y>/<state>')
def ab_game_flag( gameID, x, y, state ):
    game = gameset.getGameByID( gameID )
    game.setFlag( int(x), int(y), state.upper()=='TRUE' ) # brak obslugi bledow
    return redirect( url_for('ab_games_default', gameID=gameID ))

@app.route('/quit_server')
def quit_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Quitting server..."
   
if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    app.run(host='0.0.0.0', port=port) 

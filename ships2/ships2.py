from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import jsonify
import os
# from game import Game
from gameset import GameSet
 
app = Flask(__name__) 
gameset = GameSet()
apiPrefix = '/api/v1'
apiPrefixBare = '/api'
webPrefix = '/ab'

@app.route( '/' )
@app.route( webPrefix )
def webRoot():
    return redirect( url_for('webGamesDefault'))

@app.route( apiPrefix )
@app.route( apiPrefixBare )
def apiRoot():
    return render_template( 'api.html' )

@app.route( webPrefix + '/games')                      # tylko lista gier
@app.route( webPrefix + '/games/<gameID>')             # biezaca gra + lista gier
def webGamesDefault( gameID=None ):
    if gameID != None:
        currentGame = gameset.getGameByID( gameID )
    else:
        currentGame = None
    game_ids = gameset.getGameList()
    return render_template('game.html', game=currentGame, game_url=url_for('webGamesDefault', gameID=gameID), 
                           game_ids=game_ids, games_url=webPrefix+'/games' )                                   # snake_case -> cameCase

@app.route( apiPrefix + '/games')
def apiGames():
    rsp = {'game_ids': gameset.getGameList()}
    print( rsp )
    return jsonify( rsp )

@app.route( apiPrefix + '/games2')
def apiGames2():
#    rsp = {'games': list(map(lambda gameID: apiPrefix+'/games/'+gameID, gameset.getGameList())) }
    rsp = {'games': list(map(lambda gameID: url_for('apiShowField', gameID=gameID, _external=True), gameset.getGameList())) }
    print( rsp )
    return jsonify( rsp )

@app.route( apiPrefix + '/games/<gameID>')
def apiShowField( gameID ):                                         # nazwa?
    game = gameset.getGameByID( gameID )                            # obsluga bledu id
    rsp = { 'width': game.width, 
           'height': game.height,
           'totalMines': game.totalMines,
           'minesLeft': game.getMinesLeft(),
           'status': game.status,
           'field': game.fieldAsString(True) }
    return jsonify(rsp)                                             # dodac naglowki

@app.route( webPrefix + '/games/new' )                                         # w wersji API POST zamiast /new 
def webNewGame():
    gameID = gameset.startNewGame()
#    return 'id = ' + str(id)
    return redirect( url_for('webGamesDefault', gameID=gameID ))

@app.route( apiPrefix+'/games', methods=['POST'])
def apiNewGame():
    gameID = gameset.startNewGame()
    return 'id = ' + str(gameID)

@app.route( webPrefix + '/<gameID>/flag/<x>/<y>/<state>' )
def webFlag( gameID, x, y, state ):
    game = gameset.getGameByID( gameID )
    game.setFlag( int(x), int(y), state.upper()=='TRUE' )               # brak obslugi bledow
    return redirect( url_for('webGamesDefault', gameID=gameID ))

@app.route( apiPrefix + '/games/<gameID>/flag', methods=['GET', 'POST'])                    # powinno byc tylko POST
def apiFlag( gameID ):
    try:                                                            # nie mozna tego kodu ladnie uwspolnic z flag?
        game = gameset.getGameByID( gameID )            # obsluga bledu id
        x = int( request.args.get( 'x' ))
        y = int( request.args.get( 'y' ))
        s = request.args.get( 'state' ).upper()
        if not 0 <= x < game.width or not 0 <= y < game.height or not s in ['TRUE', 'FALSE']:
            raise 
    except:
        return 'Expecting params 0,0 <= x,y < width,height, state==false|true', 400        # dodac naglowki
    game.setFlag( x, y, s=='TRUE' )
    return apiShowField( gameID )
    
@app.route( webPrefix + '/games/<gameID>/step/<x>/<y>' )
def webStep( gameID, x, y ):
    game = gameset.getGameByID( gameID )
    game.stepOnField(int(x),int(y))                                     # brak obslugi bledow
    return redirect( url_for('webGamesDefault', gameID=gameID ))

@app.route( apiPrefix + '/games/<gameID>/step', methods=['GET', 'POST'] )                   # powinno byc tylko POST
def apiStep( gameID ):
    try:                                                            # nie mozna tego kodu ladnie uwspolnic z flag?
        game = gameset.getGameByID( gameID )            # obsluga bledu id
        x = int( request.args.get( 'x' ))
        y = int( request.args.get( 'y' ))
        if not 0 <= x < game.width or not 0 <= y < game.height:
            raise 
    except:
        return 'Expecting params 0,0 <= x,y < width,height', 400        # dodac naglowki
    game.stepOnField( x, y )
    return apiShowField( gameID )

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

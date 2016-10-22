from game import Game
from random import random 

class GameSet(object):
    
    def __init__(self):
        self.games = dict()
    
    def startNewGame(self): # zwraca id gry 
        id = int( random() * 9000 + 1000)
        while( id in self.games ):
            id = int( random() * 9000 + 1000)
        new_game = Game()
        self.games[str(id)] = new_game
        return id
        
    
    def getGameList(self): # zwraca listê id gier
        return list( self.games.keys())
    
    def getGameByID(self,id):  # zwraca obiekt gry
        return self.games[id]

    def deleteGame(self,id):  # usuwa gr
        pass
    
    # KIEDY UTRWALAC GRE w BAZIE DANYCH???
    
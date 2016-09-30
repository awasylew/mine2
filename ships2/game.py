import random

class Field(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def cells(self):
        for x in range(self.height):
            for y in range(self.width):
                yield x,y
                
    def empty(self):
        self.field=dict()
        for xy in self.cells():
                self.field[xy]='e'
        
    def show(self, transform):
        print('   ', end='')
        for x in range(self.width):
            print( "%s  " % chr( x + ord('a')), end='')
        print()
        for y in range(self.height):
            print( "%2d " % (y+1), end='' )
            for x in range(self.width):
                print(transform(self.field[(x,y)]), ' ', end='')
            print()
        print()
    
    def reveal(self):
        self.show( lambda x: x )

    def display(self):
        self.show( lambda x: '*' if x in ['e', 'M'] else 'F' if x[0]=='F' else x )
        
    def layMines(self, numMines):
        for m in range(numMines):
            while True:
                xy = int(random.random()*self.width), int(random.random()*self.height)
                if self.field[xy] == 'M':
                    continue
                self.field[xy] = 'M'
                break

    def neighbours(self,xy):
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx==0 and dy==0:
                    continue
                x1,y1 = xy[0]+dx, xy[1]+dy
                if 0 <= x1 <= self.width-1 and 0 <= y1 <= self.height-1:
                    yield x1,y1
        
    def minesAround(self,xy):
        count = 0
        for xy1 in self.neighbours(xy):
            if self.field[xy1] in ['M', 'FM']:
                count += 1 
        return count
        
    def expose(self):
        again=True
        while again:
            again=False
            for xy in self.cells():
                if self.field[xy] == '0':
                    again=True
                    self.field[xy] = '.'
                    for xy1 in self.neighbours(xy):
                        if self.field[xy1] == 'e':
                            self.field[xy1] = str(self.minesAround(xy1))
        
    def step(self,xy):
        if self.field[xy] == 'M':
#            self.field[xy] = 'B'
            return
        self.field[xy] = str(self.minesAround(xy))
        self.expose()
        
    def flag(self,xy):
        if self.field[xy][0] == 'F':
            self.field[xy] = self.field[xy][1:]
        else:
            self.field[xy] = 'F' + self.field[xy]
            
    def numFlags(self):
        return list(self.field.values()).count( 'Fe' ) + list(self.field.values()).count( 'FM' )
        

class Game(object):  #zbyt krotka nazwa? ShipsGame ShipsPlay GameOfShips
    """
    Obiekt utrzymujacy stan pojedynczej rozgrywki i wykonujacy dzialania w czasie rozgrywki.
    Gra rozpoczyna sie od wszystkich zakrytych pol. Na niektorych polach znajduja sie miny. Pola mozna odkrywac lub flagowac.
    Gra toczy sie do momentu oznaczenia wszystkich min i odkrycia pozostalych pol lub do wejscia na mine.
    """
    
    def __init__(self):  # brakuje parametryzacji (trudno�� albo wielko�� pola i liczba min)
        """
        Rozpoczyna now� rozgrywk� od wszystkich zakrytych p�l i roz�o�onych min.
        """
        self.field = Field(10,10)
        self.field.empty() # to pewnie powinno by� cz�ci� konstruktora
        self.totalMines = 10 # to mo�e te� powinien by� konstruktor
        self.field.layMines(self.totalMines) # mo�e to te� powinien by� konstruktor
        self.status = 'ready'  # mo�e jaki� getter? mo�e ENUM?

    """
    metoda zbyt specyficzna czy diagnostyczna?
    def display(self):
        print( 'status: ', self.status )
        print( 'mines left: ', self.minesLeft )
        self.field.reveal()
        self.field.display()
    """
    
    def step(self,x,y):  #zbyt kr�tka nazwa? zbyt niedok�adna? zbyt niejednoznaczna?
        """
        Ods�ania pole jak przy wst�pieniu na nie.
        Je�li na polu znajduje si� mina, gra si� ko�czy przegran�.
        Je�li ods�oni�to wszystko... gra si� ko�czy wygran�.  --- dorobi�
        Je�li mo�na ods�oni� s�siednie pola, s� one r�wnie� ods�aniane - rekurencyjnie.
        Je�li gra jest zako�czona, metoda nie ma skutk�w.
        """
        
        if self.status=='game over':
            print('game over, not stepping in')
            return
        if self.field.field[ (x,y) ] == 'M':
#            print('boom!!!')    # diagnostyka?
#            self.display()
            self.field.field[(x,y)] = 'B'
            self.status='game over'
#            return
        else:
            self.field.step( (x,y) )
#        self.display()

    def flag(self,x,y):    #zbyt kr�tka nazwa? zbyt niejednoznaczna?
        """
        Zmienia stan oznaczenia pola flag� na przeciwny.
        Je�li gra jest zako�czona, metoda nie ma skutk�w.    --- nie dzia�a tak obecnie, potrzebne?
        """
        self.field.flag( (x,y) )
#        self.display()
        
    def minesLeft(self):    #nazwa nieprecyzyjna  getNumMinesLeft?
        """
        Pobiera liczb� nieoznaczonych min - wynikaj�c� z wype�nienia planszy i oznacze� flagami. 
        Nie bada dopasowania flag do min.
        Je�li flag jest wi�cej ni� min, zwraca zero. 
        """
        fl = self.field.numFlags()
        return max( self.totalMines - fl, 0 )

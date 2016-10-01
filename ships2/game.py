import random

# class Field(object):
class Game(object):  #zbyt krotka nazwa? ShipsGame ShipsPlay GameOfShips
    """
    Obiekt utrzymujacy stan pojedynczej rozgrywki i prowadzacy rozgrywke.
    Gra rozpoczyna sie od wszystkich zakrytych pol. Na niektorych polach znajduja sie miny. Pola mozna odkrywac lub flagowac.
    Gra toczy sie do momentu oznaczenia wszystkich min i odkrycia pozostalych pol lub do wejscia na mine.
    
    Wartosci pol:
    'e' puste
    'M' mina
    'Fe' flaga + puste
    'FM' flaga + mina
    '.' odsloniete, 0 sasiadow
    '1'-'8' odsloniete, n sasiadow
    'B' mina wybuchala
    
    Statusy:
    'ready' poczatek gry, brak odslonietych pol
    'started' trwa rozgrywka
    'game over' koniec gry # zmienic na wygrana i przegrana
    """
    
    # brakuje wykrywania zakonczenia gry sukcesem
    # brakuje statusow oznaczajacych koniec gry sukcesem/porazka
    # brakuje gettera do statusu
    
    def __init__(self, setWidth=10, setHeight=10, setMines=15):  # brakuje parametryzacji (trudnosc albo wielkosc pola i liczba min)
        """
        Rozpoczyna nowa rozgrywke od wszystkich zakrytych pol i rozlozonych min.
        """
        self.width = setWidth
        self.height = setHeight
        self.totalMines = setMines 
        self.status = 'ready'  
        
    def Xcells(self):
        for x in range(self.height):
            for y in range(self.width):
                yield x,y
                
    def clearField(self):
        """
        Poczatkowe wypelnienie wszystkich pol na pusto.
        """
        self.field = dict()
        for xy in self.Xcells():
                self.field[xy] = 'e'
        
    """
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
    """
        
    def XlayMines(self, numMines, startX=None, startY=None):
        for m in range(numMines):
            while True:
                xy = int(random.random()*self.width), int(random.random()*self.height)
                print(m, xy, self.field[xy])
                if xy == (startX, startY):
                    continue
                if self.field[xy] in ['M', 'FM']:
                    continue
                if self.field[xy] == 'e':
                    self.field[xy] = 'M'
                else:
                    self.field[xy] = 'FM' 
                break

    def Xneighbours(self,xy):
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx==0 and dy==0:
                    continue
                x1,y1 = xy[0]+dx, xy[1]+dy
                if 0 <= x1 <= self.width-1 and 0 <= y1 <= self.height-1:
                    yield x1,y1
        
    def XminesAround(self,xy):
        count = 0
        for xy1 in self.Xneighbours(xy):
            if self.field[xy1] in ['M', 'FM']:
                count += 1 
        return count
        
    def Xexpose(self):
        again=True
        while again:
            again=False
            for xy in self.Xcells():
                if self.field[xy] == '0':
                    again=True
                    self.field[xy] = '.'
                    for xy1 in self.Xneighbours(xy):
                        if self.field[xy1] == 'e':
                            self.field[xy1] = str(self.XminesAround(xy1))
        
    def Xstep(self,xy):
        if self.field[xy] == 'M':
#            self.field[xy] = 'B'
            return
        self.field[xy] = str(self.XminesAround(xy))
        self.Xexpose()
        
    def Xflag(self,xy):
        if self.field[xy][0] == 'F':
            self.field[xy] = self.field[xy][1:]
        else:
            self.field[xy] = 'F' + self.field[xy]
            
    def XnumFlags(self):
        return list(self.field.values()).count( 'Fe' ) + list(self.field.values()).count( 'FM' )
        

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
        Odslania pole jak przy wstapieniu na nie.
        Jesli na polu znajduje sie mina, gra sie konczy przegrana.
        Jesli odslonieto wszystko... gra sie konczy wygrana.  --- dorobic
        Jesli mozna odslonic sasiednie pola, sa one rowwniez odslaniane - rekurencyjnie.
        Jesli gra jest zakonczona, metoda nie ma skutkow.
        """
        
        if self.status=='game over':
            print('game over, not stepping in')
            return
        if self.status == 'ready':
            self.status = 'started'
            self.XlayMines( self.totalMines, x, y )
        if self.field[ (x,y) ] == 'M':
#            print('boom!!!')    # diagnostyka?
#            self.display()
            self.field[(x,y)] = 'B'
            self.status='game over'
#            return
        else:
            self.Xstep( (x,y) )
#        self.display()

    def flag(self,x,y):    #zbyt krotka nazwa? zbyt niejednoznaczna?
        """
        Zmienia stan oznaczenia pola flaga na przeciwny.
        Jeeli gra jest zakonczona, metoda nie ma skutkow.    --- nie dziala tak obecnie, potrzebne?
        """
        self.Xflag( (x,y) )
#        self.display()
        
    def minesLeft(self):    #nazwa nieprecyzyjna  getNumMinesLeft?
        """
        Pobiera liczbe nieoznaczonych min - wynikajaca z wypelnienia planszy i oznaczen flagami. 
        Nie bada dopasowania flag do min.
        Jeeli flag jest wiecej niz min, zwraca zero. 
        """
        fl = self.XnumFlags()
        return max( self.totalMines - fl, 0 )

import random

class Game(object):  
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
    'success' koniec gry - wygrana
    'fail' koniec gry - przegrana
    """
    
    # brakuje gettera do statusu?
    # ENUMy zamiast tekstow?
    
    def __init__(self, setWidth=6, setHeight=6, setMines=5):
        """
        Rozpoczyna nowa rozgrywke od wszystkich zakrytych pol i rozlozonych min.
        """
        self.width = setWidth
        self.height = setHeight
        self.totalMines = setMines 
        self.status = 'ready'  
        self.clearField()
        
    def surfaceString(self):
        """
        Zwraca cale pole jako jeden napis wierszami z gory na dol. Wiersze oddzielone '/'.
        Wiersze od lewej do prawej. Pola oddzielone '&'.
        Przyklad 3x3: 'e&e&e/e&e&e/e&e&e'
        Pola odsloniete '.', 'B', '1'-'9' sa pokazywane bez zmian.
        Pola zasloniete ('e' i 'M') sa pokazywane jako 'X'.
         
        """
        result = ''
        for y in range(self.width):
            row = ''
            for x in range(self.height):
                f = self.field[ x,y ]
                if f in [ '.', '1', '2', '3', '4', '5', '6', '7', '8', 'B']:
                    fld = f
                elif f in [ 'Fe', 'FM' ]:
                    if self.status == 'fail':
                        fld = f
                    else:
                        fld = 'F' 
                elif f == 'M':
                    if self.status == 'fail':
                        fld = f
                    else:
                        fld = 'X' 
                else:  # 'e'
                    fld = 'X'
                if row != '':
                    row += '&'
                row += fld 
            if result != '':
                result += '/'
            result += row
        return result
    
    def allCells(self):
        """
        Funkcja pomocnicza - generuje oniesienia do wszystkich elementow planszy
        """
        for x in range(self.height):
            for y in range(self.width):
                yield x,y
                
    def clearField(self):
        """
        Poczatkowe wypelnienie wszystkich pol na pusto.
        """
        self.field = dict()
        for xy in self.allCells():
                self.field[xy] = 'e'
        
    def layMines(self, startX=None, startY=None):
        """
        Rozklada miny na planszy unikajac wskazanego pola.
        """
        for m in range(self.totalMines):
            while True:
                xy = int(random.random()*self.width), int(random.random()*self.height)
                if xy == (startX, startY):
                    continue
                if self.field[xy] in ['M', 'FM']:
                    continue
                break
            if self.field[xy] == 'e':
                self.field[xy] = 'M'
            else:
                self.field[xy] = 'FM' 

    def neighbourCells(self,xy):
        """
        Generuje wspolrzedne wszystkich pol otaczajacych dane pole - sprawdzajac czy nie wychodza poza plansze.
        """
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx==0 and dy==0:
                    continue
                x1,y1 = xy[0]+dx, xy[1]+dy
                if 0 <= x1 <= self.width-1 and 0 <= y1 <= self.height-1:
                    yield x1,y1
        
    def numNeighbourMines(self,xy):
        """
        Funkcja wyznacza liczbe min na planszy dookola danego pola.
        """
        count = 0
        for xy1 in self.neighbourCells(xy):
            if self.field[xy1] in ['M', 'FM']:
                count += 1 
        return count
        
    def exploreSafeFields(self):
        """
        Funkcja automatycznie odslania wszystkie pola sasiadujace z nowoodslonietymi polami wokol ktorych nie ma min.
        Odslanianie jest kontynuowane rekurencyjnie.
        """
        again=True
        while again:
            again=False
            for xy in self.allCells():
                if self.field[xy] == '0':
                    again=True
                    self.field[xy] = '.'
                    for xy1 in self.neighbourCells(xy):
                        if self.field[xy1] in ['e', 'Fe']:
                            self.field[xy1] = str(self.numNeighbourMines(xy1))
        
    def checkSuccess(self):
        """
        Funkcja sprawdza czy spelniony jest warunek zwyciestwa i ew. ustawia status.
        """ 
        if list(self.field.values()).count( 'Fe' ) == 0 and \
           list(self.field.values()).count( 'e' ) == 0 and \
           list(self.field.values()).count( 'M' ) == 0:
            self.status = 'success'
    
    def stepOnField(self,x,y):  #zbyt krotka nazwa? zbyt niedokladna? zbyt niejednoznaczna?
        """
        Odslania pole przy wstapieniu na nie.
        Jesli na polu znajduje sie mina, gra sie konczy przegrana.
        Jesli odslonieto wszystko... gra sie konczy wygrana.  --- dorobic
        Jesli mozna odslonic sasiednie pola, sa one rowniez odslaniane - rekurencyjnie.
        Jesli gra jest zakonczona, metoda nie ma skutkow.
        """
        if self.status in ['fail', 'success']:
            return
        xy = x,y
        if self.status == 'ready':
            self.status = 'started'
            self.layMines( x, y )
        if self.field[xy] == 'M':
            self.field[xy] = 'B'
            self.status = 'fail'   
        else:
            self.field[xy] = str(self.numNeighbourMines(xy))
            self.exploreSafeFields()
        # print(list(self.field.values()).count( 'Fe' ) , list(self.field.values()).count( 'e' ) )
        self.checkSuccess()

    def toggleCellFlag(self,x,y):    
        """
        Zmienia stan oznaczenia pola flaga na przeciwny.
        Jeeli gra jest zakonczona, metoda nie ma skutkow.    --- nie dziala tak obecnie, potrzebne?
        """
        xy = x,y
        if self.field[xy][0] == 'F':
            self.field[xy] = self.field[xy][1:]
        else:
            self.field[xy] = 'F' + self.field[xy]
        self.checkSuccess()
        
    def getMinesLeft(self):
        """
        Pobiera liczbe nieoznaczonych min - wynikajaca z wypelnienia planszy i oznaczen flagami. 
        Nie bada dopasowania flag do min - jesli gracz zle stawia flagi, to licznik i tak się zmniejsza.
        Jesli flag jest wiecej niz min, zwraca zero. 
        """
        fl = list(self.field.values()).count( 'Fe' ) + list(self.field.values()).count( 'FM' )
        return max( self.totalMines - fl, 0 )

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
        
    def display(self):
        print( 'status: ', self.status )
        print( 'mines left: ', self.minesLeft )
        self.field.reveal()
        self.field.display()
    """

class GameSet(object):
    
    def startNewGame(self): # zwraca id gry
        pass
    
    def getGameList(self): # zwraca listę id gier
        pass
    
    def getGameByID(self,id):  # zwraca obiekt gry
        pass

    def deleteGame(self,id):  # usuwa gr
        pass
    
    # KIEDY UTRWALAC GRE w BAZIE DANYCH???
    
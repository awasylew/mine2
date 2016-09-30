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
        

class Game(object):  #zbyt krótka nazwa? ShipsGame ShipsPlay GameOfShips
    """
    Obiekt utrzymuj¹cy stan pojedynczej rozgrywki i wykonuj¹cy dzia³ania w czasie rozgrywki.
    Gra rozpoczyna siê od wszystkich zakrytych pól. Na niektórych polach znajduj¹ siê miny. Pola mo¿na odkrywaæ lub flagowaæ.
    Gra toczy siê do momentu oznaczenia wszystkich min i odkrycia pozosta³ych pól lub do wejœcia na minê.
    """
    def __init__(self):  # brakuje parametryzacji (trudnoœæ albo wielkoœæ pola i liczba min)
        """
        Rozpoczyna now¹ rozgrywkê od wszystkich zakrytych pól i roz³o¿onych min.
        """
        self.field = Field(10,10)
        self.field.empty() # to pewnie powinno byæ czêœci¹ konstruktora
        self.totalMines = 10 # to mo¿e te¿ powinien byæ konstruktor
        self.field.layMines(self.totalMines) # mo¿e to te¿ powinien byæ konstruktor
        self.status = 'ready'  # mo¿e jakiœ getter? mo¿e ENUM?

    """
    metoda zbyt specyficzna czy diagnostyczna?
    def display(self):
        print( 'status: ', self.status )
        print( 'mines left: ', self.minesLeft )
        self.field.reveal()
        self.field.display()
    """
    
    def step(self,x,y):  #zbyt krótka nazwa? zbyt niedok³adna? zbyt niejednoznaczna?
        """
        Ods³ania pole jak przy wst¹pieniu na nie.
        Jeœli na polu znajduje siê mina, gra siê koñczy przegran¹.
        Jeœli ods³oniêto wszystko... gra siê koñczy wygran¹.  --- dorobiæ
        Jeœli mo¿na ods³oniæ s¹siednie pola, s¹ one równie¿ ods³aniane - rekurencyjnie.
        Jeœli gra jest zakoñczona, metoda nie ma skutków.
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
        self.display()

    def flag(self,x,y):    #zbyt krótka nazwa? zbyt niejednoznaczna?
        """
        Zmienia stan oznaczenia pola flag¹ na przeciwny.
        Jeœli gra jest zakoñczona, metoda nie ma skutków.    --- nie dzia³a tak obecnie, potrzebne?
        """
        self.field.flag( (x,y) )
        self.display()
        
    def minesLeft(self):    #nazwa nieprecyzyjna  getNumMinesLeft?
        """
        Pobiera liczbê nieoznaczonych min - wynikaj¹c¹ z wype³nienia planszy i oznaczeñ flagami. 
        Nie bada dopasowania flag do min.
        Jeœli flag jest wiêcej ni¿ min, zwraca zero. 
        """
        fl = self.field.numFlags()
        return max( self.totalMines - fl, 0 )

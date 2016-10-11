# ships2

Moja zabawa w aplikację chmurową. 
Nie będzie rozwijana do pełnej funkcjonalności - tylko tyle ile będzie mi potrzebne do testów, na jakie akurat nabiorę ochoty.

# archeytypy na podstawie TMF

## kolekcje zasobów
*kolekcje* składają się oddzielnych *zasobów*

	GET {root}/games
	POST {root}/games     ??? czy w taki sposób
	DELETE {root}/games      ??? wyczyszczenie? wyłączenie serwera?

## zasoby
każdy _zasób_ ma pola prosta zarządzane przez HTTP oraz podobiekty - _podzasoby_

	GET {root}/games/3654
	DELETE {root}/games/3654      ??? czy potrzeba

## działania
czasowniki, które nie mieszczą się w podejściu zasobowym
w tej grupie potrzebne stosowne wejście i wyjście

	{root}/games/3654/set_flag?x=2&y=3
	{root}/games/3654/reset_flag?x=2&y=3
	{root}/games/3654/step?x=2&y=3

# zapiski, zadania z RESTful - UPORZĄDKOWAĆ
ścieżka zdrowia – OPCJONALNIE (zdecydować czy robić czy tylko się dowiedzieć)

* GET/POST/PATH/DELETE – zapytania i odpowiedzi
* HTTPS
* OAuth2
* wyniki/kody błędów
* paging
* format wyniku JSON/XML
* WADL, Swagger/OpenAPI

uproszczenie modelu
definicje pola
		flaga – odczyt
		flaga/akcja – ustawienie (idempotentne, a nie toggle)
		pole – odczyt 
		pole/akcja – odkrycie

		pole – odczyt: zakryte/flaga/liczba/puste
		pole/akcja – flaga+/flaga-/wstąpienie

http://example.com/api/v1/games/739/       

GET field?x=3&y=4        - jedno zapytanie, wynik zakryte/flaga/liczba/puste/(mina)/(mina-bez-flagi)
{ ‘mine’: ‘false’; ‘flag’:’false’; ‘count’:’3’; ‘exposed’:’true’ }
‘status’:’3’ / ‘status’:’hidden’
POST field?x=3&y=4&action=step/set-flag/reset-flag      - jedno ustawienie bez parametrów


GET field

POST field/step?x=3&y=4

POST field/flag?x=3&y=4 

POST field/unflag?x=3&y=4


POST/PATCH field?x=3&y=4     - jedno ustawienie, parametry w treści 
{ ‘flag’:’true’ } / { ‘flag’:’false’ } / { ‘exposed’:’true’ }

GET games    		# lista gier (opisy i identyfikatory)
ew. ?range=5-10
POST games		# nowa gra; jakieś określenie wielkości?
GET games/739     	# stan gry (status, mines-left, szerokość, wysokość, całe pole) 
DELETE games/739	# usunięcie całej gry
POST/PATCH games/739/flag?x=3&y=4		# wykonanie akcji na grze (flag|unflag|step)


# ships2

Moja zabawa w aplikację chmurową. 
Nie będzie rozwijana do pełnej funkcjonalności - tylko tyle ile będzie mi potrzebne do testów, na jakie akurat nabiorę ochoty.


# zapiski, zadania z RESTful - UPORZĄDKOWAĆ
ścieżka zdrowia – OPCJONALNIE (zdecydować czy robić czy tylko się dowiedzieć)

GET/POST/PATH/DELETE – zapytania i odpowiedzi

HTTPS

OAuth2

wyniki/kody błędów

paging

format wyniku JSON/XML

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


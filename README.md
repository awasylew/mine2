# ships2

Moja zabawa w aplikację chmurową. 
Nie będzie rozwijana do pełnej funkcjonalności - tylko tyle ile będzie mi potrzebne do testów, na jakie akurat nabiorę ochoty.

# API

## root

	.../api/v1/...

## kolekcje zasobów
*kolekcje* składają się oddzielnych *zasobów*

	GET .../games
	POST .../games     ??? czy w taki sposób
	DELETE .../games      ??? wyczyszczenie? wyłączenie serwera?

## zasoby
każdy _zasób_ ma pola prosta zarządzane przez HTTP oraz podobiekty - _podzasoby_

	GET .../games/3654
	DELETE .../games/3654      ??? czy potrzeba

## działania
czasowniki, które nie mieszczą się w podejściu zasobowym
w tej grupie potrzebne stosowne wejście i wyjście

	[done] POST .../games/3654/set_flag?x=2&y=3&state=true
	[done] POST .../games/3654/set_flag?x=0&y=2&state=false
	[done] POST .../games/3654/step?x=2&y=3

# zapiski, zadania z RESTful - UPORZĄDKOWAĆ
ścieżka zdrowia – OPCJONALNIE (zdecydować czy robić czy tylko się dowiedzieć)

* HTTPS
* OAuth2
* wyniki/kody błędów
* paging
* format wyniku JSON/XML
* WADL, Swagger/OpenAPI

class Nodo:
    
    __slots__ = '_vuelo', '_anterior', '_siguiente'

    def __init__(self, vuelo, anterior, siguiente):
        self._vuelo = vuelo  
        self._anterior = anterior         
        self._siguiente = siguiente   
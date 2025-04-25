from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import create_engine
from database import *

# Definir el Enum de los estados de vuelo
class EstadoVuelo(PyEnum):
    EMERGENCIA = "Emergencia"
    PROGRAMADO = "Programado"
    ATRASADO = "Atrasado"

# Definir el modelo de vuelo
class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    estado = Column(Enum(EstadoVuelo))
    hora = Column(DateTime, default=datetime.utcnow)
    origen = Column(String)
    destino = Column(String)

    # Puedes agregar más relaciones o métodos si es necesario

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Dependencia para obtener sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class _ListaVuelos:
    """A base class providing a doubly linked list representation."""

    class _Node:
        """Lightweight, nonpublic class for storing a doubly linked node."""
        __slots__ = '_vuelo', '_anterior', '_siguiente'  # Memory optimization

        def __init__(self, vuelo, anterior, siguiente):
            self._vuelo = vuelo  # Reference to user's element
            self._anterior = anterior         # Reference to previous node
            self._siguiente = siguiente         # Reference to next node

    def __init__(self):
        """Create an empty list with sentinel nodes."""
        self._header = self._Node(None, None, None)  # Dummy header
        self._trailer = self._Node(None, None, None) # Dummy trailer
        self._header._siguiente = self._trailer  # Header points to trailer
        self._trailer._anterior = self._header  # Trailer points to header
        self._size = 0  # Number of elements
        self.db_session = SessionLocal()  # Start a session for database operations

    def __len__(self):
        """Devuelve el número de elementos en la lista (O(1))."""
        return self._size

    def is_empty(self):
        """Devuelve Verdadero si la lista está vacía (O(1))."""
        return self._size == 0

    def _insert_between(self, e, predecessor, successor):
        """

        Añade el elemento e entre dos nodos existentes y devuelve un nuevo nodo (O(1)).

        Argumentos:
        e: Elemento a insertar
        predecesor: Nodo anterior al nuevo nodo
        sucesor: Nodo posterior al nuevo nodo

        Devuelve:
        Nodo recién creado
        """
        newest = self._Node(e, predecessor, successor)
        predecessor._siguiente = newest
        successor._anterior = newest
        self._size += 1
        return newest

    def _delete_node(self, node):
        """

        Eliminar un nodo no centinela de la lista y devolver su elemento (O(1)).

        Argumentos:
        nodo: Nodo a eliminar

        Devuelve:
        Elemento del nodo eliminado

        Genera:
        ValueError: Si el nodo es un centinela
        """
        if node in (self._header, self._trailer):
            raise ValueError('No se pueden eliminar los nodos centinelas')
            
        predecessor = node._anterior
        successor = node._siguiente
        predecessor._siguiente = successor
        successor._anterior = predecessor
        self._size -= 1
        
        element = node._element  # Almacenar elemento eliminado
        # Referencias claras para ayudar a la recolección de basura
        node._anterior = node._siguiente = node._vuelo = None  
        return element

    def _search(self, e):
        """
        Buscar el elemento e en la lista (O(n)).

        Argumentos:
        e: Elemento a buscar

        Devuelve:
        Primer nodo que contiene el elemento o Ninguno si no se encuentra
        """
        current = self._header._siguiente  # Salta el header
        while current != self._trailer:  # Hasta que lleguemos al trailer
            if current._vuelo == e:
                return current
            current = current.__siguiente
        return None

    def insertar_al_frente(self, vuelo):
        """Insertar el elemento e al principio de la lista (O(1))."""
        return self._insert_between(vuelo, self._header, self._header._siguiente)

    def insertar_al_final(self, vuelo):
        """Insertar el elemento e al final de la lista (O(1))."""
        return self._insert_between(vuelo, self._trailer._anterior, self._trailer)

    def contains(self, e):
        """Comprueba si el elemento e está en la lista (O(n))."""
        return self._search(e) is not None
    
    def obtener_primero(self):
        """Devuelve el primer vuelo de la lista (O(1))."""
        if self.is_empty():
            return None  # si esta vacia regresa none
        return self._header._siguiente._vuelo
    
    def obtener_ultimo(self):
        """Devuelve el ultimo vuelo de la lista (O(1))."""
        if self.is_empty():
            return None  # si esta vacia regresa none
        return self._trailer._anterior._vuelo

    def __str__(self):
        """Representación de cadena de la lista (O(n))."""
        elements = []
        current = self._header._siguiente
        while current != self._trailer:
            elements.append(str(current._element))
            current = current._siguiente
        return ' <-> '.join(elements) if elements else 'lista vacia'
    


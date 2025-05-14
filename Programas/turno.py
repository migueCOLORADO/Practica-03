from typing import Optional
from jugada import Jugada

class Turno:
    def __init__(self, numero: int, blanca: Jugada, negra: Optional[Jugada] = None):
        self.numero = numero
        self.blanca = blanca
        self.negra = negra

    def __repr__(self):
        return f"Turno({self.numero}: {self.blanca} | {self.negra})"

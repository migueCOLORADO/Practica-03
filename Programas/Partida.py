from typing import List
from Turno import Turno

class Partida:
    def __init__(self, turnos: List[Turno]):
        self.turnos = turnos

    def __repr__(self):
        return f"Partida(turnos={self.turnos})"

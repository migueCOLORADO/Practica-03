import re
from typing import List
from jugada import Jugada
from turno import Turno
from partida import Partida

class ParserSAN:
    RE_ENROQUE = re.compile(r'^(O-O|O-O-O)([+#])?$')
    RE_MOV_PIEZA = re.compile(r'^[KQRBN](?:[a-h]|[1-8]|[a-h][1-8])?x?[a-h][1-8](?:=[KQRBN])?[+#]?$')
    RE_MOV_PEON_AVANCE = re.compile(r'^[a-h][1-8](?:=[KQRBN])?[+#]?$')
    RE_MOV_PEON_CAPTURA = re.compile(r'^[a-h]x[a-h][1-8](?:=[KQRBN])?[+#]?$')

    def __init__(self, texto_partida: str):
        self.tokens = texto_partida.split()
        self.pos = 0

    def parse(self) -> Partida:
        turnos: List[Turno] = []
        while self.pos < len(self.tokens):
            turno = self._parse_turno()
            turnos.append(turno)
        return Partida(turnos)

    def _parse_turno(self) -> Turno:
        token_num = self._next_token()
        if not token_num.endswith('.') or not token_num[:-1].isdigit():
            raise ValueError(f"Turno mal formado: '{token_num}' (se espera '<número>.')")
        numero = int(token_num[:-1])

        jug_blanca = Jugada(self._parse_jugada())
        jug_negra = None

        if self.pos < len(self.tokens) and not self.tokens[self.pos].endswith('.'):
            jug_negra = Jugada(self._parse_jugada())

        return Turno(numero, jug_blanca, jug_negra)

    def _parse_jugada(self) -> str:
        token = self._next_token()
        if (self._es_enroque(token) or self._es_movimiento_pieza(token)
            or self._es_mov_peon_avance(token) or self._es_mov_peon_captura(token)):
            return token
        raise ValueError(f"Jugada inválida: '{token}'")

    def _es_enroque(self, token: str) -> bool:
        return bool(self.RE_ENROQUE.match(token))

    def _es_movimiento_pieza(self, token: str) -> bool:
        return bool(self.RE_MOV_PIEZA.match(token))

    def _es_mov_peon_avance(self, token: str) -> bool:
        return bool(self.RE_MOV_PEON_AVANCE.match(token))

    def _es_mov_peon_captura(self, token: str) -> bool:
        return bool(self.RE_MOV_PEON_CAPTURA.match(token))

    def _next_token(self) -> str:
        if self.pos >= len(self.tokens):
            raise ValueError("Entrada incompleta: se esperaba más datos")
        token = self.tokens[self.pos]
        self.pos += 1
        return token


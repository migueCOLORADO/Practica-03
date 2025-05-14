import re
from typing import List, Optional
from jugada import Jugada
from turno import Turno
from partida import Partida

class ParserSAN:
    # Expresiones regulares para validación
    RE_ENROQUE = re.compile(r'^(O-O|O-O-O)(\+|#)?$')
    RE_PIEZA = re.compile(r'^[KQRBN][a-h]?[1-8]?x?[a-h][1-8](=[QRBN])?(\+|#)?$')
    RE_PEON_AVANCE = re.compile(r'^[a-h][1-8](=[QRBN])?(\+|#)?$')
    RE_PEON_CAPTURA = re.compile(r'^[a-h]x[a-h][1-8](=[QRBN])?(\+|#)?$')
    RE_TURNO = re.compile(r'^\d+\.$')

    def __init__(self, texto_partida: str):
        self.texto = texto_partida
        self.tokens = texto_partida.split()
        self.pos = 0
        self.turno_esperado = 1
        
    def obtenerElementos(self):
        return self.texto

    def parse(self) -> Partida:        
        turnos: List[Turno] = []
        try:
            while self.pos < len(self.tokens):
                turno = self._parse_turno()
                turnos.append(turno)
                self.turno_esperado += 1
            return Partida(turnos)
        except ValueError as e:
            raise ValueError(f"Error en posición {self.pos}: {str(e)}")

    def _parse_turno(self) -> Turno:
        # Validar número de turno
        token_num = self._next_token()
        if not self.RE_TURNO.match(token_num):
            raise ValueError(f"Formato de turno inválido: '{token_num}'")
        
        numero = int(token_num[:-1])
        if numero != self.turno_esperado:
            raise ValueError(f"Turno fuera de secuencia: esperado {self.turno_esperado}, obtenido {numero}")

        # Parsear jugada blanca
        jug_blanca = self._parse_jugada()
        
        # Parsear jugada negra
        jug_negra = None
        if self.pos < len(self.tokens) and not self.RE_TURNO.match(self.tokens[self.pos]):
            jug_negra = self._parse_jugada()

        return Turno(numero, jug_blanca, jug_negra)

    def _parse_jugada(self) -> Jugada:
        token = self._next_token()
        
        if self._es_enroque(token):
            return Jugada(token)
        elif self._es_movimiento_pieza(token):
            return Jugada(token)
        elif self._es_mov_peon(token):
            return Jugada(token)
        
        raise ValueError(f"Movimiento inválido: '{token}'")

    def _es_enroque(self, token: str) -> bool:
        return bool(self.RE_ENROQUE.match(token))

    def _es_movimiento_pieza(self, token: str) -> bool:
        return bool(self.RE_PIEZA.match(token))

    def _es_mov_peon(self, token: str) -> bool:
        return (bool(self.RE_PEON_AVANCE.match(token)) or 
                bool(self.RE_PEON_CAPTURA.match(token)))

    def _next_token(self) -> str:
        if self.pos >= len(self.tokens):
            raise ValueError("Fin inesperado de la entrada")
        token = self.tokens[self.pos]
        self.pos += 1
        return token

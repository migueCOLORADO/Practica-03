import re
from typing import List
from jugada import Jugada
from turno import Turno
from partida import Partida

class ParserSAN:
    # Expresiones regulares para cada producción SAN
    RE_ENROQUE = re.compile(r'^(O-O|O-O-O)([+#])?$')
    RE_MOV_PIEZA = re.compile(
        r'^(?P<pieza>[KQRBN])'                       # Pieza
        r'(?P<desambiguacion>([a-h]|[1-8]|[a-h][1-8]))?'  # Desambiguación opcional (letra | número | letra+número)
        r'(?P<captura>x)?'                            # Captura opcional
        r'(?P<destino>[a-h][1-8])'                    # Casilla destino
        r'(?:=(?P<promocion>[KQRBN]))?'               # Promoción opcional
        r'(?P<check>[+#])?$'                          # Jaque/mate opcional
    )
    RE_MOV_PEON_AVANCE = re.compile(
        r'^(?P<destino>[a-h][1-8])'                   # Casilla de avance
        r'(?:=(?P<promocion>[KQRBN]))?'               # Promoción opcional
        r'(?P<check>[+#])?$'                          # Jaque/mate opcional
    )
    RE_MOV_PEON_CAPTURA = re.compile(
        r'^(?P<origen>[a-h])'                         # Columna origen
        r'x'                                         # Captura
        r'(?P<destino>[a-h][1-8])'                   # Casilla destino
        r'(?:=(?P<promocion>[KQRBN]))?'               # Promoción opcional
        r'(?P<check>[+#])?$'                          # Jaque/mate opcional
    )
    # Resultado final de la partida (opcional): 1-0, 0-1, 1/2-1/2
    RE_RESULT = re.compile(r'^(1-0|0-1|1/2-1/2)$')

    def __init__(self, texto_partida: str):
        # Filtrar comentarios y anotaciones (p.ej. ; ... o {...}) si los hubiera
        limpio = re.sub(r"\{[^}]*\}|;[^\n]*", "", texto_partida)
        self.tokens = limpio.split()
        self.pos = 0

    def parse(self) -> Partida:
        turnos: List[Turno] = []
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            # si encontramos un resultado final, lo saltamos y terminamos
            if self.RE_RESULT.match(token):
                break
            turno = self._parse_turno()
            turnos.append(turno)
        return Partida(turnos)

    def _parse_turno(self) -> Turno:
        token_num = self._next_token()
        if not token_num.endswith('.') or not token_num[:-1].isdigit():
            raise ValueError(f"Turno mal formado: '{token_num}' (se espera '<número>.')")
        numero = int(token_num[:-1])
        if numero < 1:
            raise ValueError(f"Número de turno inválido: {numero} (debe ser >= 1)")

        jug_blanca = Jugada(self._parse_jugada())
        jug_negra = None

        if self.pos < len(self.tokens):
            siguiente = self.tokens[self.pos]
            # si no es número de turno ni resultado, interpretamos jugada negra
            if not siguiente.endswith('.') and not self.RE_RESULT.match(siguiente):
                jug_negra = Jugada(self._parse_jugada())

        return Turno(numero, jug_blanca, jug_negra)

    def _parse_jugada(self) -> str:
        token = self._next_token()
        if (self._es_enroque(token)
            or self._es_movimiento_pieza(token)
            or self._es_mov_peon_avance(token)
            or self._es_mov_peon_captura(token)):
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

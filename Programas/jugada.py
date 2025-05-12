class Jugada:
    def __init__(self, texto: str):
        self.texto = texto

    def __repr__(self):
        return f"Jugada(texto='{self.texto}')"

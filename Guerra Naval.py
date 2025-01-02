class Equipo:
    def __init__(self, name, size, orientacion, row, col):
        self.orientacion = orientacion
        self.row = row
        self.col = col
        self.name = name
        self.size = size
        self.estado = True

    def impacto(self):
        self.estado = False
        print(f"Impacto en {self.name}!")

    def falla(self):
        print("Agua!")


class Grilla:
    def __init__(self, size):
        self.size = size
        self.matriz = [["\u25A1" for _ in range(size)] for _ in range(size)]  # \u25A1 es un cuadrado vacío

    def imprimir_grilla(self):
        print("  " + " ".join(map(str, range(self.size))))
        for idx, fila in enumerate(self.matriz):
            print(f"{idx} " + " ".join(fila))
        print()


class PosicionesPropias(Grilla):
    def posicion_equipo(self, equipo):
        row, col = equipo.row, equipo.col

        if equipo.orientacion == "H":
            for count in range(equipo.size):
                if col + count >= len(self.matriz[0]) or self.matriz[row][col + count] != "\u25A1":
                    print(f"No se puede colocar {equipo.name} en {row}-{col}. Espacio insuficiente o ya ocupado.")
                    return False
            for count in range(equipo.size):
                self.matriz[row][col + count] = equipo.name[0]

        elif equipo.orientacion == "V":
            for count in range(equipo.size):
                if row + count >= len(self.matriz) or self.matriz[row + count][col] != "\u25A1":
                    print(f"No se puede colocar {equipo.name} en {row}-{col}. Espacio insuficiente o ya ocupado.")
                    return False
            for count in range(equipo.size):
                self.matriz[row + count][col] = equipo.name[0]

        print(f"{equipo.name} colocado correctamente.")
        return True

    def atacan_grilla(self, row, col):
        if self.matriz[row][col] != "\u25A1":
            print("Impacto!")
            return True
        else:
            print("Agua!")
            return False


class MapaAtaque(Grilla):
    def registrar_ataque(self, row, col, impacto):
        if impacto:
            self.matriz[row][col] = "I"
            print("Ataque registrado: Impacto.")
        else:
            self.matriz[row][col] = "F"
            print("Ataque registrado: Falla.")


class Jugador:
    def __init__(self, name):
        self.name = name
        self.equipos_activos = []

    def agregar_equipo(self, equipo):
        self.equipos_activos.append(equipo)

    def baja_equipo(self, equipo):
        self.equipos_activos.remove(equipo)

    def cuenta_equipos_activos(self):
        return len(self.equipos_activos)


def configurar_tablero(jugador, mapa, equipos):
    print(f"* Configurando el tablero para {jugador.name} *")
    mapa.imprimir_grilla()
    for equipo_data in equipos:
        while True:
            try:
                fila = int(input(f"Fila para {equipo_data['name']}: "))
                if fila < 0 or fila >= mapa.size:
                    print(f"Fila fuera de rango. Debe estar entre 0 y {mapa.size - 1}.")
                    continue

                columna = int(input(f"Columna para {equipo_data['name']}: "))
                if columna < 0 or columna >= mapa.size:
                    print(f"Columna fuera de rango. Debe estar entre 0 y {mapa.size - 1}.")
                    continue

                orientacion = input("Orientación (H o V): ").upper()
                if orientacion not in ["H", "V"]:
                    print("Orientación inválida. Ingrese 'H' para horizontal o 'V' para vertical.")
                    continue

                equipo = Equipo(equipo_data["name"], equipo_data["size"], orientacion, fila, columna)
                if mapa.posicion_equipo(equipo):
                    jugador.agregar_equipo(equipo)
                    mapa.imprimir_grilla()
                    break
                else:
                    print("Intento inválido. Intente nuevamente.")
            except ValueError:
                print("Entrada inválida. Ingrese números para fila y columna.")


def fase_ataque(atacante, defensor, mapa_ataque, mapa_defensor):
    print(f"* Turno de ataque para {atacante.name} *")
    print("Mapa de ataque actual:")
    mapa_ataque.imprimir_grilla()
    while True:
        try:
            fila = int(input("Ingrese la fila de ataque: "))
            if fila < 0 or fila >= mapa_defensor.size:
                print(f"Fila fuera de rango. Debe estar entre 0 y {mapa_defensor.size - 1}.")
                continue

            columna = int(input("Ingrese la columna de ataque: "))
            if columna < 0 or columna >= mapa_defensor.size:
                print(f"Columna fuera de rango. Debe estar entre 0 y {mapa_defensor.size - 1}.")
                continue

            impacto = mapa_defensor.atacan_grilla(fila, columna)
            mapa_ataque.registrar_ataque(fila, columna, impacto)
            print("Mapa de ataque actualizado:")
            mapa_ataque.imprimir_grilla()
            if impacto:
                for equipo in defensor.equipos_activos:
                    if equipo.row == fila and equipo.col == columna:
                        equipo.impacto()
                        defensor.baja_equipo(equipo)
                        break
            break
        except ValueError:
            print("Entrada inválida. Ingrese números para fila y columna.")


# Datos iniciales
equipos = [
    {"name": "Portaaviones", "size": 5},
    {"name": "Acorazado", "size": 4},
    {"name": "Crucero", "size": 3},
    {"name": "Destructor", "size": 2},
    {"name": "Submarino", "size": 1},
]

size = int(input("Ingrese el tamaño de la grilla (>= 7): "))
while size < 7:
    size = int(input("Tamaño inválido. Ingrese un tamaño de grilla mayor o igual a 7: "))

player_1 = Jugador(input("Nombre del jugador 1: "))
player_2 = Jugador(input("Nombre del jugador 2: "))

mapa_player_1 = PosicionesPropias(size)
mapa_player_2 = PosicionesPropias(size)

ataques_player_1 = MapaAtaque(size)
ataques_player_2 = MapaAtaque(size)

configurar_tablero(player_1, mapa_player_1, equipos)
configurar_tablero(player_2, mapa_player_2, equipos)

while player_1.cuenta_equipos_activos() > 0 and player_2.cuenta_equipos_activos() > 0:
    fase_ataque(player_1, player_2, ataques_player_1, mapa_player_2)
    if player_2.cuenta_equipos_activos() == 0:
        print(f"{player_1.name} gana!")
        break

    fase_ataque(player_2, player_1, ataques_player_2, mapa_player_1)
    if player_1.cuenta_equipos_activos() == 0:
        print(f"{player_2.name} gana!")
        break

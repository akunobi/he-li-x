import os
import time
import sys
import random

# --- CONFIGURACIÓN DE ESTILO CLÍNICO ---
class C:
    # Paleta de colores "Monitor Médico"
    CYAN = '\033[96m'      # Interfaz general
    BLUE = '\033[94m'      # Datos masculinos / bordes
    PURPLE = '\033[95m'    # Datos femeninos
    GREEN = '\033[92m'     # Sano / Positivo
    YELLOW = '\033[93m'    # Precaución / Portador
    RED = '\033[91m'       # Alerta / Enfermo
    WHITE = '\033[97m'     # Texto brillante
    GREY = '\033[90m'      # Elementos pasivos
    END = '\033[0m'        # Reset
    BOLD = '\033[1m'

class Sym:
    # Símbolos Universales (No requieren NerdFonts)
    MALE = "♂"
    FEMALE = "♀"
    ARROW = "►"
    DOT = "•"
    BLOCK = "█"
    SHADE = "▒"
    
    # Bordes de caja (ASCII Extendido estándar)
    TL = "╔" # Top Left
    TR = "╗" # Top Right
    BL = "╚" # Bottom Left
    BR = "╝" # Bottom Right
    H = "═"  # Horizontal
    V = "║"  # Vertical
    T_TOP = "╦"
    T_BOT = "╩"
    T_MID = "╬"
    L_MID = "╠"
    R_MID = "╣"

# --- FUNCIONES VISUALES ---

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_adn_header():
    # Arte ASCII grande y limpio
    print(f"{C.CYAN}")
    print(r"      ▄▄▄▄▄▄   ▐ ▄     ▄▄▄· ")
    print(r"      •██  ▪  •█▌▐█   ▐█ ▀█ ")
    print(r"       ▐█.▪ ▄█▀▄▐█▐▐▌ ▄█▀▀█ ")
    print(r"       ▐█▌·▐█▌.▐▌██▐█▌▐█ ▪▐▌")
    print(r"       ▀▀ur ▀█▄▀▪▀▀ █▪ ▀  ▀ ")
    print(f"    {C.GREY}SISTEMA DE ANÁLISIS GENÉTICO v2.0{C.END}")
    print(f"{C.BLUE}{Sym.H * 40}{C.END}\n")

def barra_progreso_medica(texto):
    print(f"\n{C.GREY} [{texto}]...{C.END}")
    sys.stdout.write(f" {C.CYAN}")
    for _ in range(30):
        time.sleep(0.04)
        # Efecto de latido o escaneo
        char = random.choice(["-", "=", "≡", "▓"])
        sys.stdout.write(char)
        sys.stdout.flush()
    sys.stdout.write(f"{C.END} {C.GREEN}[OK]{C.END}\n")

def caja_texto(texto, color=C.WHITE, ancho=40):
    # Encierra texto en una caja bonita
    print(f" {color}{Sym.TL}{Sym.H * (ancho-2)}{Sym.TR}")
    print(f" {Sym.V} {texto.center(ancho-4)} {Sym.V}")
    print(f" {Sym.BL}{Sym.H * (ancho-2)}{Sym.BR}{C.END}")

# --- LÓGICA GENÉTICA ---

def formatear_alelo(a1, a2):
    # Ordena para visualización: Mayúscula siempre a la izquierda
    if a2 == "Y": return f"X{a1}Y " # Espacio extra para alinear con XX
    genes = sorted([a1, a2])
    return f"X{genes[0]}X{genes[1]}"

def obtener_diagnostico(a1, a2, S):
    """Retorna: (Texto Estado, Color)"""
    # Lógica hombre
    if a2 == "Y":
        if a1 == S: return ("SANO", C.GREEN)
        return ("ENFERMO", C.RED)
    
    # Lógica mujer
    genes = sorted([a1, a2])
    if genes == [S, S]: return ("SANA", C.GREEN)
    if genes == [S, S.lower()]: return ("PORTADORA", C.YELLOW)
    return ("ENFERMA", C.RED)

# --- PROGRAMA PRINCIPAL ---

def main():
    limpiar()
    imprimir_adn_header()

    # 1. Configuración de Patología
    print(f"{C.WHITE} PASO 1: IDENTIFICACIÓN DE PATOLOGÍA{C.END}")
    enf = input(f" {C.CYAN}{Sym.ARROW} Nombre de la enfermedad:{C.END} ").strip().capitalize()
    if not enf: enf = "Hemofilia"
    
    S = enf[0].upper()
    e = enf[0].lower()

    print(f"    {C.GREY}Alelo Dominante (Sano):{C.END} {C.GREEN}{S}{C.END}")
    print(f"    {C.GREY}Alelo Recesivo (Enf.): {C.END} {C.RED}{e}{C.END}\n")

    # 2. Configuración de Padres
    print(f"{C.WHITE} PASO 2: MUESTRAS DE LOS PADRES{C.END}")
    
    # Madre
    print(f" {C.PURPLE}{Sym.FEMALE} MADRE:{C.END} [1]Sana [2]Portadora [3]Enferma")
    try: m_op = int(input(f" {C.CYAN}{Sym.ARROW} Selección:{C.END} "))
    except: m_op = 1
    
    # Padre
    print(f" {C.BLUE}{Sym.MALE} PADRE:{C.END} [1]Sano [2]Enfermo")
    try: p_op = int(input(f" {C.CYAN}{Sym.ARROW} Selección:{C.END} "))
    except: p_op = 1

    # Definición de Genes
    m_alelos = (S, S) if m_op == 1 else (S, e) if m_op == 2 else (e, e)
    p_alelos = (S, "Y") if p_op == 1 else (e, "Y")

    # Efecto "Cargando"
    barra_progreso_medica("SECUENCIANDO ADN")
    barra_progreso_medica("CALCULANDO PROBABILIDADES")
    limpiar()

    # --- VISUALIZACIÓN DE RESULTADOS ---
    
    # Encabezado Reporte
    print(f"{C.BLUE}{Sym.TL}{Sym.H*58}{Sym.TR}")
    print(f"{Sym.V}  REPORTE GENÉTICO: {C.BOLD}{C.WHITE}{enf.upper().center(38)}{C.END}{C.BLUE}   {Sym.V}")
    print(f"{Sym.BL}{Sym.H*58}{Sym.BR}{C.END}\n")

    # PREPARAR DATOS PARA LA TABLA
    # Pre-calculamos textos sin color para medir espacios, luego aplicamos color
    # c1, c2, c3, c4 son los genotipos de los hijos
    
    def color_gen(txt):
        # Colorea las letras dentro del string: S->Verde, e->Rojo
        res = ""
        for char in txt:
            if char == S: res += f"{C.GREEN}{char}{C.END}"
            elif char == e: res += f"{C.RED}{char}{C.END}"
            else: res += f"{C.GREY}{char}{C.END}"
        return res

    raw_c1 = formatear_alelo(m_alelos[0], p_alelos[0]).replace(" ", "")
    raw_c2 = formatear_alelo(m_alelos[0], p_alelos[1]).replace(" ", "")
    raw_c3 = formatear_alelo(m_alelos[1], p_alelos[0]).replace(" ", "")
    raw_c4 = formatear_alelo(m_alelos[1], p_alelos[1]).replace(" ", "")

    col_c1 = color_gen(raw_c1)
    col_c2 = color_gen(raw_c2)
    col_c3 = color_gen(raw_c3)
    col_c4 = color_gen(raw_c4)

    # --- LAYOUT HORIZONTAL (TABLA + LISTA) ---
    
    # Construcción de la Tabla de Punnett (Ancho fijo visual)
    # Usamos f-strings con padding manual
    
    esp = " " * 3 # Espaciado celda
    
    # Bloque Tabla (Izquierda)
    b_tabla = [
        f"        {C.BLUE}{Sym.MALE} PADRE{C.END}",
        f"       X{color_gen(p_alelos[0])}      {color_gen(p_alelos[1])}",
        f"     {C.GREY}┌───────┬───────┐{C.END}",
        f"  X{color_gen(m_alelos[0])} {C.GREY}│{C.END} {col_c1}  {C.GREY}│{C.END} {col_c2}  {C.GREY}│{C.END}",
        f"{C.PURPLE}{Sym.FEMALE}{C.END}    {C.GREY}├───────┼───────┤{C.END}",
        f"  X{color_gen(m_alelos[1])} {C.GREY}│{C.END} {col_c3}  {C.GREY}│{C.END} {col_c4}  {C.GREY}│{C.END}",
        f"     {C.GREY}└───────┴───────┘{C.END}"
    ]

    # Bloque Resultados (Derecha)
    b_res = [f"{C.WHITE}{C.BOLD}DIAGNÓSTICO DESCENDENCIA:{C.END}", ""]
    
    hijos = [(m_alelos[0], p_alelos[0]), (m_alelos[0], p_alelos[1]),
             (m_alelos[1], p_alelos[0]), (m_alelos[1], p_alelos[1])]
    
    stats = {"SANO": 0, "PORTADORA": 0, "ENFERMO": 0}

    for i, h in enumerate(hijos):
        sexo_icon = f"{C.BLUE}{Sym.MALE}{C.END}" if "Y" in h else f"{C.PURPLE}{Sym.FEMALE}{C.END}"
        gen_str = formatear_alelo(h[0], h[1])
        diag_txt, diag_col = obtener_diagnostico(h[0], h[1], S)
        
        # Guardar estadística
        key = diag_txt if "PORTADORA" not in diag_txt and "SANA" not in diag_txt else diag_txt.replace("A", "O")
        # Unificamos claves para el conteo simple
        if "SANA" in diag_txt or "SANO" in diag_txt: stats["SANO"] += 1
        elif "PORTADORA" in diag_txt: stats["PORTADORA"] += 1
        else: stats["ENFERMO"] += 1
        
        # Formatear línea
        linea = f"{i+1}. {sexo_icon} {gen_str:<5} {C.GREY}»{C.END} {diag_col}{diag_txt:<9}{C.END}"
        b_res.append(linea)

    # IMPRESIÓN LADO A LADO
    print("")
    alto = max(len(b_tabla), len(b_res))
    for i in range(alto):
        izq = b_tabla[i] if i < len(b_tabla) else " " * 25
        der = b_res[i] if i < len(b_res) else ""
        # 30 espacios fijos para la tabla izquierda
        print(f" {izq:<45}   {der}")
    print("")

    # --- BARRA DE ESTADÍSTICAS FINAL ---
    total = 4
    pct_sano = int((stats["SANO"]/total)*20)
    pct_port = int((stats["PORTADORA"]/total)*20)
    pct_enf = int((stats["ENFERMO"]/total)*20)

    # Dibujo de barra visual
    barra = f"{C.GREEN}{'█'*pct_sano}{C.YELLOW}{'▒'*pct_port}{C.RED}{'░'*pct_enf}{C.END}"
    fondo_barra = f"{C.GREY}{'·' * (20 - (pct_sano+pct_port+pct_enf))}{C.END}"
    
    caja_texto(f"PROBABILIDAD GLOBAL DE RIESGO", C.CYAN, 60)
    print(f"  Visual: [{barra}{fondo_barra}]")
    print(f"  Datos:  {C.GREEN}{Sym.BLOCK} Sanos: {stats['SANO']}{C.END}   "
          f"{C.YELLOW}{Sym.SHADE} Portadores: {stats['PORTADORA']}{C.END}   "
          f"{C.RED}░ Enfermos: {stats['ENFERMO']}{C.END}\n")
    
    print(f"{C.BLUE}{Sym.H*60}{C.END}")

if __name__ == "__main__":
    while True:
        main()
        if input(f"\n{C.GREY} ¿Analizar nueva muestra? (Enter=Sí / n=No): {C.END}").lower() == 'n':
            print(" Cerrando sistema médico...")
            break

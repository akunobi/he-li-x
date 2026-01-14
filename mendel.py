import os
import time
import sys
import re

# --- CONFIGURACIÓN DE NERD FONTS Y COLORES ---
class Icon:
    # Nerd Fonts (Iconos)
    DNA = ""       # Matraz/DNA
    MALE = ""      # Hombre
    FEMALE = ""    # Mujer
    HEART = ""     # Corazón/Salud
    CHECK = ""     # Check
    WARN = ""      # Triángulo alerta
    CROSS = ""     # Cruz error
    ARROW = ""     # Flecha derecha
    CHART = ""     # Gráfico
    BOX_TOP = "┌"
    BOX_MID = "├"
    BOX_BOT = "└"
    LINE_H = "─"
    LINE_V = "│"
    DOT = ""

class Color:
    PURPLE = '\033[38;5;141m'
    BLUE = '\033[38;5;39m'
    CYAN = '\033[38;5;44m'
    GREEN = '\033[38;5;77m'
    YELLOW = '\033[38;5;220m'
    ORANGE = '\033[38;5;208m'
    RED = '\033[38;5;196m'
    GREY = '\033[38;5;240m'
    WHITE = '\033[38;5;255m'
    BOLD = '\033[1m'
    END = '\033[0m'

# --- MOTOR DE ALINEACIÓN PERFECTA ---

def len_visible(texto):
    """Calcula la longitud del texto ignorando los códigos de color ANSI"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return len(ansi_escape.sub('', texto))

def centrar_celda(texto, ancho):
    """Centra texto con colores dentro de un ancho fijo sin romper la tabla"""
    largo_real = len_visible(texto)
    padding = ancho - largo_real
    pad_izq = padding // 2
    pad_der = padding - pad_izq
    return " " * pad_izq + texto + " " * pad_der

def imprimir_fila(col_izq, col_der, ancho_izq=36):
    """Imprime dos columnas alineadas perfectamente ignorando colores"""
    largo_izq = len_visible(col_izq)
    # Calculamos cuántos espacios faltan para llegar al ancho deseado
    espacios = " " * (ancho_izq - largo_izq)
    if largo_izq > ancho_izq: 
        espacios = " " # Si se pasa, al menos un espacio
    print(f" {col_izq}{espacios}   {Color.GREY}│{Color.END}   {col_der}")

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- LÓGICA DE GENÉTICA ---

def formatear_alelo(a1, a2):
    # Ordena: Mayúscula primero. Si hay Y, va segunda.
    if a2 == "Y": return f"X{a1} Y"
    gens = sorted([a1, a2])
    return f"X{gens[0]} X{gens[1]}"

def obtener_estado(a1, a2, S):
    # Retorna: (Texto formateado, Icono)
    if a2 == "Y": # Chico
        if a1 == S: return (f"{Color.GREEN}SANO{Color.END}", Icon.CHECK)
        else: return (f"{Color.RED}ENFERMO{Color.END}", Icon.CROSS)
    else: # Chica
        gens = sorted([a1, a2])
        if gens == [S, S]: return (f"{Color.GREEN}SANA{Color.END}", Icon.CHECK)
        elif gens == [S, S.lower()]: return (f"{Color.YELLOW}PORTADORA{Color.END}", Icon.WARN)
        else: return (f"{Color.RED}ENFERMA{Color.END}", Icon.CROSS)

# --- APP PRINCIPAL ---

def app():
    limpiar()
    
    # Header
    print(f"\n{Color.PURPLE}{Color.BOLD} {Icon.DNA}  CALCULADORA GENÉTICA (CROMOSOMA X) {Color.END}")
    print(f"{Color.GREY}{Icon.LINE_H * 60}{Color.END}\n")

    # Inputs
    print(f" {Icon.HEART}  Nombre de la patología:")
    enfermedad = input(f" {Color.BLUE} {Icon.ARROW}  {Color.END}").capitalize()
    if not enfermedad: enfermedad = "Hemofilia"
    
    S = enfermedad[0].upper()
    e = enfermedad[0].lower()

    print(f"\n {Icon.FEMALE}  {Color.ORANGE}MADRE{Color.END} [1]Sana [2]Portadora [3]Enferma")
    try: m_opc = int(input(f" {Color.BLUE} {Icon.ARROW}  {Color.END}"))
    except: m_opc = 1
    
    print(f"\n {Icon.MALE}  {Color.CYAN}PADRE{Color.END} [1]Sano [2]Enfermo")
    try: p_opc = int(input(f" {Color.BLUE} {Icon.ARROW}  {Color.END}"))
    except: p_opc = 1

    # Definir alelos
    m_alelos = (S, S) if m_opc == 1 else (S, e) if m_opc == 2 else (e, e)
    p_alelos = (S, "Y") if p_opc == 1 else (e, "Y")

    limpiar()
    
    # --- RENDERIZADO DEL DASHBOARD ---
    
    print(f"\n{Color.BOLD}{Color.WHITE}  RESUMEN: CRUCE {enfermedad.upper()}{Color.END}")
    print(f"  {Color.GREY}Padres: X{m_alelos[0]}X{m_alelos[1]}  x  X{p_alelos[0]}Y{Color.END}\n")

    # Preparar datos de celdas (Texto coloreado)
    def c(a1, a2):
        txt = formatear_alelo(a1, a2).replace(" ", "")
        # Colorear genes: Verde mayus, Rojo minus
        res = ""
        for char in txt:
            if char == S: res += f"{Color.GREEN}{char}{Color.END}"
            elif char == e: res += f"{Color.RED}{char}{Color.END}"
            elif char in ["X", "Y"]: res += f"{Color.GREY}{char}{Color.END}"
        return res

    # Generamos los contenidos de las 4 celdas
    c1 = c(m_alelos[0], p_alelos[0])
    c2 = c(m_alelos[0], p_alelos[1])
    c3 = c(m_alelos[1], p_alelos[0])
    c4 = c(m_alelos[1], p_alelos[1])

    # Columna Izquierda: TABLA PUNNETT (Construcción manual precisa)
    # Usamos centrar_celda para asegurar que los códigos de color no rompan el ancho
    W = 10 # Ancho de celda
    tabla = [
        f"        {Color.CYAN}{Icon.MALE} Padre{Color.END}",
        f"        X{p_alelos[0]}        {p_alelos[1]}",
        f"     {Icon.BOX_TOP}{Icon.LINE_H*W}{Icon.LINE_H}{Icon.LINE_H*W}{Icon.BOX_TOP[::-1]}", # Top border
        f"  X{m_alelos[0]} {Icon.LINE_V}{centrar_celda(c1, W)}{Icon.LINE_V}{centrar_celda(c2, W)}{Icon.LINE_V}",
        f"{Color.ORANGE}{Icon.FEMALE}{Color.END}    {Icon.BOX_MID}{Icon.LINE_H*W}{Icon.BOX_MID}{Icon.LINE_H*W}{Icon.BOX_MID[::-1]}",
        f"  X{m_alelos[1]} {Icon.LINE_V}{centrar_celda(c3, W)}{Icon.LINE_V}{centrar_celda(c4, W)}{Icon.LINE_V}",
        f"     {Icon.BOX_BOT}{Icon.LINE_H*W}┴{Icon.LINE_H*W}┘"
    ]

    # Columna Derecha: RESULTADOS
    resultados_txt = [f"{Icon.CHART} {Color.BOLD}ANÁLISIS DESCENDENCIA{Color.END}", ""]
    
    hijos = [(m_alelos[0], p_alelos[0]), (m_alelos[0], p_alelos[1]),
             (m_alelos[1], p_alelos[0]), (m_alelos[1], p_alelos[1])]
    
    stats = {"SANO": 0, "PORTADORA": 0, "ENFERMO": 0}

    for gen in hijos:
        # Texto del genotipo formateado bonito
        gen_bonito = formatear_alelo(gen[0], gen[1])
        estado_txt, icono = obtener_estado(gen[0], gen[1], S)
        
        # Icono sexo
        sexo_icon = f"{Color.CYAN}{Icon.MALE}{Color.END}" if "Y" in gen else f"{Color.ORANGE}{Icon.FEMALE}{Color.END}"
        
        # Guardar línea
        linea = f"{sexo_icon} {gen_bonito:<6} {Icon.ARROW} {estado_txt} {icono}"
        resultados_txt.append(linea)
        
        # Stats (simplificado para el contador)
        clean_state = len_visible(estado_txt) # Truco sucio para saber estado
        if "SANA" in estado_txt or "SANO" in estado_txt: stats["SANO"] += 1
        elif "PORTADORA" in estado_txt: stats["PORTADORA"] += 1
        else: stats["ENFERMO"] += 1

    # --- IMPRIMIR COLUMNAS ALINEADAS ---
    max_filas = max(len(tabla), len(resultados_txt))
    
    print(f"{Color.GREY}{Icon.LINE_H * 65}{Color.END}")
    
    for i in range(max_filas):
        # Obtener parte izquierda o espacio vacío
        t_izq = tabla[i] if i < len(tabla) else ""
        # Obtener parte derecha o espacio vacío
        t_der = resultados_txt[i] if i < len(resultados_txt) else ""
        
        imprimir_fila(t_izq, t_der, ancho_izq=35)
        
    print(f"{Color.GREY}{Icon.LINE_H * 65}{Color.END}")
    
    # Barra de estadísticas final
    total = 4
    p_sano = int((stats["SANO"]/total)*10)
    p_port = int((stats["PORTADORA"]/total)*10)
    p_enf = int((stats["ENFERMO"]/total)*10)
    
    barra = f"{Color.GREEN}{Icon.DOT * p_sano}{Color.YELLOW}{Icon.DOT * p_port}{Color.RED}{Icon.DOT * p_enf}{Color.END}"
    leyenda = f"{Color.GREEN}Sano: {stats['SANO']}{Color.END}  {Color.YELLOW}Port: {stats['PORTADORA']}{Color.END}  {Color.RED}Enf: {stats['ENFERMO']}{Color.END}"
    
    print(f"\n {Icon.CHART} Distribución: {barra}  ({leyenda})\n")

if __name__ == "__main__":
    while True:
        app()
        if input(f" {Icon.DNA} ¿Reiniciar? (Enter/n): ").lower() == 'n': break

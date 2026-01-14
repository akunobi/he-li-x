import os
import sys
import time
import re

# --- 1. CONFIGURACIÓN VISUAL Y COLORES ---
class C:
    # Colores brillantes para neón
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    GREY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class Box:
    # Caracteres de dibujo de caja (Box Drawing)
    # Usamos líneas dobles para contenedores principales y simples para internos
    TL, TR = "╔", "╗"
    BL, BR = "╚", "╝"
    H, V = "═", "║"
    
    # Conectores y nodos
    NODE_L = "╠"
    NODE_R = "╣"
    T_DOWN = "╦"
    T_UP = "╩"
    CROSS = "╬"
    
    # Líneas finas
    S_H = "─"
    S_V = "│"
    S_TL, S_TR = "┌", "┐"
    S_BL, S_BR = "└", "┘"

# --- 2. MOTOR DE ALINEACIÓN (EL SECRETO) ---

def visible_len(texto):
    """
    Calcula la longitud REAL del texto quitando los códigos de color invisibles.
    Esto soluciona el problema de desalineación.
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return len(ansi_escape.sub('', texto))

def centrar_seguro(texto, ancho, relleno=" "):
    """
    Centra el texto considerando que los colores no ocupan espacio.
    """
    v_len = visible_len(texto)
    if v_len >= ancho:
        return texto # No cabe, se devuelve tal cual (o podrías recortar)
    
    espacio_total = ancho - v_len
    izq = espacio_total // 2
    der = espacio_total - izq
    return (relleno * izq) + texto + (relleno * der)

def alinear_izq(texto, ancho):
    v_len = visible_len(texto)
    return texto + (" " * (ancho - v_len))

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- 3. CONSTRUCTOR DE INTERFAZ (UI) ---

def dibujar_caja(titulo, lineas_contenido, color_borde, ancho=30):
    """
    Genera una lista de strings que forman una caja perfecta.
    """
    caja = []
    
    # Borde Superior (Con título incrustado)
    t_len = visible_len(titulo)
    pad_h = ancho - 2 - t_len - 2 # -2 bordes -2 espacios alrededor titulo
    if pad_h < 0: pad_h = 0
    
    # Construcción matemática del header
    # Ej: ╔══ TITULO ════════╗
    b_sup = f"{color_borde}{Box.TL}{Box.H*2} {C.WHITE}{titulo}{C.RESET}{color_borde} {Box.H * (pad_h)}{Box.TR}{C.RESET}"
    caja.append(b_sup)
    
    # Contenido
    for linea in lineas_contenido:
        # Centramos cada línea de contenido
        linea_centrada = centrar_seguro(linea, ancho - 4) # -4 por bordes y margen interno
        caja.append(f"{color_borde}{Box.V} {linea_centrada} {Box.V}{C.RESET}")
    
    # Borde Inferior
    caja.append(f"{color_borde}{Box.BL}{Box.H * (ancho - 2)}{Box.BR}{C.RESET}")
    
    return caja

def unir_bloques_horizontalmente(bloques, espaciado=2):
    """
    Toma varias cajas (listas de strings) y las imprime una al lado de la otra.
    """
    # Altura máxima
    alto = max(len(b) for b in bloques)
    ancho_espacio = " " * espaciado
    
    for i in range(alto):
        linea_final = ""
        for bloq in bloques:
            if i < len(bloq):
                linea_final += bloq[i]
            else:
                # Si este bloque es más corto, rellenar con vacíos del ancho del bloque
                ancho_bloque = visible_len(bloq[0]) 
                linea_final += " " * ancho_bloque
            linea_final += ancho_espacio
        print(linea_final)

# --- 4. LÓGICA DE GENÉTICA ---

def app():
    limpiar()
    
    # HEADER
    print(f"\n{centrar_seguro(f'{C.CYAN}🧬 GENETICS SYSTEM PRO 🧬{C.RESET}', 80)}")
    print(f"{C.GREY}{Box.S_H * 80}{C.RESET}\n")

    # --- INPUT DE DATOS ---
    
    # Caja 1: Enfermedad
    print(f" {C.WHITE}Configuración del Análisis:{C.RESET}")
    enf = input(f" {C.CYAN}► Nombre de la patología: {C.RESET}").strip().capitalize()
    if not enf: enf = "Hemofilia"
    
    S = enf[0].upper()
    e = enf[0].lower()
    
    # Caja 2: Madre y Padre (Inputs simples para velocidad)
    print(f"\n {C.PURPLE}► Madre (XX):{C.RESET} [1]Sana [2]Portadora [3]Enferma")
    try: m = int(input(f"   Selección {C.GREY}>>{C.RESET} "))
    except: m = 1
    
    print(f"\n {C.BLUE}► Padre (XY):{C.RESET} [1]Sano [2]Enfermo")
    try: p = int(input(f"   Selección {C.GREY}>>{C.RESET} "))
    except: p = 1

    # Cálculos
    m_genes = (S,S) if m==1 else (S,e) if m==2 else (e,e)
    p_genes = (S,"Y") if p==1 else (e,"Y")
    
    hijos = [
        (m_genes[0], p_genes[0]), # Hija 1
        (m_genes[0], p_genes[1]), # Hijo 1
        (m_genes[1], p_genes[0]), # Hija 2
        (m_genes[1], p_genes[1])  # Hijo 2
    ]

    limpiar()
    print("\n")

    # --- RENDERIZADO VISUAL ---
    
    # 1. NIVEL SUPERIOR: PADRES (Cajas Flotantes)
    
    # Preparamos el contenido de las cajas
    # Formato: ICONO GENOTIPO
    c_madre = [
        f"{C.WHITE}Genotipo:{C.RESET}",
        f"{C.PURPLE}{C.BOLD}X{m_genes[0]} X{m_genes[1]}{C.RESET}",
        f"{C.GREY}(Cromosomas XX){C.RESET}"
    ]
    
    c_padre = [
        f"{C.WHITE}Genotipo:{C.RESET}",
        f"{C.BLUE}{C.BOLD}X{p_genes[0]} {p_genes[1]}{C.RESET}",
        f"{C.GREY}(Cromosomas XY){C.RESET}"
    ]

    box_m = dibujar_caja("MADRE", c_madre, C.PURPLE, ancho=26)
    box_p = dibujar_caja("PADRE", c_padre, C.BLUE, ancho=26)
    
    # Dibujar flechas de conexión en medio
    # Creamos un "bloque" de texto que sea solo las flechas
    conector = [
        "", "",
        f" {C.GREY}{Box.S_H*3}► CRUCE ◄{Box.S_H*3}{C.RESET} ", 
        "", ""
    ]
    
    # Imprimimos: MADRE - CONECTOR - PADRE
    print(centrar_seguro(f"{C.WHITE}MAPA DE HERENCIA GENÉTICA: {enf.upper()}{C.RESET}", 80))
    print("")
    # Truco de alineación global: calculamos margen izquierdo
    margen = " " * 8
    unir_bloques_horizontalmente([margen, *box_p, conector, *box_m], espaciado=0)

    # 2. NIVEL INFERIOR: DESCENDENCIA (4 Nodos)
    
    print(f"\n{centrar_seguro(f'{C.GREY}▼ RESULTADOS PROBABILÍSTICOS ▼{C.RESET}', 80)}\n")
    
    bloques_hijos = []
    
    for i, gen in enumerate(hijos):
        a1, a2 = gen
        es_hombre = "Y" in gen
        
        # Determinar estado y colores
        texto_estado = ""
        color_estado = ""
        
        if es_hombre:
            titulo = f"HIJO {i+1}"
            borde = C.BLUE
            gen_str = f"X{a1} Y"
            if a1 == S: 
                texto_estado = "SANO"
                color_estado = C.GREEN
            else:
                texto_estado = "ENFERMO"
                color_estado = C.RED
        else:
            titulo = f"HIJA {i+1}"
            borde = C.PURPLE
            gens = sorted([a1, a2])
            gen_str = f"X{gens[0]} X{gens[1]}"
            if gens == [S, S]:
                texto_estado = "SANA"
                color_estado = C.GREEN
            elif gens == [S, e]:
                texto_estado = "PORTADORA"
                color_estado = C.YELLOW
            else:
                texto_estado = "ENFERMA"
                color_estado = C.RED
        
        # Contenido de la tarjeta del hijo
        contenido = [
            f"{C.WHITE}{gen_str}{C.RESET}",
            f"{C.GREY}{Box.S_H*10}{C.RESET}", # Separador interno
            f"{color_estado}{C.BOLD}{texto_estado}{C.RESET}"
        ]
        
        # Crear caja y añadir a la lista
        bloques_hijos.append(dibujar_caja(titulo, contenido, borde, ancho=18))

    # Imprimir los 4 hijos alineados
    # Calculamos margen para centrar 4 cajas de 18 chars + 3 espacios entre ellas
    # Ancho total approx = (18*4) + (2*3) = 72 + 6 = 78 chars.
    unir_bloques_horizontalmente([" "] + bloques_hijos, espaciado=1)
    print("\n")

if __name__ == "__main__":
    while True:
        app()
        if input(f"{C.GREY} [Enter] Nuevo análisis / [n] Salir: {C.RESET}").lower() == 'n':
            break

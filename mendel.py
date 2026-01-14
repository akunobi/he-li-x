import os
import sys
import time

# --- 1. MOTOR GRÁFICO (NO TOCAR) ---
class C:
    CYAN = '\033[36m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    GREY = '\033[90m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class Box:
    TL, TR = "╭", "╮"
    BL, BR = "╰", "╯"
    H, V = "─", "│"
    T_DOWN, T_UP = "┬", "┴"
    JOINT = "┼"

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- 2. COMPONENTES DE INTERFAZ (UI) ---

def crear_tarjeta_simple(titulo, contenido, color_borde, ancho=30):
    """Crea una caja simple con texto centrado"""
    b_sup = f"{color_borde}{Box.TL}{Box.H*(ancho-2)}{Box.TR}{C.RESET}"
    texto = f"{color_borde}{Box.V}{C.WHITE}{contenido.center(ancho-2)}{C.RESET}{color_borde}{Box.V}{C.RESET}"
    b_inf = f"{color_borde}{Box.BL}{Box.H*(ancho-2)}{Box.BR}{C.RESET}"
    
    # Etiqueta incrustada en el borde superior
    etiqueta = f" {titulo} "
    b_sup = b_sup.replace(Box.H * len(etiqueta), etiqueta, 1)
    
    return [b_sup, texto, b_inf]

def crear_panel_opciones(titulo, opciones, seleccion_actual, color, ancho=26):
    """Crea un menú de opciones seleccionable visualmente"""
    lineas = []
    # Borde Superior con Titulo
    b_s = f"{color}{Box.TL}{Box.H*2} {titulo} {Box.H*(ancho - 4 - len(titulo))}{Box.TR}{C.RESET}"
    lineas.append(b_s)
    
    for i, op in enumerate(opciones):
        idx = i + 1
        if idx == seleccion_actual:
            # Opción seleccionada (Resaltada)
            txt = f"{C.WHITE}► [{idx}] {op}{C.RESET}"
            relleno = " " * (ancho - len(op) - 9) # Calculo manual aprox de espacios
            linea = f"{color}{Box.V}{C.BOLD}{txt}{relleno}{C.RESET}{color}{Box.V}{C.RESET}"
        else:
            # Opción normal
            txt = f"{C.GREY}  [{idx}] {op}{C.RESET}"
            relleno = " " * (ancho - len(op) - 9)
            linea = f"{color}{Box.V}{txt}{relleno}{color}{Box.V}{C.RESET}"
        lineas.append(linea)
        
    # Relleno vertical si faltan lineas para igualar altura (opcional)
    while len(lineas) < 5:
        lineas.append(f"{color}{Box.V}{' '*(ancho-2)}{Box.V}{C.RESET}")

    lineas.append(f"{color}{Box.BL}{Box.H*(ancho-2)}{Box.BR}{C.RESET}")
    return lineas

def dibujar_input_dashboard(fase, data):
    """Renderiza toda la pantalla de inputs basada en el estado actual"""
    limpiar()
    print(f"\n{C.CYAN}{C.BOLD}   🧬  SISTEMA DE CONFIGURACIÓN GENÉTICA v3.0  🧬{C.RESET}\n")
    
    # --- PANEL SUPERIOR: ENFERMEDAD ---
    enf_txt = data.get('enf', 'Pendiente...')
    color_enf = C.GREEN if fase > 1 else C.YELLOW
    caja_enf = crear_tarjeta_simple("PATOLOGÍA", enf_txt, color_enf, 54)
    for l in caja_enf: print(f"      {l}")
    
    print("") # Separador
    
    # --- PANELES CENTRALES: PADRES ---
    if fase >= 2:
        # Definir opciones
        ops_m = ["Sana", "Portadora", "Enferma"]
        ops_p = ["Sano", "Enfermo"]
        
        # Determinar selección visual
        sel_m = data.get('m_op', 0) if fase > 2 else 0
        sel_p = data.get('p_op', 0) if fase > 3 else 0
        
        # Color activo o gris
        c_m = C.PURPLE if fase == 2 else (C.GREY if fase < 2 else C.PURPLE)
        c_p = C.BLUE if fase == 3 else (C.GREY if fase < 3 else C.BLUE)
        
        # Generar cajas
        panel_m = crear_panel_opciones("MADRE (XX)", ops_m, sel_m, c_m)
        panel_p = crear_panel_opciones("PADRE (XY)", ops_p, sel_p, c_p)
        
        # Imprimir lado a lado
        for lm, lp in zip(panel_m, panel_p):
            print(f"      {lm}  {lp}")

    print("\n")

# --- 3. LÓGICA DE NODOS (RESULTADO) ---
# (Reutilizamos la lógica visual de nodos flotantes pero comprimida)

def crear_nodo_res(titulo, gen, estado, color, ancho=14):
    b_sup = f"{color}{Box.TL}{Box.H*(ancho-2)}{Box.TR}{C.RESET}"
    b_inf = f"{color}{Box.BL}{Box.H*(ancho-2)}{Box.BR}{C.RESET}"
    l1 = f"{color}{Box.V}{C.WHITE}{titulo.center(ancho-2)}{C.RESET}{color}{Box.V}{C.RESET}"
    l2 = f"{color}{Box.V}{C.CYAN}{gen.center(ancho-2)}{C.RESET}{color}{Box.V}{C.RESET}"
    l3 = f"{color}{Box.V}{estado.center(ancho-2)}{color}{Box.V}{C.RESET}"
    return [b_sup, l1, l2, l3, b_inf]

def imprimir_arbol_final(padre, madre, hijos):
    # Renderizado final del árbol
    limpiar()
    print(f"\n{C.CYAN}   🧬  RESULTADO DEL ANÁLISIS  🧬{C.RESET}\n")
    
    # 1. Padres (Nodos estáticos simples)
    n_p = crear_nodo_res("PADRE", f"X{padre[0]} {padre[1]}", "---", C.BLUE)
    n_m = crear_nodo_res("MADRE", f"X{madre[0]} X{madre[1]}", "---", C.PURPLE)
    
    gap = " " * 8
    pad = " " * 12
    for l_p, l_m in zip(n_p, n_m):
        print(f"{pad}{l_p}{gap}{l_m}")

    # 2. Conectores (Hardcoded para estética)
    print(f"{pad}      {C.BLUE}└──────{C.GREY}┬{C.PURPLE}──────┘{C.RESET}")
    print(f"{pad}           {C.GREY}│{C.RESET}")
    print(f"{pad}   {C.GREY}┌───────┼───────┬───────┐{C.RESET}")

    # 3. Hijos
    filas = [[],[],[],[],[]]
    for h in hijos:
        # Analisis rápido
        a1, a2 = h
        sex = "HIJO" if "Y" in (a1, a2) else "HIJA"
        col = C.BLUE if sex == "HIJO" else C.PURPLE
        
        # Estado (Inferido por mayusculas)
        if sex == "HIJO":
            st = f"{C.GREEN}SANO" if a1.isupper() else f"{C.RED}ENF."
        else:
            gs = sorted([a1, a2])
            if gs[0].isupper() and gs[1].isupper(): st=f"{C.GREEN}SANA"
            elif gs[0].isupper(): st=f"{C.YELLOW}PORT."
            else: st=f"{C.RED}ENF."
            
        gen_txt = f"X{a1}Y" if sex=="HIJO" else f"X{sorted([a1,a2])[0]}X{sorted([a1,a2])[1]}"
        
        nodo = crear_nodo_res(sex, gen_txt, st, col, 12)
        for i in range(5): filas[i].append(nodo[i])

    for f in filas:
        print(f"   {'  '.join(f)}")
    print("\n")


# --- 4. FLUJO PRINCIPAL (MAIN LOOP) ---

def main():
    datos = {}
    
    # FASE 1: Nombre Enfermedad
    dibujar_input_dashboard(1, datos)
    # Input flotante simulado
    print(f"      {C.GREY}Escribe el nombre de la enfermedad:{C.RESET}")
    enf = input(f"      {C.CYAN}❯ {C.RESET}").strip().capitalize()
    if not enf: enf = "Hemofilia"
    datos['enf'] = enf
    
    # Preparar alelos
    S = enf[0].upper()
    e = enf[0].lower()

    # FASE 2: Madre
    dibujar_input_dashboard(2, datos)
    print(f"      {C.PURPLE}Selecciona genotipo MADRE (1-3):{C.RESET}")
    try: 
        m = int(input(f"      {C.PURPLE}❯ {C.RESET}"))
    except: m = 1
    datos['m_op'] = m

    # FASE 3: Padre
    dibujar_input_dashboard(3, datos)
    print(f"      {C.BLUE}Selecciona genotipo PADRE (1-2):{C.RESET}")
    try: 
        p = int(input(f"      {C.BLUE}❯ {C.RESET}"))
    except: p = 1
    datos['p_op'] = p

    # FASE 4: Procesando...
    dibujar_input_dashboard(4, datos) # Muestra todo seleccionado
    print(f"      {C.GREEN}Configuración completada. Calculando...{C.RESET}")
    time.sleep(1.5)

    # CÁLCULO
    m_alelos = (S,S) if m==1 else (S,e) if m==2 else (e,e)
    p_alelos = (S,"Y") if p==1 else (e,"Y")
    hijos = [
        (m_alelos[0], p_alelos[0]), (m_alelos[0], p_alelos[1]),
        (m_alelos[1], p_alelos[0]), (m_alelos[1], p_alelos[1])
    ]

    # MOSTRAR RESULTADOS
    imprimir_arbol_final(p_alelos, m_alelos, hijos)

if __name__ == "__main__":
    while True:
        main()
        if input(f"{C.GREY}Presiona Enter para reiniciar o 'n' para salir: {C.RESET}") == 'n': break

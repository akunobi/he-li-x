import os
import time
import sys

# --- 1. CONFIGURACIÓN VISUAL (COLORES Y ESTILOS) ---
class C:
    # Colores de fuente
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    GREY = '\033[90m'
    
    # Fondos (Backgrounds)
    BG_BLUE = '\033[44m'
    BG_RED = '\033[41m'
    
    # Estilos
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Ancho fijo de la interfaz para que siempre se vea centrada y perfecta
ANCHO = 74 

# --- 2. HERRAMIENTAS DE DIBUJO ---

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def centrar(texto, color=C.WHITE, ancho=ANCHO):
    # Calcula espacios para centrar el texto
    return f"{color}{texto.center(ancho)}{C.END}"

def linea_horizontal(estilo="simple"):
    char = "─" if estilo == "simple" else "═"
    return f"{C.BLUE}{char * ANCHO}{C.END}"

def imprimir_header():
    print(f"{C.CYAN}╔{'═' * (ANCHO-2)}╗{C.END}")
    print(centrar("🧬  SISTEMA DE ANÁLISIS GENÉTICO (CROMOSOMA X)  🧬", C.BOLD + C.CYAN))
    print(f"{C.CYAN}╚{'═' * (ANCHO-2)}╝{C.END}")

def input_validado(prompt, opciones_validas):
    while True:
        try:
            val = int(input(f"{C.BOLD} >> {prompt}: {C.END}"))
            if val in opciones_validas:
                return val
            print(f"{C.RED}    ⚠ Error: Opción no válida. Intente de nuevo.{C.END}")
        except ValueError:
            print(f"{C.RED}    ⚠ Error: Debe ingresar un número.{C.END}")

def animacion_carga():
    print("")
    sys.stdout.write(f"    {C.CYAN}Procesando ADN: {C.END}")
    for i in range(20):
        time.sleep(0.02)
        sys.stdout.write("█")
        sys.stdout.flush()
    print(" ✅\n")

# --- 3. LÓGICA GENÉTICA ---

def formatear_alelo(a1, a2):
    # Devuelve string ordenado (ej: XH Xh)
    if a2 == "Y": return f"X{a1} Y"
    genes = sorted([a1, a2])
    return f"X{genes[0]} X{genes[1]}"

def analizar_estado(a1, a2, S):
    # Devuelve (Texto Estado, Color, Icono)
    if a2 == "Y": # Hombre
        if a1 == S: return ("SANO", C.GREEN, "✅")
        else: return ("ENFERMO", C.RED, "❌")
    else: # Mujer
        gens = sorted([a1, a2])
        if gens == [S, S]: return ("SANA", C.GREEN, "✅")
        elif gens == [S, S.lower()]: return ("PORTADORA", C.YELLOW, "⚠️")
        else: return ("ENFERMA", C.RED, "❌")

# --- 4. PROGRAMA PRINCIPAL ---

def app():
    limpiar()
    imprimir_header()
    
    # --- PASO 1: NOMBRE ---
    print(centrar("CONFIGURACIÓN DE LA PATOLOGÍA", C.WHITE))
    print(linea_horizontal())
    enfermedad = input(f"    Nombre de la enfermedad (ej. Hemofilia): {C.CYAN}").capitalize()
    if not enfermedad: enfermedad = "Hemofilia"
    
    S = enfermedad[0].upper()
    e = enfermedad[0].lower()
    
    # --- PASO 2: PADRES ---
    print("\n" + centrar(f"GENOTIPOS DE LOS PROGENITORES", C.WHITE))
    
    # Panel Madre
    print(f"    {C.PURPLE}MADRE (XX){C.END}")
    print(f"    [1] {C.GREEN}Sana{C.END} (X{S}X{S})   [2] {C.YELLOW}Portadora{C.END} (X{S}X{e})   [3] {C.RED}Enferma{C.END} (X{e}X{e})")
    m_opc = input_validado("Seleccione condición de la Madre", [1, 2, 3])

    print("-" * ANCHO)

    # Panel Padre
    print(f"    {C.BLUE}PADRE (XY){C.END}")
    print(f"    [1] {C.GREEN}Sano{C.END} (X{S}Y)      [2] {C.RED}Enfermo{C.END} (X{e}Y)")
    p_opc = input_validado("Seleccione condición del Padre", [1, 2])

    # Definir alelos
    m_alelos = (S, S) if m_opc == 1 else (S, e) if m_opc == 2 else (e, e)
    p_alelos = (S, "Y") if p_opc == 1 else (e, "Y")

    animacion_carga()

    # --- PASO 3: VISUALIZACIÓN ---
    limpiar()
    imprimir_header()
    print(centrar(f"RESULTADOS DEL CRUCE: {enfermedad.upper()}", C.YELLOW))
    print(linea_horizontal("doble"))

    # Preparar celdas tabla
    c1 = formatear_alelo(m_alelos[0], p_alelos[0]).replace(" ","")
    c2 = formatear_alelo(m_alelos[0], p_alelos[1]).replace(" ","")
    c3 = formatear_alelo(m_alelos[1], p_alelos[0]).replace(" ","")
    c4 = formatear_alelo(m_alelos[1], p_alelos[1]).replace(" ","")

    # Layout Horizontal
    # Izquierda: Tabla Punnett
    # Derecha: Lista Resultados
    
    col_izq = [
        f"           {C.BLUE}Padre ♂{C.END}",
        f"            X{p_alelos[0]}          {p_alelos[1]}",
        f"      ┌────────────┬────────────┐",
        f"   X{m_alelos[0]} │ {C.BOLD}{c1:^10}{C.END} │ {C.BOLD}{c2:^10}{C.END} │",
        f" M    ├────────────┼────────────┤",
        f" a X{m_alelos[1]} │ {C.BOLD}{c3:^10}{C.END} │ {C.BOLD}{c4:^10}{C.END} │",
        f"      └────────────┴────────────┘"
    ]

    col_der = [
        f"{C.UNDERLINE}DESGLOSE DE DESCENDENCIA:{C.END}",
        "" # Espacio vacío
    ]

    hijos_raw = [(m_alelos[0], p_alelos[0]), (m_alelos[0], p_alelos[1]), 
                 (m_alelos[1], p_alelos[0]), (m_alelos[1], p_alelos[1])]
    
    # Contadores para estadísticas
    enfermos = 0
    portadores = 0
    
    for i, gen in enumerate(hijos_raw):
        sexo = "👦 Hijo" if "Y" in gen else "👧 Hija"
        gen_txt = formatear_alelo(gen[0], gen[1])
        txt_estado, color_est, icono = analizar_estado(gen[0], gen[1], S)
        
        # Guardar linea de texto
        col_der.append(f"{i+1}. {sexo} {gen_txt:<6} → {color_est}{txt_estado} {icono}{C.END}")
        
        # Stats
        if txt_estado == "ENFERMO" or txt_estado == "ENFERMA": enfermos += 1
        if txt_estado == "PORTADORA": portadores += 1

    # Imprimir columnas lado a lado
    for i in range(max(len(col_izq), len(col_der))):
        izq = col_izq[i] if i < len(col_izq) else " " * 35
        der = col_der[i] if i < len(col_der) else ""
        print(f" {izq:<50}   {der}")

    # --- PASO 4: RESUMEN ESTADÍSTICO (Footer) ---
    print("\n" + linea_horizontal("doble"))
    print(f"{C.BOLD} 📊 RESUMEN ESTADÍSTICO:{C.END}")
    
    prob_enf = (enfermos/4)*100
    prob_port = (portadores/4)*100
    prob_sano = 100 - prob_enf - prob_port
    
    # Barra visual de porcentajes
    barra = ""
    barra += "█" * int(prob_sano/5) 
    barra += "▒" * int(prob_port/5)
    barra += "░" * int(prob_enf/5)
    
    print(f"    Probabilidad de Enfermedad: {C.RED if prob_enf > 0 else C.GREEN}{prob_enf:.0f}%{C.END}")
    print(f"    Probabilidad de Portador/a: {C.YELLOW if prob_port > 0 else C.GREY}{prob_port:.0f}%{C.END}")
    print(f"    Visualización: [{C.GREEN}{'█'*int(prob_sano/10)}{C.YELLOW}{'█'*int(prob_port/10)}{C.RED}{'█'*int(prob_enf/10)}{C.END}]")
    print(linea_horizontal("doble"))
    print("\n")

if __name__ == "__main__":
    while True:
        app()
        if input(f"{C.GREY}¿Analizar otro caso? (Enter=Sí, N=Salir): {C.END}").lower() == 'n':
            print("Cerrando sistema...")
            break

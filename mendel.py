import os
import time
import sys

class Colores:
    # Estilos de texto
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Fondos (opcional para resaltar headers)
    BG_BLUE = '\033[44m'

def limpiar_pantalla():
    # Detecta si es Windows ('nt') o Linux/Mac ('posix')
    os.system('cls' if os.name == 'nt' else 'clear')

def barra_carga():
    print(f"\n{Colores.CYAN}Procesando cruce genético...{Colores.END}")
    # Simula una barra de carga
    ancho = 40
    for i in range(ancho + 1):
        time.sleep(0.04) # Velocidad de la carga
        sys.stdout.write(f"\r[{'█' * i}{'.' * (ancho - i)}] {int((i/ancho)*100)}%")
        sys.stdout.flush()
    print("\n")

def formatear_gen(a1, a2, S):
    # Esta función ordena los genes (Dominante primero) y devuelve string coloreado
    # Si hay una Y, siempre va segunda
    if a2 == "Y":
        txt = f"X{a1} Y"
    else:
        # Ordenamos alfabéticamente (Mayúscula 'H' antes que minúscula 'h')
        gens = sorted([a1, a2])
        txt = f"X{gens[0]} X{gens[1]}"
    return txt

def calcular_herencia():
    limpiar_pantalla()
    
    # Banner ASCII
    print(f"{Colores.HEADER}{Colores.BOLD}")
    print(r"""
   ____ _____ _   _ _____ _____ ___ ____    _    
  / ___| ____| \ | | ____|_   _|_ _/ ___|  / \   
 | |  _|  _| |  \| |  _|   | |  | | |     / _ \  
 | |_| | |___| |\  | |___  | |  | | |___ / ___ \ 
  \____|_____|_| \_|_____| |_| |___\____/_/   \_\
    """)
    print(f"    🧬 CALCULADORA DE CROMOSOMA X 🧬{Colores.END}\n")

    # --- PASO 1 ---
    print(f"{Colores.BG_BLUE}{Colores.BOLD} PASO 1: Configuración {Colores.END}")
    enfermedad = input(f" {Colores.BOLD}Nombre de la enfermedad:{Colores.END} ").capitalize()
    if not enfermedad: enfermedad = "Enfermedad"
    
    S = enfermedad[0].upper()
    e = enfermedad[0].lower()

    print(f"\n Detectado: Sano = {Colores.GREEN}{S}{Colores.END} | Enfermo = {Colores.RED}{e}{Colores.END}")

    # --- PASO 2 ---
    print(f"\n{Colores.BG_BLUE}{Colores.BOLD} PASO 2: Padres {Colores.END}")
    
    # Madre
    print(f"\n {Colores.HEADER}Madre (XX){Colores.END}:")
    print(f" [1] {Colores.GREEN}Sana{Colores.END}      (X{S} X{S})")
    print(f" [2] {Colores.YELLOW}Portadora{Colores.END} (X{S} X{e})")
    print(f" [3] {Colores.RED}Enferma{Colores.END}   (X{e} X{e})")
    try:
        m_opc = int(input(f" >> Selecciona {Colores.CYAN}(1-3){Colores.END}: "))
    except:
        m_opc = 1 # Por defecto si falla

    # Padre
    print(f"\n {Colores.BLUE}Padre (XY){Colores.END}:")
    print(f" [1] {Colores.GREEN}Sano{Colores.END}    (X{S} Y)")
    print(f" [2] {Colores.RED}Enfermo{Colores.END} (X{e} Y)")
    try:
        p_opc = int(input(f" >> Selecciona {Colores.CYAN}(1-2){Colores.END}: "))
    except:
        p_opc = 1

    # Lógica
    if m_opc == 1: m_alelos = (S, S)
    elif m_opc == 2: m_alelos = (S, e)
    else: m_alelos = (e, e)
    
    if p_opc == 1: p_alelos = (S, "Y")
    else: p_alelos = (e, "Y")

    # Ejecutar animación
    barra_carga()

    # --- RESULTADOS ---
    # Pre-calculamos los textos de las celdas para que la tabla no se rompa
    # Usamos la funcion formatear_gen para que ordene (XhXH -> XHXh)
    celda_1 = formatear_gen(m_alelos[0], p_alelos[0], S).replace(" ", "")
    celda_2 = formatear_gen(m_alelos[0], p_alelos[1], S).replace(" ", "")
    celda_3 = formatear_gen(m_alelos[1], p_alelos[0], S).replace(" ", "")
    celda_4 = formatear_gen(m_alelos[1], p_alelos[1], S).replace(" ", "")

    print(f"{Colores.BOLD}TABLA DE PUNNETT:{Colores.END}")
    # Construcción rígida de tabla usando f-strings con ancho fijo (:^10)
    print(f"           {Colores.BLUE}Padre ♂{Colores.END}")
    print(f"            {Colores.BOLD}X{p_alelos[0]}          {p_alelos[1]}{Colores.END}")
    print(f"      ┌────────────┬────────────┐")
    print(f"   {Colores.HEADER}X{m_alelos[0]}{Colores.END} │ {celda_1:^10} │ {celda_2:^10} │")
    print(f" {Colores.HEADER}M{Colores.END}    │            │            │")
    print(f" {Colores.HEADER}a{Colores.END}    ├────────────┼────────────┤")
    print(f" {Colores.HEADER}m{Colores.END}    │            │            │")
    print(f" {Colores.HEADER}á{Colores.END} {Colores.HEADER}X{m_alelos[1]}{Colores.END} │ {celda_3:^10} │ {celda_4:^10} │")
    print(f"      └────────────┴────────────┘")
    print("")

    # Lista detallada
    hijos_raw = [
        (m_alelos[0], p_alelos[0]),
        (m_alelos[1], p_alelos[0]),
        (m_alelos[0], p_alelos[1]),
        (m_alelos[1], p_alelos[1])
    ]

    print(f"{Colores.UNDERLINE}Desglose de Fenotipos:{Colores.END}\n")
    
    for gen in hijos_raw:
        a1, a2 = gen
        gen_str = formatear_gen(a1, a2, S) # Esto asegura XH Xh ordenado
        
        if "Y" in gen:
            sexo = f"{Colores.BLUE}Hijo ♂{Colores.END}"
            if a1 == S: estado = f"{Colores.GREEN}SANO ✅{Colores.END}"
            else: estado = f"{Colores.RED}ENFERMO ❌{Colores.END}"
        else:
            sexo = f"{Colores.HEADER}Hija ♀{Colores.END}"
            genes = sorted([a1, a2])
            if genes == [S, S]: estado = f"{Colores.GREEN}SANA ✅{Colores.END}"
            elif genes == [S, e]: estado = f"{Colores.YELLOW}PORTADORA ⚠️{Colores.END}"
            else: estado = f"{Colores.RED}ENFERMA ❌{Colores.END}"

        print(f" • {sexo} [{gen_str}] -> {estado}")
    
    print("\n")

if __name__ == "__main__":
    while True:
        calcular_herencia()
        seguir = input(f"{Colores.CYAN}¿Calcular otra? (s/n): {Colores.END}").lower()
        if seguir != 's':
            print("¡Hasta luego!")
            break

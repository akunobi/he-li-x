class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def imprimir_titulo():
    print(f"{Color.CYAN}{Color.BOLD}")
    print("╔══════════════════════════════════════════════╗")
    print("║   🧬 CALCULADORA GENÉTICA (CROMOSOMA X) 🧬   ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"{Color.END}")

def obtener_color_estado(estado):
    if "SANO" in estado or "SANA" in estado: return Color.GREEN
    if "PORTADORA" in estado: return Color.YELLOW
    return Color.RED

def calcular_herencia():
    imprimir_titulo()
    
    print(f"{Color.BOLD}Paso 1: Configuración de la Enfermedad{Color.END}")
    enfermedad = input("Nombre de la enfermedad: ")
    S = enfermedad[0].upper()  # Dominante (Sano)
    e = enfermedad[0].lower()  # Recesivo (Enfermo)

    print(f"\n{Color.BOLD}Paso 2: Genotipos de los Padres{Color.END}")
    print("-" * 40)
    
    # MADRE
    print(f"Madre ♀:")
    print(f"[1] {Color.GREEN}Sana{Color.END} (X{S} X{S})")
    print(f"[2] {Color.YELLOW}Portadora{Color.END} (X{S} X{e})")
    print(f"[3] {Color.RED}Enferma{Color.END} (X{e} X{e})")
    madre_opc = int(input(">> Elige opción (1-3): "))
    
    # PADRE
    print(f"\nPadre ♂:")
    print(f"[1] {Color.GREEN}Sano{Color.END} (X{S} Y)")
    print(f"[2] {Color.RED}Enfermo{Color.END} (X{e} Y)")
    padre_opc = int(input(">> Elige opción (1-2): "))

    # Lógica de alelos
    if madre_opc == 1: m_alelos = (S, S)
    elif madre_opc == 2: m_alelos = (S, e)
    else: m_alelos = (e, e)
    
    if padre_opc == 1: p_alelos = (S, "Y")
    else: p_alelos = (e, "Y")

    # Cruce
    hijos = [
        (m_alelos[0], p_alelos[0]), # Hija 1
        (m_alelos[1], p_alelos[0]), # Hija 2
        (m_alelos[0], p_alelos[1]), # Hijo 1
        (m_alelos[1], p_alelos[1])  # Hijo 2
    ]

    print(f"\n{Color.BOLD}Resultados del Cruce:{Color.END}")
    print("=" * 50)

    # Dibujando el Cuadro de Punnett
    print(f"       Padre ♂")
    print(f"       X{p_alelos[0]}         {p_alelos[1]}")
    print(f"    ┌───────┬───────┐")
    print(f" M  │ ♀     │ ♂     │")
    print(f" a X{m_alelos[0]} │ X{m_alelos[0]}X{p_alelos[0]}  │ X{m_alelos[0]}{p_alelos[1]}    │")
    print(f" d  │       │       │")
    print(f" r  ├───────┼───────┤")
    print(f" e  │ ♀     │ ♂     │")
    print(f"   X{m_alelos[1]} │ X{m_alelos[1]}X{p_alelos[0]}  │ X{m_alelos[1]}{p_alelos[1]}    │")
    print(f"    └───────┴───────┘")
    print("=" * 50)
    
    print(f"{Color.BOLD}Desglose detallado:{Color.END}\n")

    for i, gen in enumerate(hijos):
        alelo1, alelo2 = gen
        
        if alelo2 == "Y": # Chico
            sexo = "Hijo ♂"
            representacion = f"X{alelo1} Y "
            estado = "SANO ✅" if alelo1 == S else "ENFERMO ❌"
        else: # Chica
            sexo = "Hija ♀"
            genes_ordenados = sorted([alelo1, alelo2])
            representacion = f"X{genes_ordenados[0]} X{genes_ordenados[1]}"
            
            if genes_ordenados == [S, S]: estado = "SANA ✅"
            elif genes_ordenados == [S, e]: estado = "PORTADORA ⚠️"
            else: estado = "ENFERMA ❌"

        # Aplicar color al texto final
        color_texto = obtener_color_estado(estado)
        print(f"{i+1}. {sexo}: {representacion} -> {color_texto}{estado}{Color.END}")
    
    print("\n")

# Ejecutar
calcular_herencia()
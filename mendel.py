import os
import time
import sys

# --- CONFIGURACIÓN DE COLORES ---
class C:
    H = '\033[95m'   # Header (Morado)
    B = '\033[94m'   # Blue
    G = '\033[92m'   # Green (Sano)
    Y = '\033[93m'   # Yellow (Portador)
    R = '\033[91m'   # Red (Enfermo)
    E = '\033[0m'    # End (Reset)
    Bold = '\033[1m'

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def formatear_gen_ordenado(a1, a2):
    # Función para ordenar: Siempre mayúscula primero (XH Xh)
    if a2 == "Y": return f"X{a1} Y"
    gens = sorted([a1, a2])
    return f"X{gens[0]} X{gens[1]}"

def obtener_estado(alelo1, alelo2, S):
    # Lógica para determinar Sano/Portador/Enfermo y devolver texto coloreado
    if alelo2 == "Y": # Hombre
        return f"{C.G}SANO ✅{C.E}" if alelo1 == S else f"{C.R}ENFERMO ❌{C.E}"
    else: # Mujer
        gens = sorted([alelo1, alelo2])
        if gens == [S, S]: return f"{C.G}SANA ✅{C.E}"
        elif gens == [S, S.lower()]: return f"{C.Y}PORTADORA ⚠️{C.E}"
        else: return f"{C.R}ENFERMA ❌{C.E}"

def calcular():
    limpiar()
    print(f"{C.H}{C.Bold}╔═════════════════════════════════════════════════════════╗")
    print(f"║       🧬  ANALIZADOR GENÉTICO HORIZONTAL  🧬        ║")
    print(f"╚═════════════════════════════════════════════════════════╝{C.E}\n")

    # --- ENTRADA DE DATOS (Esto se queda vertical para facilidad de uso) ---
    enfermedad = input(f"Nombre de la enfermedad: {C.Bold}").capitalize()
    if not enfermedad: enfermedad = "Hemofilia"
    print(C.E, end="") # Reset color

    S = enfermedad[0].upper() # Dominante
    e = enfermedad[0].lower() # Recesivo

    print(f"\n{C.B}--- Configuración de Padres ---{C.E}")
    # Madre
    print(f"Madre ♀: [1]{C.G}Sana{C.E} [2]{C.Y}Portadora{C.E} [3]{C.R}Enferma{C.E}")
    try: m_opc = int(input(">> Opción: "))
    except: m_opc = 1
    
    # Padre
    print(f"Padre ♂: [1]{C.G}Sano{C.E} [2]{C.R}Enfermo{C.E}")
    try: p_opc = int(input(">> Opción: "))
    except: p_opc = 1

    # Definir alelos
    m_alelos = (S, S) if m_opc == 1 else (S, e) if m_opc == 2 else (e, e)
    p_alelos = (S, "Y") if p_opc == 1 else (e, "Y")

    # --- CONSTRUCCIÓN DEL LAYOUT HORIZONTAL ---
    
    # 1. Preparar datos de las celdas de la tabla
    c1 = formatear_gen_ordenado(m_alelos[0], p_alelos[0]).replace(" ","")
    c2 = formatear_gen_ordenado(m_alelos[0], p_alelos[1]).replace(" ","")
    c3 = formatear_gen_ordenado(m_alelos[1], p_alelos[0]).replace(" ","")
    c4 = formatear_gen_ordenado(m_alelos[1], p_alelos[1]).replace(" ","")

    # 2. Crear las líneas de la TABLA (Izquierda)
    # Usamos ljust() y colores cuidadosamente
    bloque_tabla = [
        f"           {C.B}Padre ♂{C.E}",
        f"            X{p_alelos[0]}          {p_alelos[1]}",
        f"      ┌────────────┬────────────┐",
        f"   X{m_alelos[0]} │ {c1:^10} │ {c2:^10} │",
        f" M    ├────────────┼────────────┤",
        f"   X{m_alelos[1]} │ {c3:^10} │ {c4:^10} │",
        f"      └────────────┴────────────┘"
    ]

    # 3. Crear las líneas de los RESULTADOS (Derecha)
    bloque_info = [
        f"{C.H}{C.Bold}   RESULTADOS Y PROBABILIDADES:{C.E}",
        f"   ────────────────────────────",
    ]
    
    # Generar texto de los 4 hijos
    hijos_raw = [(m_alelos[0], p_alelos[0]), (m_alelos[0], p_alelos[1]), 
                 (m_alelos[1], p_alelos[0]), (m_alelos[1], p_alelos[1])]
    
    for i, gen in enumerate(hijos_raw):
        sexo = "Hijo ♂" if "Y" in gen else "Hija ♀"
        gen_txt = formatear_gen_ordenado(gen[0], gen[1])
        estado = obtener_estado(gen[0], gen[1], S)
        bloque_info.append(f"   {i+1}. {sexo}: {gen_txt:<7} → {estado}")

    # 4. IMPRESIÓN LADO A LADO
    print(f"\n{C.Bold}Cruce Genético Visualizado:{C.E}\n")
    
    # Determinar altura máxima para el bucle
    altura = max(len(bloque_tabla), len(bloque_info))
    
    for i in range(altura):
        # Obtener línea izquierda (o vacío si se acaba)
        izq = bloque_tabla[i] if i < len(bloque_tabla) else " " * 35 
        
        # Obtener línea derecha (o vacío)
        der = bloque_info[i] if i < len(bloque_info) else ""
        
        # Ajuste de espaciado: La tabla visualmente ocupa unos 35-40 caracteres
        # necesitamos calcular el padding manual porque los códigos de color 
        # confunden a la función len() estándar.
        
        # Truco: Imprimimos Izquierda + Espaciador + Derecha
        # El padding fijo se añade tras la tabla
        padding = " " * 4 
        
        # Como 'izq' tiene códigos de colores invisibles, alinear es difícil con string format.
        # Simplemente imprimimos con un tabulador manual o calculando espacios visuales.
        # Para simplificar y que no se rompa, asumimos un ancho fijo visual para la columna 1.
        
        # Imprimir fila combinada
        # Nota: La tabla tiene ancho variable por colores, así que usamos un ancho fijo visual grande
        print(f"{izq:<50} {padding} {der}")

    print("\n")

if __name__ == "__main__":
    while True:
        calcular()
        if input(f"{C.B}¿Otra vez? (Enter=Si, n=No): {C.E}") == 'n': break

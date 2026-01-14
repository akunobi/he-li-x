import os
import sys
import re
import time

# --- 1. ESTILO Y PALETA DE COLORES ---
class C:
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    GREY = '\033[90m'
    END = '\033[0m'
    BOLD = '\033[1m'
    INV = '\033[7m' # Invertir colores

class GFX:
    # Bordes "Light" (Suelen verse mejor en web que los dobles)
    TL, TR = "┌", "┐"
    BL, BR = "└", "┘"
    H, V = "─", "│"
    
    # Elementos de "Vida" (Bloques y texturas)
    BLOCK = "█"
    SHADE_D = "▓" # Dark shade
    SHADE_M = "▒" # Medium shade
    SHADE_L = "░" # Light shade
    DOT = "•"
    ARROW = "►"
    DNA = "≡"

# --- 2. MOTOR DE ALINEACIÓN (CRÍTICO) ---

def clean_len(text):
    """Longitud visible ignorando colores ANSI"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return len(ansi_escape.sub('', text))

def center_text(text, width):
    """Centra texto calculando relleno matemático"""
    v_len = clean_len(text)
    pad = max(0, width - v_len)
    left = pad // 2
    right = pad - left
    return (" " * left) + text + (" " * right)

def make_box(title, content_lines, color, width=32, active=False):
    """
    Crea una caja con estilo 'High-Tech'.
    Usa bloques sólidos para el encabezado.
    """
    box = []
    
    # Colores dinámicos
    c_frame = color if active else C.GREY
    c_txt = C.WHITE if active else C.GREY
    
    # --- HEADER CON ESTILO ---
    # Creamos una barra sólida: [ ▓▒░ TITULO ░▒▓ ]
    # Calculamos espacio disponible para los bloques decorativos
    tit_clean = clean_len(title)
    deco_len = (width - 2 - tit_clean - 2) // 2 # -2 bordes, -2 espacios
    if deco_len < 0: deco_len = 0
    
    # Decoración izquierda/derecha
    deco = (GFX.SHADE_M * deco_len)[:deco_len] # Asegurar no pasar largo
    
    # Relleno exacto para ajustar al ancho
    inner_len = clean_len(deco)*2 + tit_clean + 2
    pad_extra = (width - 2) - inner_len
    
    header_inner = f"{deco} {C.BOLD}{title}{C.END}{c_frame} {deco}" + (" " * pad_extra)
    
    # Borde superior
    box.append(f"{c_frame}{GFX.TL}{GFX.H*(width-2)}{GFX.TR}{C.END}")
    # Línea de título con bloques
    box.append(f"{c_frame}{GFX.V}{header_inner}{GFX.V}{C.END}")
    # Separador
    box.append(f"{c_frame}{GFX.V}{GFX.H*(width-2)}{GFX.V}{C.END}")
    
    # --- CONTENIDO ---
    # Forzar altura fija (4 líneas de contenido)
    target_h = 4
    while len(content_lines) < target_h:
        content_lines.append("")
        
    for line in content_lines[:target_h]:
        # Centrado perfecto
        txt = center_text(line, width - 2)
        box.append(f"{c_frame}{GFX.V}{txt}{GFX.V}{C.END}")
        
    # --- FOOTER ---
    # Barra de estado inferior simulada
    bar = GFX.SHADE_L * (width-2)
    box.append(f"{c_frame}{GFX.V}{bar}{GFX.V}{C.END}")
    box.append(f"{c_frame}{GFX.BL}{GFX.H*(width-2)}{GFX.BR}{C.END}")
    
    return box

def render_duo(left_box, right_box):
    """Renderiza dos cajas con un conector animado en el medio"""
    h = len(left_box)
    
    # Encontrar el punto medio visual para el conector
    # La caja tiene: Borde, Titulo, Sep, Linea1, Linea2, Linea3, Linea4, Footer1, Footer2
    # El centro del contenido es aprox el índice 5
    mid_idx = 5 
    
    for i in range(h):
        if i == mid_idx:
            # Conector sofisticado
            conn = f" {C.GREY}≡{GFX.SHADE_M}{GFX.SHADE_D}{GFX.ARROW} CRUCE {C.END} "
        else:
            conn = "             " # 13 espacios
            
        print(f"   {left_box[i]}{conn}{right_box[i]}")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- 3. UI DASHBOARD ---

def main():
    state = {'step': 1, 'enf': '---', 'm': 0, 'p': 0}
    
    while True:
        clear()
        
        # LOGO SUPERIOR
        print(f"\n   {C.CYAN}{GFX.DNA} SISTEMA DE ANÁLISIS GENÉTICO {GFX.DNA}{C.END}")
        print(f"   {C.GREY}{GFX.H * 40}{C.END}\n")
        
        # --- PREPARACIÓN DE DATOS ---
        
        # 1. ENFERMEDAD
        c_enf = C.GREEN if state['step'] > 1 else C.YELLOW
        lbl_enf = state['enf'].upper() if state['enf'] != '---' else "CONFIGURANDO..."
        print(f"   {c_enf}{GFX.BLOCK} PATOLOGÍA ACTIVA:{C.END} {C.BOLD}{lbl_enf}{C.END}\n")
        
        # 2. CAJA MADRE
        lines_m = []
        col_m = C.PURPLE
        active_m = (state['step'] == 2)
        
        if state['step'] == 1:
            lines_m = ["", f"{C.GREY}Esperando datos", "del sistema..."]
            col_m = C.GREY
        elif state['step'] == 2:
            ops = ["Sana", "Portadora", "Enferma"]
            gens = ["(XX)", "(XXh)", "(XhXh)"]
            for i, op in enumerate(ops):
                if i+1 == state['m']: # Highlight
                    lines_m.append(f"{C.INV} {op} {gens[i]} {C.END}")
                else:
                    lines_m.append(f"{i+1}. {op}")
        else: # Finalizado
            sel = state['m']-1
            ops = ["SANA", "PORTADORA", "ENFERMA"]
            gens = ["Gen: XX", "Gen: XXh", "Gen: XhXh"]
            lines_m = ["", f"{C.BOLD}{ops[sel]}{C.END}", gens[sel], ""]

        # 3. CAJA PADRE
        lines_p = []
        col_p = C.BLUE
        active_p = (state['step'] == 3)
        
        if state['step'] < 3:
            lines_p = ["", f"{C.GREY}En espera...", ""]
            col_p = C.GREY
        elif state['step'] == 3:
            ops = ["Sano", "Enfermo"]
            gens = ["(XY)", "(XhY)"]
            for i, op in enumerate(ops):
                lines_p.append(f"{i+1}. {op} {gens[i]}")
        else:
            sel = state['p']-1
            ops = ["SANO", "ENFERMO"]
            gens = ["Gen: XY", "Gen: XhY"]
            lines_p = ["", f"{C.BOLD}{ops[sel]}{C.END}", gens[sel], ""]

        # --- RENDER ---
        # Ancho fijo de 28 caracteres
        b_m = make_box("MADRE", lines_m, col_m, 28, active_m or state['step']>2)
        b_p = make_box("PADRE", lines_p, col_p, 28, active_p or state['step']>3)
        
        render_duo(b_m, b_p)
        print("\n")
        
        # --- INPUTS ---
        prompt = f"   {C.CYAN}{GFX.ARROW}{C.END} "
        
        if state['step'] == 1:
            print(f"   {C.GREY}Ingrese nombre de la patología:{C.END}")
            i = input(prompt).strip().upper()
            if i: state['enf']=i; state['step']=2
            
        elif state['step'] == 2:
            print(f"   {C.PURPLE}Seleccione Genotipo Madre [1-3]:{C.END}")
            try:
                v = int(input(prompt))
                if 1<=v<=3: state['m']=v; state['step']=3
            except: pass
            
        elif state['step'] == 3:
            print(f"   {C.BLUE}Seleccione Genotipo Padre [1-2]:{C.END}")
            try:
                v = int(input(prompt))
                if 1<=v<=2: state['p']=v; state['step']=4
            except: pass
            
        elif state['step'] == 4:
            print(f"   {C.GREEN}{GFX.SHADE_D * 10} PROCESANDO {GFX.SHADE_D * 10}{C.END}")
            time.sleep(1)
            clear()
            show_result(state)
            if input(f"\n   [Enter] Reiniciar / [n] Salir: ") == 'n': sys.exit()
            else: state['step']=1; state['enf']='---'; state['m']=0; state['p']=0

def show_result(s):
    # Logica simple
    S_char, e_char = s['enf'][0], s['enf'][0].lower()
    
    # Genes
    gm = (S_char, S_char) if s['m']==1 else (S_char, e_char) if s['m']==2 else (e_char, e_char)
    gp = (S_char, "Y") if s['p']==1 else (e_char, "Y")
    
    hijos = []
    # Cruce: M1-P1, M1-P2, M2-P1, M2-P2
    combos = [(gm[0], gp[0]), (gm[0], gp[1]), (gm[1], gp[0]), (gm[1], gp[1])]
    
    print(f"\n   {C.CYAN}{GFX.BLOCK} REPORTE FINAL: {s['enf']} {GFX.BLOCK}{C.END}\n")
    
    # Mostrar resultados en tarjetas compactas
    for i, gen in enumerate(combos):
        is_boy = "Y" in gen
        tit = f"HIJO {i+1}" if is_boy else f"HIJA {i+1}"
        col = C.BLUE if is_boy else C.PURPLE
        
        # Formatear genes
        g1, g2 = gen
        if is_boy: 
            gtxt = f"X{g1} Y"
            st_val = g1 == S_char
        else:
            gs = sorted([g1, g2]) # Ordenar para que sea XH Xh
            gtxt = f"X{gs[0]} X{gs[1]}"
            st_val = (gs == [S_char, S_char])
            
        # Determinar estado texto
        if is_boy:
            st_txt = "SANO" if st_val else "ENFERMO"
            c_st = C.GREEN if st_val else C.RED
        else:
            # Recalcular para mujer
            gs = sorted([g1, g2])
            if gs == [S_char, S_char]: st_txt, c_st = "SANA", C.GREEN
            elif gs == [S_char, e_char]: st_txt, c_st = "PORTADORA", C.YELLOW
            else: st_txt, c_st = "ENFERMA", C.RED
            
        # Dibujar cajita manual para alineación perfecta en resultado
        # Usamos padding manual
        print(f"   {col}{GFX.TL}{GFX.H*18}{GFX.TR}{C.END}")
        print(f"   {col}{GFX.V} {center_text(tit, 16)} {GFX.V}{C.END}")
        print(f"   {col}{GFX.V} {C.WHITE}{center_text(gtxt, 16)}{C.END} {col}{GFX.V}{C.END}")
        print(f"   {col}{GFX.V} {c_st}{center_text(st_txt, 16)}{C.END} {col}{GFX.V}{C.END}")
        print(f"   {col}{GFX.BL}{GFX.H*18}{GFX.BR}{C.END}")
        # Pequeño espacio vertical entre hijos
        if i < 3: print(f"           {C.GREY}{GFX.V}{C.END}") 

if __name__ == "__main__":
    main()

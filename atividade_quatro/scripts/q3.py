import cv2
import numpy as np
import matplotlib.pyplot as plt
import heapq
import os

# =========================================================================
# QUESTÃO 3 - PIPELINE COMPLETO REPLICANDO O GRID DE REFERÊNCIA (100% MANUAL)
# =========================================================================

# --- OPERAÇÕES MORFOLÓGICAS MANUAIS (ELEMENTO ESTRUTURANTE 3x3 QUADRADO) ---
def dilatar_manual(img, iteracoes=1):
    h, w = img.shape
    saida = img.copy()
    for _ in range(iteracoes):
        temp = saida.copy()
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if temp[y, x] == 255:
                    saida[y-1:y+2, x-1:x+2] = 255
    return saida

def eroder_manual(img, iteracoes=1):
    h, w = img.shape
    saida = img.copy()
    for _ in range(iteracoes):
        temp = saida.copy()
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if temp[y, x] == 0:
                    saida[y-1:y+2, x-1:x+2] = 0
    return saida

def abertura_manual(img, iteracoes=2):
    # Abertura = Erosão seguida de Dilatação
    return dilatar_manual(eroder_manual(img, iteracoes), iteracoes)

def fechamento_manual(img, iteracoes=2):
    # Fechamento = Dilatação seguida de Erosão
    return eroder_manual(dilatar_manual(img, iteracoes), iteracoes)


# --- TRANSFORMADA DE DISTÂNCIA MANUAL (ALGORITMO CHAMPION TWO-PASS COSSENO/EUCLIDIANO APPROX) ---
def transformada_distancia_manual(img_binaria):
    h, w = img_binaria.shape
    dist = np.full((h, w), 999999.0, dtype=np.float32)
    dist[img_binaria == 0] = 0.0
    
    # Passo 1: Passada progressiva (cima para baixo, esquerda para direita)
    for y in range(1, h):
        for x in range(1, w):
            if img_binaria[y, x] == 255:
                dist[y, x] = min(dist[y, x],
                                 dist[y-1, x] + 1.0, 
                                 dist[y, x-1] + 1.0,
                                 dist[y-1, x-1] + 1.414)
                
    # Passo 2: Passada regressiva (baixo para cima, direita para esquerda)
    for y in range(h - 2, -1, -1):
        for x in range(w - 2, -1, -1):
            if img_binaria[y, x] == 255:
                dist[y, x] = min(dist[y, x],
                                 dist[y+1, x] + 1.0, 
                                 dist[y, x+1] + 1.0,
                                 dist[y+1, x+1] + 1.414)
    return dist


# --- DETECÇÃO DE COMPONENTES CONECTADOS MANUAL PARA MARCADORES (Rotulação por FloodFill) ---
def connected_components_manual(img_sure_fg):
    h, w = img_sure_fg.shape
    marcadores = np.zeros((h, w), dtype=np.int32)
    id_atual = 1
    
    # Varre a imagem procurando pixels de primeiro plano não rotulados
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if img_sure_fg[y, x] == 255 and marcadores[y, x] == 0:
                # Inicia um Flood Fill manual usando uma fila simples
                fila = [(y, x)]
                marcadores[y, x] = id_atual
                
                while fila:
                    cy, cx = fila.pop(0)
                    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ny, nx = cy + dy, cx + dx
                        if img_sure_fg[ny, nx] == 255 and marcadores[ny, nx] == 0:
                            marcadores[ny, nx] = id_atual
                            fila.append((ny, nx))
                id_atual += 1
                
    return marcadores, id_atual - 1


# --- CRESCIMENTO WATERSHED SIMPLIFICADO BASEADO EM FILA DE PRIORIDADES ---
def watershed_manual(imagem_gradiente, marcadores_iniciais, img_closing):
    h, w = imagem_gradiente.shape
    rotulos = marcadores_iniciais.copy()
    fila_prioridade = []
    
    # Insere as bordas dos marcadores na fila de prioridades
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if rotulos[y, x] > 0:
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ny, nx = y + dy, x + dx
                    if rotulos[ny, nx] == 0 and img_closing[ny, nx] == 255:
                        heapq.heappush(fila_prioridade, (imagem_gradiente[ny, nx], ny, nx, rotulo[y, x]))

    while fila_prioridade:
        val, y, x, rotulo_origem = heapq.heappop(fila_prioridade)
        
        if rotulos[y, x] != 0:
            continue
            
        borda_detectada = False
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w:
                if rotulos[ny, nx] > 0 and rotulos[ny, nx] != rotulo_origem:
                    borda_detectada = True
                    break
                    
        if borda_detectada:
            rotulos[y, x] = -1 # Linha do divisor de águas
        else:
            rotulos[y, x] = rotulo_origem
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w:
                    if rotulos[ny, nx] == 0 and img_closing[ny, nx] == 255:
                        heapq.heappush(fila_prioridade, (imagem_gradiente[ny, nx], ny, nx, rotulo_origem))
                        
    return rotulos


# =========================================================================
# EXECUÇÃO DO PIPELINE
# =========================================================================

pasta_saida = "resultados_watershed_final"
os.makedirs(pasta_saida, exist_ok=True)

# 0. Carregar imagem original
img_bgr = cv2.imread('fotos/naranjas.png')
if img_bgr is None:
    print("Erro: Verifique se sua imagem está em 'fotos/muedas.png'")
    exit()

# Conversão manual para cinza por luminância
gray = (0.114 * img_bgr[:,:,0] + 0.587 * img_bgr[:,:,1] + 0.299 * img_bgr[:,:,2]).astype(np.uint8)

# 1. Threshold (Convertido em THRESH_BINARY_INV manual)
# Usando um limiar ajustado padrão para separar as moedas do fundo claro
img_threshold = np.zeros_like(gray)
img_threshold[gray < 130] = 255  # Moedas ficam brancas (Invertido)

# 2. Closing (Passando a abertura antes para tirar ruídos e o fechamento para consolidar os corpos)
img_opening = abertura_manual(img_threshold, iteracoes=1)
img_closing = fechamento_manual(img_opening, iteracoes=2)

# 3. Distance Transform
mapa_distancia = transformada_distancia_manual(img_closing)
# Normalização para exibição visual [0, 255]
img_distance_transform = np.zeros_like(gray)
if np.max(mapa_distancia) > 0:
    img_distance_transform = ((mapa_distancia / np.max(mapa_distancia)) * 255).astype(np.uint8)

# 4. Local Maximum
# Extrai as cristas de distância mais altas de cada moeda (Cores brancas puras isoladas)
img_local_maximum = np.zeros_like(gray)
img_local_maximum[mapa_distancia > (0.45 * np.max(mapa_distancia))] = 255

# 5. Markers (Rótulos numéricos únicos + borda Unknown limpa em fundo preto)
mapa_sure_fg = img_local_maximum.copy()
marcadores, num_objetos = connected_components_manual(mapa_sure_fg)

# Incrementa marcadores para o fundo ser 1 (Crescimento correto)
marcadores_ajustados = marcadores + 1
img_sure_bg = dilatar_manual(img_closing, iteracoes=3)
unknown = img_sure_bg - img_closing
marcadores_ajustados[unknown == 255] = 0

# Imagem visual dos marcadores (escala cinza mapeada para o relatório)
img_markers_visual = (marcadores * (230 // (num_objetos + 1))).astype(np.uint8)

# Execução do algoritmo Watershed sobre o relevo inverso da distância
relevo = np.max(mapa_distancia) - mapa_distancia
resultado_rotulos = watershed_manual(relevo, marcadores_ajustados, img_closing)

# 6. Segmented - Gray
img_segmented_gray = np.zeros_like(gray)
for i in range(1, num_objetos + 2):
    tom = int(i * (255 / (num_objetos + 2)))
    img_segmented_gray[resultado_rotulos == i] = tom

# 7. Segmented - Color
np.random.seed(25) # Garante cores bonitas e bem distribuídas
paleta_cores = np.random.randint(40, 240, size=(num_objetos + 2, 3), dtype=np.uint8)
paleta_cores[1] = [30, 30, 30] # Fundo cinza escuro para manter o padrão das laranjas

img_segmented_color = np.zeros_like(img_bgr)
h, w = resultado_rotulos.shape
for y in range(h):
    for x in range(w):
        rot = resultado_rotulos[y, x]
        if rot > 0:
            img_segmented_color[y, x] = paleta_cores[rot]
        elif rot == -1:
            img_segmented_color[y, x] = [0, 0, 0] # Borda preta de separação na colorida

# 8. Output Image (Original com linhas de divisão em Vermelho)
img_output = img_bgr.copy()
img_output[resultado_rotulos == -1] = [0, 0, 255] # Linhas vermelhas puras


# =========================================================================
# RENDERIZAÇÃO DO MOSAICO 3x3 PERFEITO (IGUAL AO ENUNCIADO)
# =========================================================================
fig, axs = plt.subplots(3, 3, figsize=(15, 13))

# Converte BGR para RGB apenas para a amostragem correta do Matplotlib
img_rgb_original = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
img_rgb_output = cv2.cvtColor(img_output, cv2.COLOR_BGR2RGB)
img_rgb_segmented_color = cv2.cvtColor(img_segmented_color, cv2.COLOR_BGR2RGB)

# Linha 1
axs[0, 0].imshow(img_rgb_original); axs[0, 0].set_title("Original image", fontsize=14, weight='bold'); axs[0, 0].axis("off")
axs[0, 1].imshow(img_threshold, cmap='gray'); axs[0, 1].set_title("Threshold", fontsize=14, weight='bold'); axs[0, 1].axis("off")
axs[0, 2].imshow(img_closing, cmap='gray'); axs[0, 2].set_title("Closing", fontsize=14, weight='bold'); axs[0, 2].axis("off")

# Linha 2
axs[1, 0].imshow(img_distance_transform, cmap='gray'); axs[1, 0].set_title("Distance transform", fontsize=14, weight='bold'); axs[1, 0].axis("off")
axs[1, 1].imshow(img_local_maximum, cmap='gray'); axs[1, 1].set_title("Local maximum", fontsize=14, weight='bold'); axs[1, 1].axis("off")
axs[1, 2].imshow(img_markers_visual, cmap='gray'); axs[1, 2].set_title("Markers", fontsize=14, weight='bold'); axs[1, 2].axis("off")

# Linha 3
axs[2, 0].imshow(img_segmented_gray, cmap='gray'); axs[2, 0].set_title("Segmented - gray", fontsize=14, weight='bold'); axs[2, 0].axis("off")
axs[2, 1].imshow(img_rgb_segmented_color); axs[2, 1].set_title("Segmented - color", fontsize=14, weight='bold'); axs[2, 1].axis("off")
axs[2, 2].imshow(img_rgb_output); axs[2, 2].set_title("Output image", fontsize=14, weight='bold'); axs[2, 2].axis("off")

plt.tight_layout()

# Salva o mosaico completo montado
caminho_mosaico = os.path.join(pasta_saida, "mosaico_comparativo_3x3.png")
plt.savefig(caminho_mosaico, dpi=300, bbox_inches='tight')
plt.show()

print(f"\n[Sucesso] Mosaico 3x3 gerado e salvo em '{caminho_mosaico}'!")
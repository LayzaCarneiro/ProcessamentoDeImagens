import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# =========================================================================
# QUESTÃO 3 - PIPELINE COMPLETO BASEADO NAS FUNÇÕES REPASSADAS PELO ALUNO
# =========================================================================

# --- OPERAÇÕES MORFOLÓGICAS ADAPTADAS COM ELEMENTO ESTRUTURANTE 3x3 ---

def dilatar_manual(img, iteracoes=1):
    h, w = img.shape
    saida = img.copy()
    for _ in range(iteracoes):
        temp = saida.copy()
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                if temp[r, c] == 255:
                    saida[r-1:r+2, c-1:c+2] = 255
    return saida

def eroder_manual(img, iteracoes=1):
    h, w = img.shape
    saida = img.copy()
    for _ in range(iteracoes):
        temp = saida.copy()
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                if temp[r, c] == 0:
                    saida[r-1:r+2, c-1:c+2] = 0
    return saida

def opening(binary_img, kernel_size=3):
    # Abertura = Erosão seguida de Dilatação
    return dilatar_manual(eroder_manual(binary_img, 1), 1)

def closing(binary_img, kernel_size=3):
    # Fechamento = Dilatação seguida de Erosão
    return eroder_manual(dilatar_manual(binary_img, 1), 1)

# --- FUNÇÕES EXPLICITAS DA SUA NOVA BASE ---

def distance_transform(binary_img):
    h, w = binary_img.shape
    dist = np.where(binary_img == 0, 0, np.inf)
    
    for r in range(h):
        for c in range(w):
            if dist[r, c] > 0:
                top = dist[r - 1, c] + 1 if r > 0 else np.inf
                left = dist[r, c - 1] + 1 if c > 0 else np.inf
                dist[r, c] = min(dist[r, c], top, left)
                
    for r in range(h - 1, -1, -1):
        for c in range(w - 1, -1, -1):
            if dist[r, c] > 0:
                bottom = dist[r + 1, c] + 1 if r < h - 1 else np.inf
                right = dist[r, c + 1] + 1 if c < w - 1 else np.inf
                dist[r, c] = min(dist[r, c], bottom, right)
                
    return dist

def preprocess_morphology_and_distance(binary_img, kernel):
    cleaned_bin = opening(binary_img, kernel) 
    dist_map = distance_transform(cleaned_bin)
    return cleaned_bin, dist_map

def _bfs(r, c, peaks, markers, visited, label, h, w):
    queue = [(r, c)]
    visited[r, c] = True
    
    while queue:
        curr_r, curr_c = queue.pop(0)
        markers[curr_r, curr_c] = label
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr_r + dr, curr_c + dc
            
            if 0 <= nr < h and 0 <= nc < w:
                if peaks[nr, nc] == 255 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

def extract_and_label_markers(dist_map, threshold):
    h, w = dist_map.shape
    max_dist = np.max(dist_map)
    
    if max_dist == 0:
        return np.zeros((h, w), dtype=np.int32)
        
    peaks = np.where(dist_map > (max_dist * threshold), 255, 0).astype(np.uint8)
    
    markers = np.zeros((h, w), dtype=np.int32)
    visited = np.zeros((h, w), dtype=bool)
    label = 1
    
    for r in range(h):
        for c in range(w):
            if peaks[r, c] == 255 and not visited[r, c]:
                _bfs(r, c, peaks, markers, visited, label, h, w)
                label += 1
                
    return markers

def watershed(dist_map, markers):
    h, w = dist_map.shape
    labels = markers.copy()
    
    topo_surface = (np.max(dist_map) - dist_map).astype(np.int32)
    
    init_r, init_c = np.where(labels > 0)
    boundary_pixels = []
    in_queue = np.zeros((h, w), dtype=bool)
    
    for r, c in zip(init_r, init_c):
        in_queue[r, c] = True
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w:
                if labels[nr, nc] == 0 and not in_queue[nr, nc]:
                    in_queue[nr, nc] = True
                    boundary_pixels.append((topo_surface[nr, nc], nr, nc))
    
    boundary_pixels.sort(key=lambda x: x[0])
    
    while boundary_pixels:
        _, curr_r, curr_c = boundary_pixels.pop(0)
        
        neighbor_labels = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr_r + dr, curr_c + dc
            if 0 <= nr < h and 0 <= nc < w and labels[nr, nc] > 0:
                neighbor_labels.append(labels[nr, nc])
                
        if neighbor_labels:
            unique_labels = np.unique(neighbor_labels)
            if len(unique_labels) == 1:
                labels[curr_r, curr_c] = unique_labels[0]
            else:
                labels[curr_r, curr_c] = -1 
                
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr_r + dr, curr_c + dc
            if 0 <= nr < h and 0 <= nc < w:
                if labels[nr, nc] == 0 and not in_queue[nr, nc]:
                    in_queue[nr, nc] = True
                    item = (topo_surface[nr, nc], nr, nc)
                    
                    idx = 0
                    while idx < len(boundary_pixels) and boundary_pixels[idx][0] < item[0]:
                        idx += 1
                    boundary_pixels.insert(idx, item)
                    
    return labels

def generate_label_color_image(labels):
    h, w = labels.shape
    color_img = np.zeros((h, w, 3), dtype=np.uint8)
    
    np.random.seed(42)
    max_label = np.max(labels)
    
    colors = {0: [0, 0, 0], -1: [0, 0, 255]}  # -1 mapeado para Vermelho BGR
    for i in range(1, max_label + 1):
        colors[i] = list(np.random.randint(40, 240, size=3))
        
    for r in range(h):
        for c in range(w):
            lbl = labels[r, c]
            if lbl in colors:
                color_img[r, c] = colors[lbl]
            else:
                color_img[r, c] = [255, 255, 255]
                
    return color_img

def watershed_pipeline(binary_img, kernel_size, threshold_ratio):
    cleaned_bin, dist_map = preprocess_morphology_and_distance(binary_img, kernel_size)
    markers = extract_and_label_markers(dist_map, threshold_ratio)
    labels = watershed(dist_map, markers)
    colored_output = generate_label_color_image(labels)
    
    return cleaned_bin, dist_map, markers, labels, colored_output


# =========================================================================
# CONFIGURAÇÃO E MONTAGEM DO GRID DE PRODUTOS INTERMEDIÁRIOS
# =========================================================================

pasta_saida = "resultados_watershed_final"
os.makedirs(pasta_saida, exist_ok=True)

# 0. Carregar imagem original
img_bgr = cv2.imread('fotos/gatos.png')
if img_bgr is None:
    print("Erro: Verifique se sua imagem está em 'fotos'")
    exit()

gray = (0.114 * img_bgr[:,:,0] + 0.587 * img_bgr[:,:,1] + 0.299 * img_bgr[:,:,2]).astype(np.uint8)

# 1. Threshold
img_threshold = np.zeros_like(gray)
img_threshold[gray < 130] = 255 

# 2. Closing de pré-processamento conforme sua rotina estrutural
img_closed = closing(img_threshold, kernel_size=5)

# Execução do seu pipeline unificado
kernel_param = 5
threshold_param = 0.4
cleaned_bin, dist_map, markers, labels, colored_output = watershed_pipeline(
    img_closed, 
    kernel_size=kernel_param, 
    threshold_ratio=threshold_param
)

# Engenharia de normalização visual para exibição uniforme
dist_norm = ((dist_map - np.min(dist_map)) / (np.max(dist_map) - np.min(dist_map)) * 255).astype(np.uint8)
markers_norm = np.where(markers > 0, 255, 0).astype(np.uint8)

# Gerando o "Local Maximum" isolado a partir do threshold multiplicador direto
img_local_maximum = np.zeros_like(gray)
img_local_maximum[dist_map > (np.max(dist_map) * threshold_param)] = 255

# Criando "Segmented - Gray" baseado nos labels numéricos estáveis
max_lbl = np.max(labels)
img_segmented_gray = np.zeros_like(gray)
for i in range(1, max_lbl + 1):
    tom = int(i * (230 / (max_lbl + 1)))
    img_segmented_gray[labels == i] = tom
img_segmented_gray[labels == -1] = 255  # Borda divisória branca

# Criando a imagem final do Output (Original com linhas divisórias em vermelho engrossadas)
img_output = img_bgr.copy()
# Engrossamento simples das bordas para correta amostragem visual no grid
borda_mask = np.zeros_like(gray)
borda_mask[labels == -1] = 255
borda_mask_grossa = dilatar_manual(borda_mask, iteracoes=1)
img_output[borda_mask_grossa == 255] = [0, 0, 255]  # Vermelho Puro BGR

# Aplica contorno no Segmented - Color original
img_segmented_color_rgb = cv2.cvtColor(colored_output, cv2.COLOR_BGR2RGB)
img_segmented_color_rgb[borda_mask_grossa == 255] = [255, 255, 255]


# =========================================================================
# EXIBIÇÃO EM GRID 3x3 EXATAMENTE COMO SOLICITADO NO ENUNCIADO
# =========================================================================
fig, axs = plt.subplots(3, 3, figsize=(15, 13))

img_rgb_original = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
img_rgb_output = cv2.cvtColor(img_output, cv2.COLOR_BGR2RGB)

# Linha 1
axs[0, 0].imshow(img_rgb_original); axs[0, 0].set_title("Original image", fontsize=14, weight='bold'); axs[0, 0].axis("off")
axs[0, 1].imshow(img_threshold, cmap='gray'); axs[0, 1].set_title("Threshold", fontsize=14, weight='bold'); axs[0, 1].axis("off")
axs[0, 2].imshow(img_closed, cmap='gray'); axs[0, 2].set_title("Closing", fontsize=14, weight='bold'); axs[0, 2].axis("off")

# Linha 2
axs[1, 0].imshow(dist_norm, cmap='gray'); axs[1, 0].set_title("Distance transform", fontsize=14, weight='bold'); axs[1, 0].axis("off")
axs[1, 1].imshow(img_local_maximum, cmap='gray'); axs[1, 1].set_title("Local maximum", fontsize=14, weight='bold'); axs[1, 1].axis("off")
axs[1, 2].imshow(markers_norm, cmap='gray'); axs[1, 2].set_title("Markers", fontsize=14, weight='bold'); axs[1, 2].axis("off")

# Linha 3
axs[2, 0].imshow(img_segmented_gray, cmap='gray'); axs[2, 0].set_title("Segmented - gray", fontsize=14, weight='bold'); axs[2, 0].axis("off")
axs[2, 1].imshow(img_segmented_color_rgb); axs[2, 1].set_title("Segmented - color", fontsize=14, weight='bold'); axs[2, 1].axis("off")
axs[2, 2].imshow(img_rgb_output); axs[2, 2].set_title("Output image", fontsize=14, weight='bold'); axs[2, 2].axis("off")

plt.tight_layout()

caminho_mosaico = os.path.join(pasta_saida, "mosaico_aluno_final_3x3.png")
plt.savefig(caminho_mosaico, dpi=300, bbox_inches='tight')
plt.show()

print(f"\n[Sucesso] Pipeline atualizado com sua base. Resultado salvo em: '{caminho_mosaico}'")
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# =========================================================================
# FUNÇÕES DA BASE DO ALUNO (CONVOLUÇÃO, GAUSSIANO, SOBEL, HOG)
# =========================================================================

def convolution(img_gray, kernel):
    h, w = img_gray.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    
    kernel_flipped = kernel[::-1, ::-1]
    
    padded = np.pad(img_gray, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    out = np.zeros_like(img_gray, dtype=np.float32)
    
    for y in range(h):
        for x in range(w):
            window = padded[y:y + kh, x:x + kw]
            out[y, x] = np.sum(window * kernel_flipped)
            
    return out

def gaussian_kernel(size, sigma):
    ax = np.linspace(-(size // 2), size // 2, size)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2.0 * sigma**2))
    return kernel / np.sum(kernel)

def sobel(img_blur):
    sobel_x = np.array([[-1, 0, 1], 
                        [-2, 0, 2], 
                        [-1, 0, 1]], dtype=np.float32)
    
    sobel_y = np.array([[-1, -2, -1], 
                        [ 0,  0,  0], 
                        [ 1,  2,  1]], dtype=np.float32)
    
    gx = convolution(img_blur, sobel_x)
    gy = convolution(img_blur, sobel_y)
    
    magnitude = np.sqrt(gx**2 + gy**2)
    orientation = np.arctan2(gy, gx)
    
    return magnitude, orientation

def hog(magnitude, orientation, cell_size=8, num_bins=9):
    h, w = magnitude.shape
    num_cells_y = h // cell_size
    num_cells_x = w // cell_size
    
    hog_cells = np.zeros((num_cells_y, num_cells_x, num_bins), dtype=np.float32)
    
    orientation_deg = np.degrees(orientation) % 180
    bin_width = 180.0 / num_bins
    
    for cy in range(num_cells_y):
        for cx in range(num_cells_x):
            mag_tile = magnitude[cy*cell_size:(cy+1)*cell_size, cx*cell_size:(cx+1)*cell_size]
            ang_tile = orientation_deg[cy*cell_size:(cy+1)*cell_size, cx*cell_size:(cx+1)*cell_size]
            
            for y in range(cell_size):
                for x in range(cell_size):
                    pix_mag = mag_tile[y, x]
                    pix_ang = ang_tile[y, x]
                    
                    if pix_mag > 150.0:
                        bin_idx = int(pix_ang // bin_width) % num_bins
                        hog_cells[cy, cx, bin_idx] += pix_mag

    centers_x = []
    centers_y = []
    u_dirs = []
    v_dirs = []
    lengths = []
    
    half_cell = cell_size / 2.0
    bins_angles = np.linspace(0, np.pi, num_bins, endpoint=False) + (np.pi / (2 * num_bins))
    
    for cy in range(num_cells_y):
        for cx in range(num_cells_x):
            hist = hog_cells[cy, cx, :]
            
            max_val = np.max(hist)
            if max_val == 0:
                continue
            
            max_bin = np.argmax(hist)
            angle = bins_angles[max_bin]

            center_y = cy * cell_size + half_cell
            center_x = cx * cell_size + half_cell

            centers_x.append(center_x)
            centers_y.append(center_y)

            u_dirs.append(np.cos(angle))
            v_dirs.append(np.sin(angle))
            lengths.append(max_val)

    if len(lengths) == 0:
        return (np.array([]), np.array([]), np.array([]), np.array([]), np.array([]))

    lengths = np.array(lengths, dtype=np.float32)
    lengths = (lengths / (np.max(lengths) + 1e-9)) * (cell_size * 0.9)

    return (np.array(centers_x), np.array(centers_y), np.array(u_dirs), np.array(v_dirs), lengths)

def process_canny_and_hog(img_gray, gaussian_size=5, sigma=1.4, cell_size=8, num_bins=9):
    kernel_g = gaussian_kernel(gaussian_size, sigma)
    blurred = convolution(img_gray, kernel_g)
    magnitude, orientation = sobel(blurred)
    hog_vectors = hog(magnitude, orientation, cell_size, num_bins)
    
    return blurred, magnitude, hog_vectors


# =========================================================================
# PIPELINE DE EXECUÇÃO PRINCIPAL
# =========================================================================

os.makedirs("resultados/canny_hog", exist_ok=True)

# 1. Carregar imagem do tema
img_bgr = cv2.imread("fotos/coruja.png")
if img_bgr is None:
    print("Erro: Imagem não encontrada.")
    exit()

# Conversão manual para escala de cinza por luminância
img_cinza = (0.114 * img_bgr[:, :, 0] + 0.587 * img_bgr[:, :, 1] + 0.299 * img_bgr[:, :, 2]).astype(np.uint8)

# Ajuste dinâmico para garantir dimensões múltiplas de 8 (evitando quebras nas bordas do HOG)
h, w = img_cinza.shape
h_novo, w_novo = (h // 8) * 8, (w // 8) * 8
img_cinza = img_cinza[:h_novo, :w_novo]

print("Processando pipeline Canny & HOG com as funções base...")
# Executa a função principal do seu bloco de código
img_suave, magnitude, (cx, cy, u, v, lengths) = process_canny_and_hog(img_cinza, gaussian_size=5, sigma=1.4, cell_size=8, num_bins=9)

# Normalização puramente visual das imagens para salvaguardar no disco
img_suave_visual = np.clip(img_suave, 0, 255).astype(np.uint8)
magnitude_visual = np.clip(magnitude, 0, 255).astype(np.uint8)

cv2.imwrite("resultados/canny_hog/1_suavizada_base.png", img_suave_visual)
cv2.imwrite("resultados/canny_hog/2_magnitude_base.png", magnitude_visual)

print(f"-> Sucesso! Total de orientações HOG válidas a renderizar: {len(cx)}")
# =========================================================================
# EXIBIÇÃO DOS RESULTADOS VISUAIS (CINZA -> BLUR -> SOBEL -> HOG)
# =========================================================================
plt.figure(figsize=(20, 5))

# Painel 1: Imagem Original Cinza
plt.subplot(1, 4, 1)
plt.imshow(img_cinza, cmap='gray')
plt.title("Original (Tons de Cinza)", fontsize=12)
plt.axis("off")

# Painel 2: Imagem Suavizada (Blur)
plt.subplot(1, 4, 2)
plt.imshow(img_suave_visual, cmap='gray')
plt.title("Imagem Suavizada (Gaussian)", fontsize=12)
plt.axis("off")

# Painel 3: Magnitude do Gradiente (Sobel)
plt.subplot(1, 4, 3)
plt.imshow(magnitude_visual, cmap='gray')
plt.title("Magnitude do Gradiente", fontsize=12)
plt.axis("off")

# Painel 4: HOG refinado sobre fundo preto
plt.subplot(1, 4, 4)
fundo_preto = np.zeros_like(img_cinza)
plt.imshow(fundo_preto, cmap='gray')

if len(cx) > 0:
    quiver_u = u * lengths
    quiver_v = v * lengths
    plt.quiver(cx, cy, quiver_u, quiver_v,
               color='white',
               angles='xy',
               scale_units='xy',
               scale=1,
               pivot='mid',
               linewidths=0.8,
               width=0.003,
               antialiased=True)

plt.title("Refined HOG Visualisation", fontsize=12)
plt.axis("off")

plt.tight_layout()
plt.savefig("resultados/canny_hog/resultado_unificado_base.png", dpi=300, bbox_inches='tight')
plt.savefig("resultados/canny_hog/steps_sequence.png", dpi=300, bbox_inches='tight')
plt.show()

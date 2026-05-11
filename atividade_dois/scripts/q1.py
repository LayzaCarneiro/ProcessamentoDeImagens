import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================================================
# QUESTÃO 1 - Aplicar filtros h1 até h11
# Convolução manual em imagem monocromática
# ==================================================


# -------------------------
# 1. Converter imagem para cinza
# -------------------------

def to_gray_manual(img):
    altura, largura, _ = img.shape
    gray = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]

            valor = int(0.299*r + 0.587*g + 0.114*b)

            if valor > 255:
                valor = 255

            gray[y, x] = valor

    return gray


# -------------------------
# 2. Convolução manual
# -------------------------

def convolution(img, kernel):
    altura, largura = img.shape
    k_altura, k_largura = kernel.shape

    # centro da máscara (offset)
    offset_y = k_altura // 2
    offset_x = k_largura // 2

    padded = np.zeros(
        (altura + 2 * offset_y, largura + 2 * offset_x),
        dtype=np.uint8
    )

    for y in range(altura):
        for x in range(largura):
            padded[y + offset_y, x + offset_x] = img[y, x]

    # Matriz resultado
    output = np.zeros((altura, largura), dtype=np.float32)

    # Percorrendo pixel a pixel
    for y in range(altura):
        print(f"Linha {y+1}/{altura}", end="\r")

        for x in range(largura):
            soma = 0.0

            # Percorrendo o kernel
            for ky in range(k_altura):
                for kx in range(k_largura):
                    pixel = padded[y + ky, x + kx]
                    peso = kernel[ky, kx]
                    soma += pixel * peso

            # Valor absoluto para destacar bordas
            output[y, x] = abs(soma)

    # Travando entre 0 e 255
    final_result = np.clip(output, 0, 255).astype(np.uint8)
    return final_result


# -------------------------
# 3. Definir filtros
# -------------------------

filtros = {}

# h1 : Realce de bordas (Sharpen / Laplacian variant)
filtros['h1'] = np.array([
    [0, 0, -1, 0, 0],
    [0, -1, -2, -1, 0],
    [-1, -2, 16, -2, -1],
    [0, -1, -2, -1, 0],
    [0, 0, -1, 0, 0]
], dtype=np.float32)

# h2 : Suavização Gaussiana (Blur) - Normalizado por 1/256
filtros['h2'] = np.array([
    [1, 4, 6, 4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1, 4, 6, 4, 1]
], dtype=np.float32) / 256.0

# h3 : Detector de bordas verticais (Sobel Horizontal)
filtros['h3'] = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
], dtype=np.float32)

# h4 : Detector de bordas horizontais (Sobel Vertical)
filtros['h4'] = np.array([
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
], dtype=np.float32)

# h5 : Filtro Passa-Altas (Laplaciano clássico 3x3)
filtros['h5'] = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1]
], dtype=np.float32)

# h6 : Filtro de Média Simples (Box Blur) - Normalizado por 1/9
filtros['h6'] = np.array([
    [1,1,1],
    [1,1,1],
    [1,1,1]
], dtype=np.float32) / 9.0

# h7 : Realce direcional
filtros['h7'] = np.array([
    [-1,-1,2],
    [-1,2,-1],
    [2,-1,-1]
], dtype=np.float32)

# h8 : Realce direcional (diagonal oposta)
filtros['h8'] = np.array([
    [2,-1,-1],
    [-1,2,-1],
    [-1,-1,2]
], dtype=np.float32)

# h9 : Motion Blur (Desfoque de movimento na diagonal) - 9x9 normalizado por 1/9
filtros['h9'] = np.array([
    [1,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,1]
], dtype=np.float32) / 9.0

# h10 : Filtro Híbrido (Realce com suporte estendido) - Normalizado por 1/8
filtros['h10'] = np.array([
    [-1,-1,-1,-1,-1],
    [-1,2,2,2,-1],
    [-1,2,8,2,-1],
    [-1,2,2,2,-1],
    [-1,-1,-1,-1,-1]
], dtype=np.float32) / 8.0

# h11 : Realce diagonal
filtros['h11'] = np.array([
    [-1,-1,0],
    [-1,0,1],
    [0,1,1]
], dtype=np.float32)


# -------------------------
# 4. Carregar imagem
# -------------------------

img = cv2.imread("fotos/sphynx.png")
print("Imagem carregada!")
gray = to_gray_manual(img)


# -------------------------
# 5. Aplicar filtros
# -------------------------

resultados = []
titulos = []

resultados.append(gray)
titulos.append("Original Cinza")


# cria pasta resultados/filtros
os.makedirs("resultados/filtros", exist_ok=True)

for nome in filtros:
    print(f"\nAplicando {nome}...")
    img_filtrada = convolution(gray, filtros[nome])
    resultados.append(img_filtrada)
    titulos.append(nome)
       
    # salva imagem com filtro aplicado
    caminho = f"resultados/filtros/sphynx-{nome}.png"
    cv2.imwrite(caminho, img_filtrada)
    print(f"Salvo: {caminho}")


# -------------------------
# 6. Mostrar resultados
# -------------------------

plt.figure(figsize=(16, 10))

for i in range(len(resultados)):
    plt.subplot(3, 4, i+1)
    plt.imshow(resultados[i], cmap="gray", vmin=0, vmax=255)
    plt.title(titulos[i])
    plt.axis("off")

plt.tight_layout()
plt.show()


# -------------------------
# 7. Salvar
# -------------------------

os.makedirs("resultados", exist_ok=True)
plt.figure(figsize=(16, 10))

for i in range(len(resultados)):
    plt.subplot(3, 4, i+1)
    plt.imshow(resultados[i], cmap="gray", vmin=0, vmax=255)
    plt.title(titulos[i])
    plt.axis("off")

plt.tight_layout()
plt.savefig("resultados/sphynx_todos_filtros.png", dpi=300, bbox_inches="tight")
print("\nResultados salvo em resultados")
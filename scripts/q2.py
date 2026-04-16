import cv2
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# 1. Conversão para cinza + normalização [0,1]
# -------------------------

def to_gray_and_normalize(img):
    altura, largura, _ = img.shape

    # matriz float para [0,1]
    norm = np.zeros((altura, largura), dtype=np.float64)

    print(f"Processando imagem de {largura}x{altura}...")
    print("Convertendo para cinza e normalizando...")

    for y in range(altura):
        for x in range(largura):

            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]

            # cinza manual
            pixel_cinza = int(0.299*r + 0.587*g + 0.114*b)

            if pixel_cinza > 255:
                pixel_cinza = 255

            # normalização
            norm[y, x] = pixel_cinza / 255.0

    return norm


# -------------------------
# 2. Correção gama manual
# -------------------------

def apply_gamma(norm_img, gamma):
    altura, largura = norm_img.shape

    # saída já em [0,255]
    output = np.zeros((altura, largura), dtype=np.uint8)

    print(f"Aplicando gamma = {gamma}...")

    for y in range(altura):
        for x in range(largura):

            A = norm_img[y, x]

            # equação principal
            B = A ** (1.0 / gamma)

            # voltando para [0,255]
            novo_pixel = int(B * 255)

            if novo_pixel > 255:
                novo_pixel = 255

            if novo_pixel < 0:
                novo_pixel = 0

            output[y, x] = novo_pixel

    return output


# -------------------------
# Carregar imagem
# -------------------------

img = cv2.imread('fotos/macaco.png')

print("Imagem carregada!")

# -------------------------
# Pipeline
# -------------------------

norm = to_gray_and_normalize(img)

valores_gamma = [0.5, 1.5, 2.5, 3.5]

imagens = []
titulos = []

# original
gray_original = (norm * 255).astype(np.uint8)

imagens.append(gray_original)
titulos.append("Original")

# normalizada
imagens.append(norm)
titulos.append("Normalizada [0,1]")

# aplicar gamas
for g in valores_gamma:
    resultado = apply_gamma(norm, g)

    imagens.append(resultado)
    titulos.append(f"Gamma = {g}")


# -------------------------
# Exibição
# -------------------------

plt.figure(figsize=(14,6))

for i in range(len(imagens)):

    plt.subplot(2, 3, i+1)

    # imagem normalizada
    if imagens[i].dtype == np.float64:
        plt.imshow(imagens[i], cmap='gray', vmin=0.0, vmax=1.0)
    else:
        plt.imshow(imagens[i], cmap='gray', vmin=0, vmax=255)

    plt.title(titulos[i])
    plt.axis("off")

plt.tight_layout()
plt.show()
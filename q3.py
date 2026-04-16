import cv2
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# 1. Conversão manual para cinza
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
# 2. Combinação ponderada manual
# -------------------------

def weighted_sum(imgA, imgB, wA, wB):
    altura, largura = imgA.shape

    result = np.zeros((altura, largura), dtype=np.uint8)

    print(f"Combinando imagens com pesos {wA} e {wB}...")

    for y in range(altura):
        for x in range(largura):

            A = float(imgA[y, x])
            B = float(imgB[y, x])

            valor = (wA * A) + (wB * B)

            if valor > 255:
                valor = 255
            if valor < 0:
                valor = 0

            result[y, x] = int(valor)

    return result


# -------------------------
# Carregar imagens
# -------------------------

img_lua = cv2.imread('fotos/macaco.png')
img_titan = cv2.imread('fotos/medelin.jpg')

print("Imagens carregadas!")

# -------------------------
# Pipeline
# -------------------------

gray_A = to_gray_manual(img_lua)
gray_B = to_gray_manual(img_titan)

# garantir mesmo tamanho
altura, largura = gray_A.shape
gray_B = cv2.resize(gray_B, (largura, altura))

# combinações
img_c = weighted_sum(gray_A, gray_B, 0.2, 0.8)
img_d = weighted_sum(gray_A, gray_B, 0.5, 0.5)
img_e = weighted_sum(gray_A, gray_B, 0.8, 0.2)


# -------------------------
# Exibição
# -------------------------

plt.figure(figsize=(15,5))

plt.subplot(1,5,1)
plt.imshow(gray_A, cmap="gray")
plt.title("Imagem A")
plt.axis("off")

plt.subplot(1,5,2)
plt.imshow(gray_B, cmap="gray")
plt.title("Imagem B")
plt.axis("off")

plt.subplot(1,5,3)
plt.imshow(img_c, cmap="gray")
plt.title("0.2A + 0.8B")
plt.axis("off")

plt.subplot(1,5,4)
plt.imshow(img_d, cmap="gray")
plt.title("0.5A + 0.5B")
plt.axis("off")

plt.subplot(1,5,5)
plt.imshow(img_e, cmap="gray")
plt.title("0.8A + 0.2B")
plt.axis("off")

plt.tight_layout()
plt.show()
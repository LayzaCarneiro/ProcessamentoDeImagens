import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import os

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
# 2. Kernel gaussiano manual
# -------------------------

def gaussian_kernel(size, sigma):
    offset = size // 2
    kernel = np.zeros((size, size), dtype=np.float32)
    soma = 0.0

    for y in range(-offset, offset + 1):
        for x in range(-offset, offset + 1):

            termo1 = 1 / (2 * math.pi * sigma**2)
            termo2 = math.exp(-(x**2 + y**2) / (2 * sigma**2))
            valor = termo1 * termo2

            kernel[y + offset, x + offset] = valor
            soma += valor

    # normalização
    for i in range(size):
        for j in range(size):
            kernel[i, j] /= soma

    return kernel


# -------------------------
# 3. Convolução manual COM padding
# -------------------------

def convolution(img, kernel):
    altura, largura = img.shape
    ksize = kernel.shape[0]
    offset = ksize // 2

    # padding manual (borda preta)
    padded = np.zeros((altura + 2*offset, largura + 2*offset), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):
            padded[y + offset, x + offset] = img[y, x]

    output = np.zeros((altura, largura), dtype=np.float32)

    for y in range(altura):

        if y % 10 == 0:
            print(f"Processando linha {y}/{altura}...")

        for x in range(largura):

            soma_pixel = 0.0

            for ky in range(ksize):
                for kx in range(ksize):

                    pixel = padded[y + ky, x + kx]
                    peso = kernel[ky, kx]

                    soma_pixel += pixel * peso

            output[y, x] = soma_pixel

    return output.astype(np.uint8)


# -------------------------
# 4. Efeito lápis (divisão manual)
# -------------------------

def pencil_effect(gray, blurred):
    altura, largura = gray.shape
    result = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):

            g = int(gray[y, x])
            b = int(blurred[y, x])

            if b == 0:
                novo = 255
            else:
                valor = (g * 255) / b

                if valor > 255:
                    novo = 255
                else:
                    novo = int(valor)

            result[y, x] = novo

    return result


# -------------------------
# Carregar imagem
# -------------------------

img = cv2.imread("fotos/onca_natureza.jpg")
cv2.imwrite("fotos/animal.png", img)
print("Imagem carregada!")

# -------------------------
# Redimensiona para tamanho padrão
# -------------------------
def resize_proporcional(img, tamanho_max=512):
    altura, largura, _ = img.shape

    if altura > largura:
        nova_altura = tamanho_max
        nova_largura = int(largura * (tamanho_max / altura))
    else:
        nova_largura = tamanho_max
        nova_altura = int(altura * (tamanho_max / largura))

    img_redimensionada = cv2.resize(img, (nova_largura, nova_altura))

    return img_redimensionada

img = resize_proporcional(img)
print("Imagem redimensionada para tamanho padrão!")


# -------------------------
# Pipeline
# -------------------------

gray = to_gray_manual(img)

kernel = gaussian_kernel(21, 3.0)

blurred = convolution(gray, kernel)

sketch = pencil_effect(gray, blurred)

# -------------------------
# Salvar automaticamente
# -------------------------

os.makedirs("resultados", exist_ok=True)

caminho = "resultados/questao_um.png"
cv2.imwrite(caminho, sketch)

print(f"Imagem salva em: {caminho}")


# -------------------------
# Mostrar imagens
# -------------------------

plt.figure(figsize=(12,4))

plt.subplot(1,4,1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original")
plt.axis("off")

plt.subplot(1,4,2)
plt.imshow(gray, cmap="gray")
plt.title("Cinza (manual)")
plt.axis("off")

plt.subplot(1,4,3)
plt.imshow(blurred, cmap="gray")
plt.title("Gaussiano (manual)")
plt.axis("off")

plt.subplot(1,4,4)
plt.imshow(sketch, cmap="gray")
plt.title("Lápis")
plt.axis("off")

plt.show()
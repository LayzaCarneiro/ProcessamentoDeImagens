import cv2
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# 1. Converter para cinza
# -------------------------

def to_gray_manual(img):
    altura, largura, _ = img.shape
    gray = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):

            b, g, r = img[y, x]

            valor = int(0.299*r + 0.587*g + 0.114*b)

            if valor > 255:
                valor = 255

            gray[y, x] = valor

    return gray


# -------------------------
# 2. Quantização manual
# -------------------------

def quantize_image(img, niveis):
    altura, largura = img.shape
    result = np.zeros((altura, largura), dtype=np.uint8)

    print(f"Quantizando para {niveis} níveis...")

    passo = int(256 / niveis)

    # fator de expansão para ocupar [0,255]
    escala = 255 / (256 - passo)

    for y in range(altura):
        for x in range(largura):

            valor = img[y, x]

            # quantização padrão
            q = int(valor / passo) * passo

            # expansão de contraste (ESSENCIAL)
            novo_valor = int(q * escala)

            if novo_valor > 255:
                novo_valor = 255

            result[y, x] = novo_valor

    return result

# -------------------------
# Carregar imagem
# -------------------------

img = cv2.imread('fotos/macaco.png')

print("Imagem carregada!")

# -------------------------
# Pipeline
# -------------------------

img_gray = to_gray_manual(img)

# níveis de quantização
niveis_lista = [64, 32, 16, 8, 4, 2]

imagens = []
titulos = []

# original
imagens.append(img_gray)
titulos.append("(a) 256 níveis (8-bit)")

# quantizações
for n in niveis_lista:
    img_q = quantize_image(img_gray, n)

    imagens.append(img_q)
    titulos.append(f"{n} níveis")

# -------------------------
# Exibição
# -------------------------

plt.figure(figsize=(18,5))

for i in range(len(imagens)):
    plt.subplot(1, len(imagens), i+1)
    plt.imshow(imagens[i], cmap="gray", vmin=0, vmax=255)
    plt.title(titulos[i])
    plt.axis("off")

plt.tight_layout()
plt.show()


# -------------------------
# Mostrar resultado
# -------------------------

plt.figure(figsize=(18,5))

for i in range(len(imagens)):
    plt.subplot(1, len(imagens), i+1)
    plt.imshow(imagens[i], cmap="gray", vmin=0, vmax=255)
    plt.title(titulos[i])
    plt.axis("off")

plt.tight_layout()
plt.savefig("resultados/teste/img_quantizada.png", dpi=300, bbox_inches='tight')
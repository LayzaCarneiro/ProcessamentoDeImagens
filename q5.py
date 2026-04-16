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

            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]

            valor = int(0.299*r + 0.587*g + 0.114*b)

            if valor > 255:
                valor = 255

            gray[y, x] = valor

    return gray


# -------------------------
# 2. Ajustar tamanho (múltiplo de 4)
# -------------------------

def crop_to_multiple_of_4(img):
    altura, largura = img.shape

    nova_altura = (altura // 4) * 4
    nova_largura = (largura // 4) * 4

    return img[0:nova_altura, 0:nova_largura]


# -------------------------
# 3. Construir mosaico 4x4
# -------------------------

def build_mosaic(img, ordem):
    altura, largura = img.shape

    altura_bloco = altura // 4
    largura_bloco = largura // 4

    result = np.zeros((altura, largura), dtype=np.uint8)

    print("Montando mosaico 4x4...")

    for lin_dest in range(4):
        for col_dest in range(4):

            # número do bloco de origem
            num = ordem[lin_dest, col_dest]

            # converter para coordenadas (linha, coluna)
            lin_ori = (num - 1) // 4
            col_ori = (num - 1) % 4

            # coordenadas origem
            y1o = lin_ori * altura_bloco
            y2o = y1o + altura_bloco

            x1o = col_ori * largura_bloco
            x2o = x1o + largura_bloco

            # coordenadas destino
            y1d = lin_dest * altura_bloco
            y2d = y1d + altura_bloco

            x1d = col_dest * largura_bloco
            x2d = x1d + largura_bloco

            # copiar bloco
            result[y1d:y2d, x1d:x2d] = img[y1o:y2o, x1o:x2o]

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

img_crop = crop_to_multiple_of_4(img_gray)

# ordem da questão (c)
ordem_blocos = np.array([
    [6, 11, 13, 3],
    [8, 16, 1, 9],
    [12, 14, 2, 7],
    [4, 15, 10, 5]
])

img_mosaico = build_mosaic(img_crop, ordem_blocos)

# -------------------------
# Exibição
# -------------------------

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.imshow(img_crop, cmap="gray")
plt.title("Original (ajustada)")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(img_mosaico, cmap="gray")
plt.title("Mosaico 4x4")
plt.axis("off")

plt.tight_layout()
plt.show()


# -------------------------
# Salvar resultado
# -------------------------

# cv2.imwrite('mosaico.jpg', img_mosaico)
# print("Imagem salva com sucesso!")
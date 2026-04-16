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

    # Ajusta dimensões para múltiplos de 4
    nova_altura = (altura // 4) * 4
    nova_largura = (largura // 4) * 4

    # Recorta a imagem
    return img[0:nova_altura, 0:nova_largura]


# -------------------------
# 3. Construir mosaico 4x4
# -------------------------

def build_mosaic(img, ordem):
    altura, largura = img.shape

    # Define tamanho de cada bloco
    altura_bloco = altura // 4
    largura_bloco = largura // 4

    # Imagem de saída
    result = np.zeros((altura, largura), dtype=np.uint8)

    print("Montando mosaico 4x4...")

    # Percorre cada posição do mosaico
    for lin_dest in range(4):
        for col_dest in range(4):

            # Número do bloco na matriz de ordem
            num = ordem[lin_dest, col_dest]

            # Converte número do bloco em posição (linha, coluna)
            lin_ori = (num - 1) // 4
            col_ori = (num - 1) % 4

            # Coordenadas do bloco original
            y1o = lin_ori * altura_bloco
            y2o = y1o + altura_bloco
            x1o = col_ori * largura_bloco
            x2o = x1o + largura_bloco

            # Coordenadas de destino
            y1d = lin_dest * altura_bloco
            y2d = y1d + altura_bloco
            x1d = col_dest * largura_bloco
            x2d = x1d + largura_bloco

            # Copia o bloco da origem para o destino
            result[y1d:y2d, x1d:x2d] = img[y1o:y2o, x1o:x2o]

    return result


# -------------------------
# 4. Redimensionamento proporcional
# -------------------------

def resize_proporcional(img, tamanho_max=512):
    altura, largura, _ = img.shape

    # Mantém proporção original
    if altura > largura:
        nova_altura = tamanho_max
        nova_largura = int(largura * (tamanho_max / altura))
    else:
        nova_largura = tamanho_max
        nova_altura = int(altura * (tamanho_max / largura))

    return cv2.resize(img, (nova_largura, nova_altura))


# -------------------------
# Carregar imagem
# -------------------------

img = cv2.imread('fotos/cachorro.jpg')
print("Imagem carregada!")

# Redimensionamento para melhorar desempenho
img = resize_proporcional(img)
print("Imagem redimensionada!")


# -------------------------
# Pipeline
# -------------------------

# Conversão para cinza
img_gray = to_gray_manual(img)

# Ajuste para múltiplos de 4
img_crop = crop_to_multiple_of_4(img_gray)

# Ordem dos blocos (definida no exercício)
ordem_blocos = np.array([
    [6, 11, 13, 3],
    [8, 16, 1, 9],
    [12, 14, 2, 7],
    [4, 15, 10, 5]
])

# Construção do mosaico
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
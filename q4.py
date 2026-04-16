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
# 2. Negativo
# -------------------------

def negative(img):
    altura, largura = img.shape
    result = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):

            r = img[y, x]
            s = 255 - r

            result[y, x] = s

    return result


# -------------------------
# 3. Ajuste para intervalo [100,200]
# -------------------------

def adjust_interval(img):
    altura, largura = img.shape
    result = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):

            r = img[y, x]

            # transformação linear
            s = (r / 255.0) * 100.0 + 100.0

            if s > 200: s = 200
            if s < 100: s = 100

            result[y, x] = int(s)

    return result


def contraste_agressivo(img):
    altura, largura = img.shape
    result = np.zeros((altura, largura), dtype=np.uint8)

    # 1. Definir os limiares de 'escuro' e 'claro' que queremos transformar.
    # Estes valores (70 e 200) são estimativas baseadas na imagem (a).
    # Tudo abaixo de r_min virará preto (0).
    # Tudo acima de r_max virará branco (255).
    r_min = 100.0
    r_max = 200.0

    # Evitar divisão por zero se a imagem for plana
    if r_max == r_min:
        return img

    for y in range(altura):
        for x in range(largura):
            r = img[y, x]

            # 2. Aplicar a transformação linear de expansão na faixa intermediária.
            # A fórmula expande a faixa [r_min, r_max] para o intervalo [0, 255].
            s = ( (r - r_min) / (r_max - r_min) ) * 255.0

            # 3. Importante: Limitar os resultados (clipping) para garantir que
            # fiquem dentro do intervalo de imagem [0, 255].
            if s > 255:
                s = 255
            if s < 0:
                s = 0

            # 4. Converter para inteiro e salvar
            result[y, x] = int(s)

    return result



# -------------------------
# 4. Inverter linhas pares
# -------------------------

def invert_even_rows(img):
    altura, largura = img.shape
    result = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):

            if y % 2 == 0:
                x_inv = (largura - 1) - x
                result[y, x_inv] = img[y, x]
            else:
                result[y, x] = img[y, x]

    return result


# -------------------------
# 5. Espelhamento top-down
# -------------------------

def mirror_top_down(img):
    altura, largura = img.shape
    result = np.zeros((altura, largura), dtype=np.uint8)

    metade = altura // 2

    for y in range(altura):
        for x in range(largura):

            if y < metade:
                result[y, x] = img[y, x]
            else:
                y_origem = (altura - 1) - y
                result[y, x] = img[y_origem, x]

    return result


# -------------------------
# 6. Flip vertical total
# -------------------------

def flip_vertical(img):
    altura, largura = img.shape
    result = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):

            y_inv = (altura - 1) - y
            result[y_inv, x] = img[y, x]

    return result


# -------------------------
# Carregar imagem
# -------------------------

img = cv2.imread('fotos/rua.png')

print("Imagem carregada!")

# -------------------------
# Pipeline
# -------------------------

img_a = to_gray_manual(img)
img_b = negative(img_a)
img_c = contraste_agressivo(img_a)
img_d = invert_even_rows(img_a)
img_e = mirror_top_down(img_a)
img_f = flip_vertical(img_a)

# -------------------------
# Exibição
# -------------------------

imagens = [img_a, img_b, img_c, img_d, img_e, img_f]
titulos = [
    "(a) Cinza",
    "(b) Negativo",
    "(c) [100,200]",
    "(d) Linhas pares invertidas",
    "(e) Espelho top-down",
    "(f) Flip vertical"
]

plt.figure(figsize=(12,8))

for i in range(6):
    plt.subplot(2,3,i+1)
    plt.imshow(imagens[i], cmap="gray", vmin=0, vmax=255)
    plt.title(titulos[i])
    plt.axis("off")

plt.tight_layout()
plt.show()
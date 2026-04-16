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

            # Inversão de intensidade
            s = 255 - r

            result[y, x] = s

    return result


# -------------------------
# 3. Ajuste para intervalo [100,200]
# -------------------------
def adjust_interval(img):
    altura, largura = img.shape
    result = np.zeros((altura, largura), dtype=np.uint8)

    # Limiares definidos empiricamente
    r_min = 100.0
    r_max = 200.0

    # Evitar divisão por zero se a imagem for plana
    if r_max == r_min:
        return img

    for y in range(altura):
        for x in range(largura):
            r = img[y, x]

            # Expansão de contraste na faixa intermediária
            s = ( (r - r_min) / (r_max - r_min) ) * 255.0

            # Clipping
            if s > 255:
                s = 255
            if s < 0:
                s = 0

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

            # Se a linha for par → espelha horizontalmente
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

            # Metade superior permanece igual
            if y < metade:
                result[y, x] = img[y, x]
            else:
                # Metade inferior espelha a superior
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

            # Inversão completa no eixo vertical
            y_inv = (altura - 1) - y
            result[y_inv, x] = img[y, x]

    return result

# -------------------------
# 7. Redimensionamento proporcional
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
# Carregar imagens
# -------------------------

img = cv2.imread('fotos/raposa_artico.jpg')
print("Imagem carregada!")

# Redimensionamento para melhorar desempenho
img = resize_proporcional(img)
print("Imagem redimensionada!")


# -------------------------
# Pipeline
# -------------------------

img_a = to_gray_manual(img)          # cinza
img_b = negative(img_a)              # negativo
img_c = adjust_interval(img_a)       # ajuste de intensidade
img_d = invert_even_rows(img_a)      # linhas pares invertidas
img_e = mirror_top_down(img_a)       # espelho superior/inferior
img_f = flip_vertical(img_a)         # flip total

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
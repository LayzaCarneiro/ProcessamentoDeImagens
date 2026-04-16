import cv2 # leitura e escrita de imagens
import numpy as np  # manipulação de matrizes
import matplotlib.pyplot as plt  # exibição de imagens

# -------------------------
# 1. Conversão para cinza + normalização [0,1]
# -------------------------

def to_gray_and_normalize(img):
    altura, largura, _ = img.shape

    # Cria uma matriz float (double) para armazenar valores entre 0 e 1
    norm = np.zeros((altura, largura), dtype=np.float64)

    print(f"Processando imagem de {largura}x{altura}...")
    print("Convertendo para cinza e normalizando...")

    # Percorre pixel a pixel
    for y in range(altura):
        for x in range(largura):

            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]

            # Conversão manual para escala de cinza (luminância)
            pixel_cinza = int(0.299*r + 0.587*g + 0.114*b)

            # Garantia de limite máximo
            if pixel_cinza > 255:
                pixel_cinza = 255

            # Normalização: traz o valor para o intervalo [0,1]
            norm[y, x] = pixel_cinza / 255.0

    return norm


# -------------------------
# 2. Correção gama manual
# -------------------------

def apply_gamma(norm_img, gamma):
    altura, largura = norm_img.shape

    # Imagem de saída já no formato padrão [0,255]
    output = np.zeros((altura, largura), dtype=np.uint8)

    print(f"Aplicando gamma = {gamma}...")

    for y in range(altura):
        for x in range(largura):

            # Pixel normalizado
            A = norm_img[y, x]

            # Aplicação da transformação gama:
            # B = A^(1/gamma)
            B = A ** (1.0 / gamma)

            # Retorno para escala [0,255]
            novo_pixel = int(B * 255)

            # Clipping de segurança
            if novo_pixel > 255:
                novo_pixel = 255
            if novo_pixel < 0:
                novo_pixel = 0

            output[y, x] = novo_pixel

    return output


# -------------------------
# 3. Redimensionamento proporcional
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

img = cv2.imread('fotos/vaca.jpg')
print("Imagem carregada!")

# Redimensionamento para melhorar desempenho
img = resize_proporcional(img)
print("Imagem redimensionada!")

# -------------------------
# Pipeline
# -------------------------

# Valores de gamma a serem testados
valores_gamma = [0.5, 1.5, 2.5, 3.5]

imagens = []
titulos = []

# Imagem original colorida
imagens.append(img)
titulos.append("Original")

# Conversão + normalização
norm = to_gray_and_normalize(img)

# Imagem normalizada
imagens.append(norm)
titulos.append("Normalizada [0,1]")

# Aplicação da correção gama para diferentes valores
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

    # Caso especial para imagem normalizada
    if len(imagens[i].shape) == 3:
        # imagem colorida (BGR → RGB)
        plt.imshow(cv2.cvtColor(imagens[i], cv2.COLOR_BGR2RGB))

    elif imagens[i].dtype == np.float64:
        # imagem normalizada
        plt.imshow(imagens[i], cmap='gray', vmin=0.0, vmax=1.0)

    else:
        # imagem em cinza [0,255]
        plt.imshow(imagens[i], cmap='gray', vmin=0, vmax=255)

    plt.title(titulos[i])
    plt.axis("off")

plt.tight_layout()
plt.show()
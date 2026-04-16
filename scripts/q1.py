import cv2  # leitura e escrita de imagens
import numpy as np  # manipulação de matrizes
import math  # funções matemáticas
import matplotlib.pyplot as plt  # exibição de imagens
import os  # manipulação de diretórios

# -------------------------
# 1. Conversão para cinza (manual)
# -------------------------

def to_gray_manual(img):
    # Obtém dimensões da imagem
    altura, largura, _ = img.shape

    # Cria matriz vazia para imagem em tons de cinza
    gray = np.zeros((altura, largura), dtype=np.uint8)

    # Percorre pixel a pixel
    for y in range(altura):
        for x in range(largura):

            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]

            # Fórmula da luminância
            value = int(0.299*r + 0.587*g + 0.114*b)

            # Garantia de limite
            if value > 255:
                value = 255

            gray[y, x] = value

    return gray


# -------------------------
# 2. Kernel gaussiano (manual)
# -------------------------

def gaussian_kernel(size, sigma):
    offset = size // 2
    kernel = np.zeros((size, size), dtype=np.float32)
    soma = 0.0

    # Construção do kernel usando fórmula Gaussiana
    for y in range(-offset, offset + 1):
        for x in range(-offset, offset + 1):

            termo1 = 1 / (2 * math.pi * sigma**2)
            termo2 = math.exp(-(x**2 + y**2) / (2 * sigma**2))
            valor = termo1 * termo2

            kernel[y + offset, x + offset] = valor
            soma += valor

    # Normalização (soma dos pesos = 1)
    for i in range(size):
        for j in range(size):
            kernel[i, j] /= soma

    return kernel


# -------------------------
# 3. Convolução manual com padding
# -------------------------

def convolution(img, kernel):
    altura, largura = img.shape
    ksize = kernel.shape[0]
    offset = ksize // 2

    # Criação do padding (bordas pretas)
    padded = np.zeros((altura + 2*offset, largura + 2*offset), dtype=np.uint8)

    # Copia imagem original para o centro do padding
    for y in range(altura):
        for x in range(largura):
            padded[y + offset, x + offset] = img[y, x]

    output = np.zeros((altura, largura), dtype=np.float32)

    # Convolução
    for y in range(altura):

        # Apenas para acompanhar progresso
        if y % 10 == 0:
            print(f"Processando linha {y}/{altura}...")

        for x in range(largura):

            soma_pixel = 0.0

            # Aplica o kernel
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

    # Percorre pixel a pixel
    for y in range(altura):
        for x in range(largura):

            g = int(gray[y, x])     # imagem original
            b = int(blurred[y, x])  # imagem borrada

            # Evita divisão por zero
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
# 5. Redimensionamento proporcional
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

img = cv2.imread("fotos/onca_natureza.jpg")
cv2.imwrite("fotos/animal.png", img)

print("Imagem carregada!")

# Redimensionamento
img = resize_proporcional(img)
print("Imagem redimensionada!")


# -------------------------
# Pipeline de processamento
# -------------------------

gray = to_gray_manual(img)

kernel = gaussian_kernel(21, 3.0)

blurred = convolution(gray, kernel)

sketch = pencil_effect(gray, blurred)


# -------------------------
# Salvar resultado
# -------------------------

os.makedirs("resultados", exist_ok=True)

caminho = "resultados/questao_um.png"
cv2.imwrite(caminho, sketch)

print(f"Imagem salva em: {caminho}")


# -------------------------
# Exibição
# -------------------------

plt.figure(figsize=(12,4))

plt.subplot(1,4,1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original")
plt.axis("off")

plt.subplot(1,4,2)
plt.imshow(gray, cmap="gray")
plt.title("Cinza")
plt.axis("off")

plt.subplot(1,4,3)
plt.imshow(blurred, cmap="gray")
plt.title("Gaussiano")
plt.axis("off")

plt.subplot(1,4,4)
plt.imshow(sketch, cmap="gray")
plt.title("Lápis")
plt.axis("off")

plt.show()
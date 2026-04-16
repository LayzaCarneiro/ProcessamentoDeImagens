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

    # Imagem de saída
    result = np.zeros((altura, largura), dtype=np.uint8)

    print(f"Quantizando para {niveis} níveis...")

    # Define o tamanho de cada intervalo de intensidade
    passo = int(256 / niveis)

    # Fator de expansão para redistribuir os níveis no intervalo [0,255]
    escala = 255 / (256 - passo)

    for y in range(altura):
        for x in range(largura):

            valor = img[y, x]

            # Quantização: reduz os níveis de intensidade
            q = int(valor / passo) * passo

            # Expansão de contraste: "empurra" os valores para preto/branco
            novo_valor = int(q * escala)

            # Clipping de segurança
            if novo_valor > 255:
                novo_valor = 255

            result[y, x] = novo_valor

    return result

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

img = cv2.imread('fotos/praia.png')

print("Imagem carregada!")

# Redimensionamento para melhorar desempenho
img = resize_proporcional(img)
print("Imagem redimensionada!")


# -------------------------
# Pipeline
# -------------------------

# Conversão para cinza
img_gray = to_gray_manual(img)

# Lista de níveis de quantização
niveis_lista = [64, 32, 16, 8, 4, 2]

imagens = []
titulos = []

# Imagem original (8 bits = 256 níveis)
imagens.append(img_gray)
titulos.append("(a) 256 níveis (8-bit)")

# Aplica quantização para cada nível
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
# Salvar resultado
# -------------------------

plt.figure(figsize=(18,5))

for i in range(len(imagens)):
    plt.subplot(1, len(imagens), i+1)
    plt.imshow(imagens[i], cmap="gray", vmin=0, vmax=255)
    plt.title(titulos[i])
    plt.axis("off")

plt.tight_layout()
plt.savefig("resultados/teste/img_quantizada.png", dpi=300, bbox_inches='tight')
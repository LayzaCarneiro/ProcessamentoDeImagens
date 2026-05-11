import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import os

# ==================================================
# QUESTÃO 2 - Transformada de Fourier e filtros
# ==================================================


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


# -------------------------------
# 2. Converter espectro em imagem
# -------------------------------

def espectro_para_imagem(espectro):
    magnitude = 20 * np.log(np.abs(espectro) + 1)
    return np.clip(magnitude, 0, 255).astype(np.uint8)


# -------------------------
# 3. Criar máscaras
# -------------------------

def criar_mascaras(altura, largura):
    centro_y = altura // 2
    centro_x = largura // 2
    raio_corte = 40
    raio_min = 20
    raio_max = 60

    passa_baixa = np.zeros((altura, largura),dtype=np.float32)
    passa_alta = np.zeros((altura, largura),dtype=np.float32)
    passa_faixa = np.zeros((altura, largura),dtype=np.float32)
    rejeita_faixa = np.ones((altura, largura),dtype=np.float32)

    for y in range(altura):
        for x in range(largura):
            distancia = math.sqrt((y - centro_y) ** 2 + (x - centro_x) ** 2)

            # Passa-baixa
            if distancia <= raio_corte:
                passa_baixa[y, x] = 1.0

            # Passa-alta
            if distancia > raio_corte:
                passa_alta[y, x] = 1.0

            # Passa-faixa
            if raio_min <= distancia <= raio_max:
                passa_faixa[y, x] = 1.0

            # Rejeita-faixa
            if raio_min <= distancia <= raio_max:
                rejeita_faixa[y, x] = 0.0

    return (passa_baixa, passa_alta, passa_faixa, rejeita_faixa)


# -------------------------
# 4. Aplicar máscaras
# -------------------------

def aplicar_mascara(espectro, mascara):
    altura, largura = espectro.shape
    espectro_filtrado = np.zeros((altura, largura), dtype=complex)

    for y in range(altura):
        for x in range(largura):
            espectro_filtrado[y, x] = (espectro[y, x] * mascara[y, x])

    return espectro_filtrado

# -------------------------------
# 5. Carregar e aplicar na imagem
# -------------------------------

# Passo I: Abrir imagem e converter para escala de cinza;
img = cv2.imread("fotos/pavao.png")
if img is None:
    print("Erro ao carregar imagem")
    exit()

gray = to_gray_manual(img)
altura, largura = gray.shape
print("Imagem carregada!")

os.makedirs("resultados", exist_ok=True) # criar pastas de resultados
os.makedirs("resultados/fft", exist_ok=True) # criar subpasta para salvar cada resultado

# Passo II: Aplicando transformada rápida de Fourier;
print("Calculando FFT 2D...")
fourier_transform = np.fft.fft2(gray) # Transformada de Fourier

# Passo III: Centralizar o espectro de frequência;
fourier_shift = np.fft.fftshift(fourier_transform) # centralizar frequência zero
print("FFT concluída!")

espectro_visual = espectro_para_imagem(fourier_shift)
cv2.imwrite("resultados/fft/espectro_fourier.png", espectro_visual) # salvar Espectro

# Passo IV: Criar os núcleos (máscaras) para os diferentes filtros com as mesmas dimensões das imagens;
print("Criando máscaras...")
(mascara_pb, mascara_pa, mascara_pf, mascara_rf) = criar_mascaras(altura, largura)

cv2.imwrite("resultados/fft/mascara_passa_baixa.png", (mascara_pb * 255).astype(np.uint8))
cv2.imwrite("resultados/fft/mascara_passa_alta.png", (mascara_pa * 255).astype(np.uint8))
cv2.imwrite("resultados/fft/mascara_passa_faixa.png", (mascara_pf * 255).astype(np.uint8))
cv2.imwrite("resultados/fft/mascara_rejeita_faixa.png", (mascara_rf * 255).astype(np.uint8))

# Passo V: Aplicar cada filtro por meio da multiplicação entre o espectro de frequência e a máscara do filtro;
print("Aplicando filtros...")
espectro_pb = aplicar_mascara(fourier_shift, mascara_pb)
espectro_pa = aplicar_mascara(fourier_shift, mascara_pa)
espectro_pf = aplicar_mascara(fourier_shift, mascara_pf)
espectro_rf = aplicar_mascara(fourier_shift, mascara_rf)

# Salvar Espectros
cv2.imwrite("resultados/fft/espectro_pb.png",espectro_para_imagem(espectro_pb))
cv2.imwrite("resultados/fft/espectro_pa.png",espectro_para_imagem(espectro_pa))
cv2.imwrite("resultados/fft/espectro_pf.png",espectro_para_imagem(espectro_pf))
cv2.imwrite("resultados/fft/espectro_rf.png",espectro_para_imagem(espectro_rf))

# Passo VI: Aplicar a transformada inversa de Fourier para Reconstrução Espacial
print("Reconstruindo imagens...")

imagens_finais = []
titulos = []
filtros = {"Passa-Baixa": espectro_pb, "Passa-Alta": espectro_pa, "Passa-Faixa": espectro_pf, "Rejeita-Faixa": espectro_rf}

for nome, espectro in filtros.items():
    print(f"Reconstruindo {nome}...")
    espectro_descentralizado = np.fft.ifftshift(espectro)
    imagem_reconstruida = np.abs(np.fft.ifft2(espectro_descentralizado))

    img_final = np.clip(imagem_reconstruida, 0, 255).astype(np.uint8)
    imagens_finais.append(img_final)
    titulos.append(nome)
    nome_arquivo = (nome.lower().replace("-", "_").replace(" ", "_"))

    cv2.imwrite(f"resultados/fft/{nome_arquivo}.png", img_final)


# ----------------------------------------
# 13. Passo VII - Compressão e Histogramas
# ----------------------------------------

print("Iniciando compressão e histogramas...")
magnitude_espectro = np.abs(fourier_shift) # Magnitude do espectro
energia_maxima = np.max(magnitude_espectro) # Energia máxima
limiar = 0.05 * energia_maxima # Limiar de compressão

# Compressão Lossy
print("Aplicando compressão...")
espectro_comprimido = np.copy(fourier_shift)

for y in range(altura):
    for x in range(largura):
        if magnitude_espectro[y, x] < limiar:
            espectro_comprimido[y, x] = 0j

# Reconstruir imagem comprimida
print("Reconstruindo imagem comprimida...")
espectro_comp_descentralizado = (np.fft.ifftshift(espectro_comprimido))
imagem_comprimida = np.abs(np.fft.ifft2(espectro_comp_descentralizado))
img_comprimida_final = np.clip(imagem_comprimida, 0, 255).astype(np.uint8)

# Salvar imagem comprimida
cv2.imwrite("resultados/fft/imagem_comprimida.png", img_comprimida_final)

# Histogramas manuais
print("Calculando histogramas...")
hist_original = np.zeros(256, dtype=int)
hist_comprimido = np.zeros(256, dtype=int)

for y in range(altura):
    for x in range(largura):
        pixel_original = gray[y, x]
        pixel_comprimido = img_comprimida_final[y, x]
        hist_original[pixel_original] += 1
        hist_comprimido[pixel_comprimido] += 1

# Salvar histogramas
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1) # Histograma Original
plt.title("Histograma Original")
plt.bar(range(256), hist_original, color="gray")
plt.subplot(1, 2, 2) # Histograma Comprimido
plt.title("Histograma Comprimido")
plt.bar(range(256), hist_comprimido, color="blue")
plt.tight_layout()
plt.savefig("resultados/fft/comparativo_histogramas.png", dpi=300, bbox_inches="tight")


# ------------------------------
# 9. Salvar e Mostrar Resultados
# ------------------------------

plt.figure(figsize=(14, 8))
plt.subplot(2, 3, 1)
plt.imshow(gray, cmap="gray")
plt.title("Original")
plt.axis("off")

for i in range(len(imagens_finais)):
    plt.subplot(2, 3, i + 2)
    plt.imshow(imagens_finais[i], cmap="gray")
    plt.title(titulos[i])
    plt.axis("off")

plt.tight_layout()
plt.savefig("resultados/resultado_geral_fft.png", dpi=300, bbox_inches="tight")
print("\nResultados salvos em: resultados/")

plt.show()
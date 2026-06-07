import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================================================
# QUESTÃO 2 - Descritores de Imagem
# ==================================================

# -------------------------
# 1. Converter para cinza
# -------------------------
def to_gray(img):
    altura, largura, _ = img.shape
    gray = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]

            # Conversão manual para tons de cinza usando a fórmula de luminância
            valor = int(0.299 * r + 0.587 * g + 0.114 * b) 

            if valor > 255:
                valor = 255

            gray[y, x] = valor

    return gray


# -------------------------
# 2. Média (Brilho geral)
# -------------------------
def calcular_media(img):
    altura, largura = img.shape
    soma = 0.0

    for y in range(altura):
        for x in range(largura):
            soma += img[y, x]
    media = soma / (altura * largura)

    return media


# -------------------------------
# 3. Variância (Contraste global)
# -------------------------------
def calcular_variancia(img, media):
    altura, largura = img.shape
    soma = 0.0

    for y in range(altura):
        for x in range(largura):
            soma += (img[y, x] - media) ** 2

    variancia = soma / (altura * largura)

    return variancia


# -----------------------------------------------------------
# 4. Energia (Uniformidade/Homogeneidade dos níveis de cinza)
# -----------------------------------------------------------
def calcular_energia(img):
    altura, largura = img.shape

    # Primeiro calculamos o histograma normalizado (probabilidades)
    frequencias = [0] * 256
    for y in range(altura):
        for x in range(largura):
            frequencias[img[y, x]] += 1
            
    energia = 0.0
    for i in range(256):
        p_i = frequencias[i] / (altura * largura)
        energia += p_i ** 2  # Soma das probabilidades ao quadrado

    return energia

# --------------------------------------------------------------------
# 5. Diferença Absoluta Horizontal (Variação de textura na horizontal)
# --------------------------------------------------------------------
def diferenca_horizontal(img):
    altura, largura = img.shape
    diff_horizontal = 0.0

    for y in range(altura):
        for x in range(largura - 1):
            atual = img[y, x]
            vizinho = img[y, x + 1]
            diff_horizontal += abs(atual - vizinho)

    diff_horizontal /= (altura * (largura - 1)) # Média por pixel vizinho
    return diff_horizontal


# ----------------------------------------------------------------
# 6. Diferença Absoluta Vertical (Variação de textura na vertical)
# ----------------------------------------------------------------
def diferenca_vertical(img):
    altura, largura = img.shape
    diff_vertical = 0.0

    for y in range(0, altura - 1):
        for x in range(largura):
            atual = img[y, x]
            vizinho = img[y + 1, x]
            diff_vertical += abs(atual - vizinho)

    diff_vertical /= ((altura - 1) * largura) # Média por pixel vizinho
    return diff_vertical


# -------------------------
# 7. Extrair descritores
# -------------------------

def extrair_descritores(img_gray):
    # Converter para float para evitar overflow nos cálculos matemáticos
    img_f = img_gray.astype(float)
    
    # --- A. Métricas Estatísticas Globais ---
    media = calcular_media(img_f)
    variancia = calcular_variancia(img_f, media)
    energia = calcular_energia(img_gray)

    # --- B. Medidas de Variação Espacial (Estruturais) ---
    diff_horizontal = diferenca_horizontal(img_f)
    diff_vertical = diferenca_vertical(img_f)

    return {
        "Média": media,
        "Variância": variancia,
        "Energia": energia,
        "Diff_Horizontal": diff_horizontal,
        "Diff_Vertical": diff_vertical
    }


# -------------------------
# 8. Carregar imagens
# -------------------------
print("Carregando imagens...")
img1 = cv2.imread("fotos/aurora_boreal.png")
img2 = cv2.imread("fotos/macaco.png")

if img1 is None or img2 is None:
    print("Erro ao carregar imagens")
    exit()

gray1 = to_gray(img1)
gray2 = to_gray(img2)
print("Imagens carregadas!")


# -------------------------
# 9. Criar pastas
# -------------------------
os.makedirs("resultados", exist_ok=True)
os.makedirs("resultados/q2", exist_ok=True)


# -------------------------
# 10. Extrair descritores
# -------------------------
descritores1 = extrair_descritores(gray1)
descritores2 = extrair_descritores(gray2)


# -------------------------
# 11. Mostrar resultados
# -------------------------
print("\n==============================")
print("DESCRITORES - IMAGEM 1")
print("==============================")

for chave, valor in descritores1.items():
    print(f"{chave}: {valor}")

print("\n==============================")
print("DESCRITORES - IMAGEM 2")
print("==============================")

for chave, valor in descritores2.items():
    print(f"{chave}: {valor}")


# -------------------------
# 12. Salvar imagens
# -------------------------
cv2.imwrite("resultados/q2/imagem1_gray.png", gray1)
cv2.imwrite("resultados/q2/imagem2_gray.png", gray2)


# -------------------------
# 13. Gráfico comparativo
# -------------------------
descritores = {
    "Média": (descritores1["Média"], descritores2["Média"]),
    "Variância": (descritores1["Variância"], descritores2["Variância"]),
    "Energia": (descritores1["Energia"], descritores2["Energia"]),
    "Dif. Horizontal": (descritores1["Diff_Horizontal"], descritores2["Diff_Horizontal"]),
    "Dif. Vertical": (descritores1["Diff_Vertical"], descritores2["Diff_Vertical"])
}

fig, axs = plt.subplots(2, 3, figsize=(15, 8))
axs = axs.flatten()

for i, (nome, valores) in enumerate(descritores.items()):
    barras = axs[i].bar(["Imagem 1", "Imagem 2"], valores)

    axs[i].set_title(nome)
    axs[i].set_ylabel("Valor")
    axs[i].grid(axis="y", alpha=0.3)

    # margem superior para os textos
    axs[i].set_ylim(0, max(valores) * 1.15)

    # valor acima das barras
    for barra in barras:
        altura = barra.get_height()
        axs[i].text(
            barra.get_x() + barra.get_width() / 2,
            altura,
            f"{altura:.4f}",
            ha="center",
            va="bottom",
            fontsize=8
        )

# remove o sexto subplot vazio
fig.delaxes(axs[5])

plt.suptitle("Comparação dos Descritores",  fontsize=16)
plt.tight_layout()
plt.savefig("resultados/q2/comparacao_descritores.png", dpi=300, bbox_inches="tight")
plt.show()


# -------------------------
# 14. Salvar relatório txt
# -------------------------
arquivo = open("resultados/q2/descritores.txt", "w")

arquivo.write("DESCRITORES - IMAGEM 1\n")
arquivo.write("========================\n")

for chave, valor in descritores1.items():
    arquivo.write(f"{chave}: {valor}\n")

arquivo.write("\n")

arquivo.write("DESCRITORES - IMAGEM 2\n")
arquivo.write("========================\n")

for chave, valor in descritores2.items():
    arquivo.write(f"{chave}: {valor}\n")

arquivo.close()

print("\nResultados salvos em resultados/q2")
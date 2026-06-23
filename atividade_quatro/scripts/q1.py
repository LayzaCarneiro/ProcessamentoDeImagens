import cv2
import numpy as np
import os

# =========================================================================
# Q1 - OPERAÇÕES MORFOLÓGICAS MANUAIS (IMAGENS BINÁRIAS)
# =========================================================================

def erosao(img_binaria, k_size):
    """
    Aplica a erosão usando kernel de tamanho k_size.
    Para erosão: o pixel central só será 255 se TODOS os pixels na vizinhança forem 255.
    """
    altura, largura = img_binaria.shape
    img_saida = np.zeros_like(img_binaria)
    pad = k_size // 2
    
    # Varre a imagem ignorando as bordas do padding
    for y in range(pad, altura - pad):
        for x in range(pad, largura - pad):
            # Recorta a vizinhança sob o elemento estruturante
            vizinhanca = img_binaria[y - pad : y + pad + 1, x - pad : x + pad + 1]
            
            # Se todos forem 255 (objeto), mantém 255. Se houver um 0, vira 0.
            if np.all(vizinhanca == 255):
                img_saida[y, x] = 255
            else:
                img_saida[y, x] = 0
                
    return img_saida


def dilatacao(img_binaria, k_size):
    """
    Aplica a dilatação usando um kernel de tamanho k_size.
    Para dilatação: o pixel central será 255 se PELO MENOS UM pixel na vizinhança for 255.
    """
    altura, largura = img_binaria.shape
    img_saida = np.zeros_like(img_binaria)
    pad = k_size // 2
    
    for y in range(pad, altura - pad):
        for x in range(pad, largura - pad):
            vizinhanca = img_binaria[y - pad : y + pad + 1, x - pad : x + pad + 1]
            
            # Se houver pelo menos um pixel branco (255), o pixel central vira branco
            if np.any(vizinhanca == 255):
                img_saida[y, x] = 255
            else:
                img_saida[y, x] = 0
                
    return img_saida


def abertura(img_binaria, k_size):
    """ Abertura = Erosão seguida de Dilatação """
    erodida = erosao(img_binaria, k_size)
    aberta = dilatacao(erodida, k_size)
    return aberta


def fechamento(img_binaria, k_size):
    """ Fechamento = Dilatação seguida de Erosão """
    dilatada = dilatacao(img_binaria, k_size)
    fechada = erosao(dilatada, k_size)
    return fechada


# =========================================================================
# PIPELINE DE TESTES E DEMONSTRAÇÃO
# =========================================================================

imagens_caminhos = ["fotos/zebra.png", "fotos/moscow.png"]
tamanhos_kernel = [3, 5, 15]

for idx, caminho in enumerate(imagens_caminhos, start=1):
    print(f"\n--- Processando Imagem {idx}: {caminho} ---")
    
    img = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem em: {caminho}")
        continue
        
    # Garante que a imagem esteja binarizada (Threshold simples)
    # Valores acima de 127 viram 255, abaixo viram 0.
    _, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    
    # Cria diretório específico para organizar os resultados da imagem atual
    pasta_destino = f"resultados/imagem_{idx}"
    os.makedirs(pasta_destino, exist_ok=True)
    cv2.imwrite(f"{pasta_destino}/0_original_binaria.png", img_bin)
    
    # Aplica as operações para cada tamanho de elemento estruturante solicitado
    for k in tamanhos_kernel:
        print(f"Aplicando máscaras de tamanho {k}x{k}...")
        
        # Executa as transformações
        img_erodida = erosao(img_bin, k)
        img_dilatada = dilatacao(img_bin, k)
        img_abertura = abertura(img_bin, k)
        img_fechamento = fechamento(img_bin, k)
        
        # Salva os resultados salvaguardando o tamanho do kernel no nome do arquivo
        cv2.imwrite(f"{pasta_destino}/erosao_{k}x{k}.png", img_erodida)
        cv2.imwrite(f"{pasta_destino}/dilatacao_{k}x{k}.png", img_dilatada)
        cv2.imwrite(f"{pasta_destino}/abertura_{k}x{k}.png", img_abertura)
        cv2.imwrite(f"{pasta_destino}/fechamento_{k}x{k}.png", img_fechamento)

print("\nTodas as operações foram concluídas! Verifique a pasta 'resultados_morfologia'.")
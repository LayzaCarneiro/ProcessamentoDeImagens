# Processamento de Imagens (PI)

Este projeto reúne duas atividades de **Processamento de Imagens** desenvolvidas em Python, com implementação direta sobre pixels e sem uso de funções de alto nível do OpenCV.

---

# Visão Geral

O repositório contém duas atividades principais:

* `atividade_um/` — operações básicas de PDI e transformações geométricas.
* `atividade_dois/` — análise de frequência, filtros e tratamento de sinais em imagens.
* `atividade_tres/` — compressão, representação e descrição de imagens digitais.

Cada atividade inclui imagens de entrada, resultados gerados e scripts das questões.

---

# Atividade 1: Processamento Direto de Imagens

Nesta primeira etapa foram exploradas técnicas de manipulação clássicas, aplicadas diretamente em arrays de pixels:

* conversão para escala de cinza
* correção gama e ajuste de brilho/contraste
* quantização de níveis de cinza
* filtros de suavização e realce
* combinações de imagens e mosaicos
* transformações geométricas simples

Resultados:

* imagens originais comparadas com versões processadas
* redução de ruído e melhoria de contraste
* efeitos visuais de quantização e filtragem
* geração de mosaicos e composições a partir de múltiplas entradas

---

# Atividade 2: Filtros e Transformada de Fourier

A segunda atividade foi focada em análise de frequência e filtragem:

* cálculo manual da FFT de imagens
* visualização de espectros de magnitude
* aplicação de filtros em domínio espacial e de frequência
* comparação entre imagem original e filtrada

Resultados:

* identificação de componentes de frequência nas imagens
* remoção de ruído e suavização seletiva
* efeitos de filtragem implementados a partir da matemática da transformada

---

# Atividade 3: Compressão, Representação e Descrição de Imagens

A terceira atividade teve como foco a representação compacta e a caracterização quantitativa de imagens digitais:

* aplicação de transformações para representação da informação em diferentes domínios
* análise de técnicas de compressão e redução de redundância
* extração de descritores estatísticos globais
* cálculo de medidas como média, variância e energia
* obtenção de descritores baseados em diferenças horizontais e verticais
* comparação quantitativa entre diferentes imagens por meio dos descritores extraídos

Resultados:

* representação mais compacta dos dados visuais por meio de transformações apropriadas
* análise do impacto da compressão na preservação das informações da imagem
* caracterização numérica das imagens através de descritores estatísticos
* comparação objetiva entre imagens utilizando medidas extraídas automaticamente
  
---

# Estrutura do Projeto

```text
.
├── atividade_dois/
│   ├── fotos/            # Imagens de entrada da atividade 2
│   ├── resultados/       # Resultados gerados pela atividade 2
│   ├── scripts/          # Códigos das questões da atividade 2
│   ├── Atividade2PI.pdf 
│   └── relatorio_atividade_dois_pi.pdf
├── atividade_tres/
│   ├── fotos/            # Imagens de entrada da atividade 3
│   ├── resultados/       # Resultados gerados pela atividade 3
│   ├── scripts/          # Códigos das questões da atividade 3
│   ├── Atividade3PI.pdf 
│   └── relatorio_atividade_tres_pi.pdf
├── atividade_um/
│   ├── fotos/           # Imagens de entrada da atividade 1
│   ├── resultados/      # Resultados gerados pela atividade 1
│   ├── scripts/         # Códigos das questões da atividade 1
│   ├── Atividade1PI.pdf 
│   └── relatorio_atividade_um_pi.pdf
├── README.md
```

---

# Como Executar

1. Ative o ambiente virtual:

```bash
source venv/bin/activate
```

2. Instale dependências:

```bash
pip3 install opencv-python numpy matplotlib
```

3. Navegue até a atividade desejada e execute o script correspondente:

```bash
cd atividade_um && python3 scripts/q1.py
```

ou

```bash
cd atividade_dois && python3 scripts/q1.py
```

4. Os resultados são:

* exibidos na tela
* salvos em `resultados/`

---

# Resultado Final

O projeto demonstra duas frentes do processamento de imagens:

* **atividade 1:** transformações diretas e manipulação clássica de pixels.
* **atividade 2:** análise de frequência e filtragem sofisticada.
* **atividade 3:** compressão, representação e descrição de imagens.

Cada atividade entrega resultados visuais e arquivos de saída que ilustram o efeito de cada técnica aplicada.

### Preview dos Resultados da Atividade 1

| Questão | Resultado |
|--------|------------|
| 1 | <img src="https://github.com/user-attachments/assets/51eaf8b2-b313-4a60-816e-e0204fdf26ef" width="700"/> |
| 2 | <img src="https://github.com/user-attachments/assets/64acc593-cfcf-4a3e-b847-cf5fd0b3b31d" width="700"/> |
| 3 | <img src="https://github.com/user-attachments/assets/11ab3758-ea2e-4458-b88d-1e48d3254c69" width="700"/> |
| 4 | <img src="https://github.com/user-attachments/assets/a6a0c186-ffdf-4ab2-a01d-887371248b01" width="700"/> |
| 5 | <img src="https://github.com/user-attachments/assets/1512a384-6e72-4f0e-858d-19f9ee25da31" width="700"/> |
| 6 | <img src="https://github.com/user-attachments/assets/b748541c-b945-4f74-9211-29cfbf853815" width="700"/> |

### Preview dos Resultados da Atividade 2

| Questão | Resultado |
|--------|----------|
| 1 | <img src="https://github.com/user-attachments/assets/229ed1ef-7cdc-41db-a631-b7170e1e10bf" width="700"/> |
| 2 | <img src="https://github.com/user-attachments/assets/5aaa9325-dee0-4134-bc3a-b8d2791d85dc" width="700"/> |

### Preview dos Resultados da Atividade 3
#### Questão 1 — Representação por Blocos

| Tamanho do Bloco | Resultado |
|------------------|-----------|
| 2×2 | <img src="https://github.com/user-attachments/assets/a72340f1-dd04-43e5-a530-1e38dd8d7516" width="700"/> |
| 8×8 | <img src="https://github.com/user-attachments/assets/f44886c7-d3bc-42ad-8841-e849322d2bc0" width="700"/> |
| 16×16 | <img src="https://github.com/user-attachments/assets/e4d6e529-9146-4876-9338-6a5895fb545e" width="700"/> |
| 64×64 | <img src="https://github.com/user-attachments/assets/3bfb3da4-f4dc-4e2e-a144-90779948a32c" width="700"/> |

#### Questão 2 — Descritores de Imagens

| Resultado | Imagem |
|------------|--------|
| Imagem 1 | <img src="https://github.com/user-attachments/assets/d6fc4007-0fb5-41e0-8f14-27f375fe1bd8" width="400"/> |
| Imagem 2 | <img src="https://github.com/user-attachments/assets/7651a338-a269-45ff-b694-ee25ffacdc37" width="400"/> |
| Comparação dos Descritores | <img src="https://github.com/user-attachments/assets/2a65da30-c899-472d-8718-2850fa3940de" width="500"/> |

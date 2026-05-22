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
│   └── relatorio_atividade_dois_pi.pdf
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

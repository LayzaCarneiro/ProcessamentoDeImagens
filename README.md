# Processamento de Imagens (PI)

Este projeto reúne duas atividades de **Processamento de Imagens** desenvolvidas em Python, com implementação direta sobre pixels e sem uso de funções de alto nível do OpenCV.

---

# Visão Geral

O repositório contém duas atividades principais:

* `atividade_um/` — operações básicas de PDI e transformações geométricas.
* `atividade_dois/` — análise de frequência, filtros e tratamento de sinais em imagens.

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
├── atividade_um/
│   ├── fotos/           # Imagens de entrada da atividade 1
│   ├── resultados/      # Resultados gerados pela atividade 1
│   ├── scripts/         # Códigos das questões da atividade 1
│   └── relatorio_atividade_um_pi.pdf
├── atividade_dois/
│   ├── fotos/           # Imagens de entrada da atividade 2
│   ├── resultados/      # Resultados gerados pela atividade 2
│   ├── scripts/         # Códigos das questões da atividade 2
│   └── relatorio_atividade_dois_pi.pdf
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

# Observações

* As implementações evitam funções prontas do OpenCV sempre que possível.
* O processamento é feito pixel a pixel ou com conceitos matemáticos explícitos.
* O uso de PNG é preferido para reduzir perdas por compressão.

---

# Resultado Final

O projeto demonstra duas frentes do processamento de imagens:

* **atividade 1:** transformações diretas e manipulação clássica de pixels.
* **atividade 2:** análise de frequência e filtragem sofisticada.

Cada atividade entrega resultados visuais e arquivos de saída que ilustram o efeito de cada técnica aplicada.

# Processamento de Imagens (PI)

Este projeto contém a implementação de diversas técnicas de **Processamento de Imagens**, desenvolvidas manualmente utilizando Python, com foco em manipulação direta dos pixels.

---

# Resumo da Atividade

O trabalho consiste na implementação de operações fundamentais de PDI, como:

* Conversão para escala de cinza
* Aplicação de filtros (ex: Gaussiano)
* Correção gama
* Quantização de níveis de cinza
* Transformações geométricas
* Combinação de imagens
* Construção de mosaicos

As implementações foram feitas **sem uso de funções prontas do OpenCV**, priorizando o entendimento dos algoritmos na base matemática.

Além disso, foram realizadas análises visuais para compreender o impacto de cada transformação nas imagens.

---

# Requisitos

* Python 3.x
* pip

---

# Instalação

## 1. Criar ambiente virtual

```bash
python3 -m venv venv
```

## 2. Ativar o ambiente

### Linux / Mac:

```bash
source venv/bin/activate
```

### Windows:

```bash
venv\Scripts\activate
```

---

## 3. Instalar dependências

```bash
pip3 install opencv-python numpy matplotlib
```

---

# Estrutura do Projeto

```text
.
├── fotos/           # Imagens de entrada
├── resultados/      # Imagens geradas pelo processamento
├── scripts/         # Códigos das questões
├── README.md
```

---

# Como Executar

1. Coloque as imagens na pasta `fotos/`
2. Execute o script desejado:

```bash
python3 nome_do_arquivo.py
```

3. Os resultados serão:

* ✔ exibidos na tela (preview)
* ✔ salvos automaticamente na pasta `resultados/`

---

# Observações Importantes

* As imagens são redimensionadas (quando necessário) para evitar alto custo computacional.
* Sempre que possível, utiliza-se o formato **PNG** para evitar perda de qualidade.
* Todas as operações foram implementadas **manualmente**, percorrendo pixel a pixel.

---

# Sobre os Resultados

Cada técnica aplicada gera efeitos distintos, como:

* **Correção gama:** ajuste de brilho e contraste
* **Quantização:** redução de níveis de cinza e perda de detalhes
* **Filtros:** suavização ou realce de regiões
* **Transformações:** alteração da geometria da imagem

As análises foram feitas com base em comparações visuais entre as imagens originais e processadas.
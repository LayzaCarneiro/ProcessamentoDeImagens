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

---

# Preview dos Resultados

| Questão | Original | Processada |
|--------|----------|------------|
| 1 | <img src="https://github.com/user-attachments/assets/324fd750-a7e1-427e-87c0-61d524513cb1" width="200"/> | <img src="https://github.com/user-attachments/assets/51eaf8b2-b313-4a60-816e-e0204fdf26ef" width="300"/> |
| 2 | <img src="https://github.com/user-attachments/assets/49ea8dac-75c5-4a84-bd21-73ce980143d5" width="200"/> | <img src="https://github.com/user-attachments/assets/64acc593-cfcf-4a3e-b847-cf5fd0b3b31d" width="300"/> |
| 3 | <img src="https://github.com/user-attachments/assets/3d26de04-db64-4739-8c7d-bab909f38941" width="150"/> <img src="https://github.com/user-attachments/assets/8a1df2e9-26ba-449a-b0ba-5b2a158605e0" width="150"/> | <img src="https://github.com/user-attachments/assets/11ab3758-ea2e-4458-b88d-1e48d3254c69" width="300"/> |
| 4 | <img src="https://github.com/user-attachments/assets/98626a56-6470-44e6-b1e7-2974d76e067d" width="200"/> | <img src="https://github.com/user-attachments/assets/a6a0c186-ffdf-4ab2-a01d-887371248b01" width="300"/> |
| 5 | <img src="https://github.com/user-attachments/assets/39eb74d6-d603-496c-8b2d-66b647540d64" width="200"/> | <img src="https://github.com/user-attachments/assets/1512a384-6e72-4f0e-858d-19f9ee25da31" width="300"/> |
| 6 | <img src="https://github.com/user-attachments/assets/38b032a6-41d9-4fb6-8c11-96c2319fc171" width="200"/> | <img src="https://github.com/user-attachments/assets/b748541c-b945-4f74-9211-29cfbf853815" width="300"/> |

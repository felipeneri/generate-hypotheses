# 🕵️ Detetive de Dados - Gerador de Hipóteses com IA

**Status do Projeto:** Backend Concluído | Frontend em Desenvolvimento

## 💡 Conceito

O **Detetive de Dados** é um projeto que inverte a lógica tradicional da análise de dados. Em vez de um analista fazer perguntas a um conjunto de dados, esta ferramenta utiliza o poder da Inteligência Artificial Generativa (Google Gemini) para analisar a estrutura de um dataset e **sugerir quais perguntas e hipóteses valem a pena ser investigadas**.

O objetivo é acelerar a fase de Análise Exploratória de Dados (EDA), fornecendo ao analista um ponto de partida criativo e insights que poderiam passar despercebidos.

## 🚀 Demonstração (Teste de Backend)

A imagem abaixo mostra um teste do backend sendo realizado através do Insomnia. O corpo da requisição (`body`) contém o conteúdo de um arquivo CSV em formato de string dentro de um JSON, e a resposta (`response`) exibe as hipóteses geradas pela IA.

![Demonstração no Insomnia](https://ik.imagekit.io/5wm4hyxnh/hypotheses.png)

## 🛠️ Tecnologias Utilizadas

### Backend

- **Linguagem:** Python 3.11+
- **Framework da API:** FastAPI
- **Análise de Dados:** Pandas
- **IA Generativa:** Google Gemini API (`google-generativeai`)
- **Servidor:** Uvicorn

### Frontend (Planejado)

- **Framework:** Next.js
- **Linguagem:** TypeScript
- **Estilização:** Tailwind CSS

## ⚙️ Como Funciona o Backend

1.  **Requisição:** O servidor FastAPI recebe uma requisição `POST` no endpoint `/api/generate-hypotheses`. O corpo da requisição contém um JSON com uma chave `csv_content`, cujo valor é uma string com todo o conteúdo de um arquivo CSV.
2.  **Análise Estrutural:** A string CSV é carregada em um DataFrame do Pandas.
3.  **Extração de Metadados:** A aplicação extrai informações cruciais do DataFrame: nomes das colunas, tipos de dados (`df.info()`) e estatísticas descritivas (`df.describe()`).
4.  **Geração do Prompt:** Um prompt detalhado e cuidadosamente elaborado é montado, instruindo o modelo do Gemini a agir como um cientista de dados sênior e a gerar hipóteses investigativas com base nos metadados fornecidos.
5.  **Comunicação com a IA:** O prompt é enviado para a API do Google Gemini.
6.  **Resposta:** A API retorna as hipóteses em formato de texto. O backend formata essa resposta em uma lista e a envia de volta para o cliente como um JSON.

## 🏁 Como Executar o Backend Localmente

Siga os passos abaixo para rodar o servidor da API em sua máquina.

### 1\. Pré-requisitos

- Python 3.11 ou superior
- Gerenciador de pacotes `pip`
- Uma chave de API do [Google AI Studio](https://aistudio.google.com/)

### 2\. Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/detetive-de-dados.git
cd detetive-de-dados

# 2. Crie e ative um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
# (Certifique-se de criar um arquivo requirements.txt com as bibliotecas)
```

### 3\. Configuração

1.  Crie um arquivo chamado `.env` na raiz do projeto.
2.  Adicione sua chave da API do Google Gemini a este arquivo:
    ```
    GOOGLE_API_KEY="SUA_CHAVE_AQUI"
    ```

### 4\. Execução

Com o ambiente virtual ativado, inicie o servidor FastAPI:

```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://127.0.0.1:8000`.

## 📖 Documentação da API

### Endpoint: `POST /api/generate-hypotheses`

- **Descrição:** Recebe o conteúdo de um CSV e retorna uma lista de hipóteses geradas pela IA.
- **Corpo da Requisição (Request Body):**
  ```json
  {
    "csv_content": "coluna1,coluna2\nvalor1,valor2\nvalor3,valor4"
  }
  ```
- **Resposta de Sucesso (200 OK):**
  ```json
  {
    "hypotheses": [
      "1. Hipótese gerada número um?",
      "2. Hipótese gerada número dois?",
      "3. Hipótese gerada número três?"
    ]
  }
  ```
- **Respostas de Erro:**
  - `400 Bad Request`: Se o `csv_content` estiver vazio.
  - `500 Internal Server Error`: Se ocorrer um erro durante a comunicação com a API do Gemini ou no processamento dos dados.

## 🔮 Próximos Passos

- [ ] Desenvolver a interface de frontend com Next.js e Tailwind CSS.
- [ ] Criar um componente de upload de arquivos que leia o CSV e o envie para o backend.
- [ ] Exibir as hipóteses recebidas em cartões estilizados.
- [ ] Adicionar tratamento de erros e estados de carregamento (loading) na interface.
- [ ] Implementar a funcionalidade "avançada" de gerar o código Python para testar as hipóteses.

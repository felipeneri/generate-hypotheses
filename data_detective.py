import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from io import StringIO

def configure_api():
    """
    Carrega a chave da API do arquivo .env e configura o SDK do Gemini.
    Esta função deve ser chamada uma vez quando o aplicativo iniciar.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Chave da API do Google não encontrada. Verifique seu arquivo .env")
    genai.configure(api_key=api_key)
    print("API do Google Gemini configurada com sucesso.")

def generate_hypotheses_from_data(csv_data: str) -> str:
    """
    Analisa dados de uma string CSV, extrai metadados e usa o Gemini para gerar hipóteses.

    Args:
        csv_data (str): Uma string contendo os dados em formato CSV.

    Returns:
        str: As hipóteses geradas pelo modelo de IA em texto puro.
    """
    try:
        # 1. Carregar os dados usando Pandas a partir da string
        df = pd.read_csv(StringIO(csv_data))

        # 2. Extrair metadados para construir o prompt
        colunas = df.columns.tolist()
        
        # Captura a saída do df.info() que é muito rica
        buffer = StringIO()
        df.info(buf=buffer)
        info_dataset = buffer.getvalue()
        
        # Captura estatísticas descritivas, se houver colunas numéricas
        estatisticas_descritivas = "Nenhuma coluna numérica para análise estatística."
        if not df.select_dtypes(include='number').empty:
            estatisticas_descritivas = df.describe().to_string()

        # 3. Montar o Prompt para o Gemini
        prompt = f"""
        Você é um cientista de dados sênior, especialista em análise exploratória de dados
        e na formulação de hipóteses investigativas. Seu objetivo é encontrar insights
        potencialmente valiosos que não são óbvios à primeira vista.

        Analise a estrutura do dataset a seguir e gere 5 hipóteses de negócio ou
        de comportamento que valeriam a pena ser investigadas.

        Formule cada hipótese como uma pergunta clara e acionável, iniciando cada uma com um número (ex: 1. Pergunta...).

        **Estrutura do Dataset:**
        ---
        **Colunas:** {colunas}

        **Informações Gerais e Tipos de Dados:**
        {info_dataset}

        **Estatísticas Descritivas (para colunas numéricas):**
        {estatisticas_descritivas}
        ---

        **Gere agora as 5 hipóteses investigativas:**
        """

        print(prompt)
        # 4. Chamar a API do Gemini
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        # Retorna uma string de erro que pode ser mostrada no frontend
        print(f"Erro ao gerar hipóteses: {e}")
        raise e

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Importa as funções do nosso outro arquivo
from data_detective import configure_api, generate_hypotheses_from_data

# --- Modelo de Dados para a Requisição ---
class CsvData(BaseModel):
    csv_content: str

# --- Gerenciador de Ciclo de Vida (Lifespan) ---
# A forma moderna de lidar com eventos de startup e shutdown no FastAPI.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código a ser executado na inicialização:
    print("Servidor iniciando... Configurando API externa.")
    configure_api()
    yield
    # Código a ser executado no encerramento:
    print("Servidor encerrando.")

# --- Inicialização da Aplicação FastAPI ---
# Passamos nosso gerenciador de lifespan para a aplicação.
app = FastAPI(lifespan=lifespan)

# --- Configuração do CORS ---
# Permite que o frontend Next.js se comunique com este backend.
origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoint Principal da API ---
@app.post("/api/generate-hypotheses")
async def get_hypotheses_endpoint(data: CsvData):
    """
    Recebe o conteúdo de um CSV, gera hipóteses e as retorna como JSON.
    """
    if not data.csv_content or not data.csv_content.strip():
        raise HTTPException(status_code=400, detail="O conteúdo do CSV não pode estar vazio.")

    try:
        # Chama a função principal que faz todo o trabalho pesado
        raw_hypotheses = generate_hypotheses_from_data(data.csv_content)

        # Processa a resposta de texto puro para uma lista limpa
        hypotheses_list = [
            line.strip() for line in raw_hypotheses.split('\n')
            if line.strip() and line.strip()[0].isdigit()
        ]

        return {"hypotheses": hypotheses_list}
    except Exception as e:
        # Retorna um erro claro para o frontend.
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")

# --- Ponto de Entrada para Rodar o Servidor ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
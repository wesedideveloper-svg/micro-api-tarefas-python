from fastapi import FastAPI


app = FastAPI(
    title="Micro-API de Gerenciamento de Tarefas",
    version="0.1.0",
    description=(
        "API RESTful de gerenciamento de tarefas desenvolvida como projeto "
        "acadêmico da pós-graduação em Engenharia de Software com "
        "Inteligência Artificial Generativa."
    ),
    docs_url="/docs",
    openapi_url="/openapi.json",
)


@app.get("/health", summary="Verificar o funcionamento da API")
def health() -> dict[str, str]:
    return {"status": "ok"}

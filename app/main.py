from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.tasks import router
from app.database import Base, engine
from app.services.task_service import TaskNotFoundError


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


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
    lifespan=lifespan,
)

app.include_router(router)


@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.get("/health", summary="Verificar o funcionamento da API")
def health() -> dict[str, str]:
    return {"status": "ok"}

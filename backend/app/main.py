from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.routes.health import router as health_router


def create_app() -> FastAPI:
    settings = get_settings()
    # `debug` do Starlette expõe tracebacks em erros 500; a documentação
    # interativa permanece disponível em desenvolvimento conforme APP_DEBUG.
    app = FastAPI(
        title=settings.APP_NAME,
        debug=False,
        docs_url="/docs" if settings.APP_DEBUG else None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.APP_DEBUG else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_error_handlers(app)
    # Health check fora do prefixo /api/v1 (uso de load balancers e testes de prontidão).
    app.include_router(health_router)
    return app


app = create_app()

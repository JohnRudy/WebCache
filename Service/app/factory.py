from fastapi import FastAPI


def create_app() -> FastAPI:
    from app.api.cache.router import router as webcache_router

    app = FastAPI(title="WebCache")

    app.include_router(webcache_router, prefix="/webcache")

    return app

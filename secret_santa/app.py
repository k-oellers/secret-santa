from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def app_factory() -> FastAPI:
    app = FastAPI()
    origins = [
        "http://localhost",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    @app.get("/")
    def main():
        return "Hi"

    @app.get("/{test}")
    def main2(test: str):
        return f"cmd: {test}"

    return app

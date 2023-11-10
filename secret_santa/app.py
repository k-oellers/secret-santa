from fastapi import FastAPI


def app_factory() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def main():
        return "Hi"

    @app.get("/{test}")
    def main2(test: str):
        return f"cmd: {test}"

    return app

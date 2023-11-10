import uvicorn


def serve() -> None:
    uvicorn.run(
        "secret_santa.app:app_factory",
        host="0.0.0.0",
        port=80,
        factory=True,
    )


print(__name__)
serve()

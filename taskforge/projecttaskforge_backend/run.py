import uvicorn


def main() -> None:
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        loop="core.uvicorn_loop:selector_loop_factory",
    )


if __name__ == "__main__":
    main()
